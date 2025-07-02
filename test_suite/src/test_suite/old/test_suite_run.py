from __future__ import annotations

import json
import os
from abc import abstractmethod
from subprocess import PIPE, Popen
from typing import TYPE_CHECKING

from environment.environment_manager import EnvironmentManager
from logging_lib import RootLogger as logger

# from playwright_helpers.playwright_run import start_playwright
from pytest_helpers.pytest_run import start_pytest
from rest_rem_lib.helpers import RestRemLibClientsManager
from rest_rem_lib.rest_rem_lib_client import ClientInfo
from serialize import SerializableMetaclass

from test_suite.constants import SuiteResult
from test_suite.settings import EXECUTOR_PORT, TestSuiteSettings

if TYPE_CHECKING:
    from .test_suite import TestSuite
    from .test_suite_params import TestSuiteParams


class TestSuiteRunBase(metaclass=SerializableMetaclass):
    def __init__(self, test_suite: TestSuite, test_suite_params: TestSuiteParams, report_dir=None):
        self.test_suite = test_suite
        self._reports_dir = report_dir

        self.test_suite_params = test_suite_params

        self._subprocess_result = None

        self._assistants_data = []

        self.assistant_clients = [ClientInfo(ip=ip) for ip in TestSuiteSettings.REMOTE_SERVERS]

        self.file_senders = []

        self._specific_test = None

        self._environment_properties = {}

    @property
    def reports_dir(self):
        if not self._reports_dir:
            return TestSuiteSettings.REPORTS_DIR.replace("/", os.path.sep)
        return self._reports_dir

    def set_environment_properties(self, key, value=None):
        self._environment_properties[key] = value

    @property
    def environment_properties(self):
        lines = []
        for k, v in self._environment_properties.items():
            if v:
                lines.append(f"{k}={v}")
            else:
                lines.append(f"{k}")

        return ("environment.properties", lines)

    @property
    def executors(self):
        ips = [EnvironmentManager.get_ip()] + self.assistant_clients
        return RestRemLibClientsManager([(ip, EXECUTOR_PORT, "Executor") for ip in ips])

    @property
    def assistants_data(self):
        if self._assistants_data:
            return self._assistants_data
        else:
            assistants = self.test_suite.get_assistants()
            if not assistants:
                logger.info("Test suite {} doesn't have any assistant".format(self.test_suite))

            assert len(self.assistant_clients) >= len(assistants), (
                f"Count of clients {len(self.assistant_clients)} less then"
                f" count of assistants for test_suite {len(assistants)}"
            )

            return [(client, cls) for client, cls in zip(self.assistant_clients, assistants)]

    @assistants_data.setter
    def assistants_data(self, value):
        self._assistants_data = value

    @property
    def specific_test(self):
        return self._specific_test

    @specific_test.setter
    def specific_test(self, test_name):
        if not test_name:
            return
        self._specific_test = test_name

    @property
    def output_dir(self):
        return os.path.join(self.reports_dir, self.test_suite.relpath)

    @property
    def allure_report(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def _get_result(self):
        raise NotImplementedError

    def execute_in_subprocess(self, stop_event):
        """
        Запускает новый процесс, цель которого -- выполнить :func:`test_suite_run.run`. Поток,
        вызвавший настоящий метод, блокируется до завершения дочернего процесса.

        Здесь мы используем :func:`Popen.communicate` чтобы избежать переполнения stdout-буфера
        дочернего процесса (при переполнении, дочерний процесс приостанавливается).
        """
        return self.execute()
        # test_suite_subprocess = PipeCommunicatedPopen.from_obj_or_cls(self, "execute", stop_event=stop_event)
        # test_suite_subprocess.start_with_args()
        # subprocess_result = test_suite_subprocess.wait_subprocess_result()
        # self._subprocess_result = subprocess_result
        # if stop_event and stop_event.is_set():
        #     return subprocess_result

        # return subprocess_result

    @property
    def result(self):
        return self._get_result()

    def _result(self):
        """
        Абстрактный метод. Необходимо определить в производных классах.
        """
        raise NotImplementedError()

    def __repr__(self):
        if self.specific_test:
            return f'<TestSuite "{self.test_suite.relpath}#{self.specific_test}">'

        return f'<TestSuite "{self.test_suite.relpath}">'

    def _to_dict(self):
        return {
            "test_suite": self.test_suite,
            "test_suite_params": self.test_suite_params,
            "assistants_data": self._assistants_data,
            "file_senders": self.file_senders,
            "assistant_clients": self.assistant_clients,
        }

    @classmethod
    def _from_dict(cls, dict_):
        test_suite = dict_["test_suite"]
        test_suite_params = dict_["test_suite_params"]
        obj = cls(test_suite, test_suite_params)
        obj._assistants_data = dict_["assistants_data"]
        obj.file_senders = dict_["file_senders"]
        obj.assistant_clients = dict_["assistant_clients"]
        return obj


class PyTestSuiteRun(TestSuiteRunBase):
    ALLURE_DIR = "allure_report"

    @classmethod
    def from_fullname(cls, name, test_suite_params):
        from test_suite.test_suite import TestSuite

        package, test = name.split("#")
        path, classname = package.rsplit(".", 1)
        relpath = path.replace(".", "/")
        test_suite = TestSuite.from_relpath(relpath)
        tcr = test_suite.create_TestSuiteRun(test_suite_params)
        tcr.specific_test = test
        return tcr

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_name = self._get_full_name()
        self.class_name = self._get_class_name()

    def _get_class(self):
        classes = self.test_suite.classes
        # assert len(classes) == 1, f"TODO: case when len != 1; {len(classes)}\n{classes}"
        return classes.pop()

    def get_docstring(self):
        return self._get_class().docs

    def _get_class_name(self):
        return self._get_class().cls.__name__

    def _get_full_name(self):
        if self.specific_test:
            test_full_name = [
                f"{self.test_suite.package}.{test_class.cls.__name__}#{test}"
                for test_class in self.test_suite.classes
                for test in test_class.tests
                if test == self.specific_test
            ].pop()
        else:
            test_full_name = self.test_suite.package
        return test_full_name

    @staticmethod
    def categories():
        return (
            "categories.json",
            [
                {
                    "name": "Skipped product defects",
                    "matchedStatuses": ["skipped"],
                    "messageRegex": ".*(?:ACR|CLOUD|SALE|IPINT|INTL|DPE|SL).*",
                },
                {"name": "Skipped test defects", "matchedStatuses": ["skipped"], "messageRegex": ".*ROBO.*"},
                {"name": "Dumps in log", "messageRegex": ".*Dumps in logs:.*"},
                {"name": "Environment installation failed", "traceRegex": r".*\[WHEN\:INSTALL_ENVIRONMENT\].*"},
                {"name": "Setup failed", "traceRegex": r".*\[WHEN\:TEST_SETUP\].*"},
                {"name": "Execute failed", "traceRegex": r".*\[WHEN\:TEST_EXECUTE\].*"},
                {"name": "Teardown failed", "traceRegex": r".*\[WHEN\:TEST_TEARDOWN\].*"},
                {
                    "name": "Passed",
                    "matchedStatuses": ["passed"],
                },
            ],
        )

    def execute(self):
        if self.allure_report and not os.path.exists(self.allure_report):
            os.makedirs(self.allure_report)

        EnvironmentManager.delete_all_in_directory(self.allure_report)

        file_name, body = self.categories()
        dest = os.path.join(self.allure_report, file_name)
        if not os.path.exists(dest):
            with open(dest, "w") as f:
                f.write(json.dumps(body, indent=2))

        file_name, lines = self.environment_properties
        dest = os.path.join(self.allure_report, file_name)
        if not os.path.exists(dest):
            with open(dest, "w") as f:
                f.writelines(lines)

        r_code = start_pytest(self)
        logger.info("Exit code: {} type = {}".format(r_code, type(r_code)))
        return r_code

    def gen_report(self):
        EnvironmentManager.kill_process_tree_by_cmdline("io.qameta.allure.CommandLine")
        Popen(f"allure serve {self.allure_report}", stdout=PIPE, stderr=PIPE, shell=True, encoding="utf-8")

    def _get_result(self):
        # TODO: У PyTest много кодов возврата. И _не_ только нулевой говорит о том, что тест прошел успешно!
        if self._subprocess_result:
            if self._subprocess_result.result == 0:
                return SuiteResult.PASS
            return SuiteResult.FAIL
        else:
            return SuiteResult.NOT_RESULT

    @property
    def allure_report(self):
        allure_report = os.path.join(self.output_dir, PyTestSuiteRun.ALLURE_DIR)

        if self.specific_test:
            allure_report = os.path.join(allure_report, self.specific_test)

        try:
            if not os.path.exists(allure_report):
                os.makedirs(allure_report)
        except FileNotFoundError:
            raise Exception(
                f"Can't create folder {allure_report}. Maybe you need to set allure report path. \nPlease see {TestSuiteSettings}"
            )

        return allure_report


# class PlayWrightSuiteRun(TestSuiteRunBase):
#     ALLURE_DIR = "allure_report"
#     playwright_report_dir: str

#     def execute(self):
#         self.playwright_report_dir = os.path.join(self.output_dir, "playwright-report")
#         if self.allure_report and not os.path.exists(self.allure_report):
#             os.makedirs(self.allure_report)

#         EnvironmentManager.set_sys_env("PLAYWRIGHT_HTML_REPORT", self.playwright_report_dir)
#         EnvironmentManager.set_sys_env("ALLURE_RESULTS_DIR", self.allure_report)
#         EnvironmentManager.delete_all_in_directory(self.allure_report)
#         EnvironmentManager.delete_all_in_directory(self.playwright_report_dir)

#         file_name, lines = self.environment_properties
#         dest = os.path.join(self.allure_report, file_name)
#         if not os.path.exists(dest):
#             with open(dest, "w") as f:
#                 f.writelines(lines)

#         result = start_playwright(self)
#         # logger.info(result)
#         return PyTestReturnCodes.EXIT_OK  # пока так

#     def full_name(self):
#         return "test"  # TODO: ???

#     def gen_report(self):
#         EnvironmentManager.kill_process_tree_by_cmdline("io.qameta.allure.CommandLine")
#         Popen(
#             f"npx allure serve {self.allure_report}",
#             stdout=PIPE,
#             stderr=PIPE,
#             cwd=f"{self.test_suite.root_dir}",
#             shell=True,
#             encoding="utf-8",
#         )

#     def get_playwright_report(self):
#         Popen(
#             f"npx playwright show-report {self.playwright_report_dir}",
#             shell=True,
#             cwd=f"{self.test_suite.root_dir}",
#             stdout=PIPE,
#             encoding="utf-8",
#         )

#     def _get_result(self):
#         if self._subprocess_result:
#             if self._subprocess_result.result == 0:
#                 return SuiteResult.PASS
#             return SuiteResult.FAIL
#         else:
#             return SuiteResult.NOT_RESULT

#     @property
#     def allure_report(self):
#         allure_report = os.path.join(self.output_dir, PlayWrightSuiteRun.ALLURE_DIR)

#         if self.specific_test:
#             allure_report = os.path.join(allure_report, self.specific_test)

#         try:
#             if not os.path.exists(allure_report):
#                 os.makedirs(allure_report)
#         except FileNotFoundError:
#             raise Exception(
#                 f"Can't create folder {allure_report}. Maybe you need to set allure report path. \nPlease see {TestSuiteSettings.DEFAULT_FILE_PATTERN()}"
#             )

#         return allure_report
