import os
import re
import traceback
from copy import deepcopy

from logging_lib import RootLogger as logger
from platform_helpers import path_rel2abs
from serialize import SerializableMetaclass

from test_suite import TestSuite

from .test_suite_run import PyTestSuiteRun


class TestSuiteRunCollector(metaclass=SerializableMetaclass):
    @staticmethod
    def _get_suite_runs(test_suite_params, src, by_tests):
        test_suite_runs = []
        errors = []
        for test_dir in src:
            if re.match(r"(.+\..+)+#.+", test_dir):
                test_suite_runs.append(PyTestSuiteRun.from_fullname(test_dir, test_suite_params))
            else:
                for root, d_names, f_names in os.walk(path_rel2abs(test_dir)):
                    suite = TestSuite.from_abspath(root)
                    d_names.sort()

                    if not d_names or "__pycache__" in d_names:  # TODO: ???
                        if "test.py" in f_names:
                            try:
                                if (
                                    suite.is_pytest_package
                                ):  # TODO and OSTypes(test_suite_params["os_type"]) in suite.get_os_types():
                                    test_suite_run = suite.create_TestSuiteRun(test_suite_params)
                                    if by_tests:
                                        for test in [
                                            test for cls in test_suite_run.test_suite.classes for test in cls.tests
                                        ]:
                                            test_suite_run = deepcopy(test_suite_run)
                                            test_suite_run.specific_test = test
                                            test_suite_runs.append(test_suite_run)
                                    else:
                                        test_suite_runs.append(test_suite_run)

                            except Exception as ex:
                                logger.info(f"Test: {root} has problem")
                                logger.error(ex)
                                errors.append(f"Test: {root} has problem\n{root}\n{traceback.format_exc()}\n\n")

                        elif any([".spec.ts" in name for name in f_names]):
                            suite = TestSuite.from_abspath(root)
                            if suite.is_playwright_package:
                                test_suite_run = suite.create_TestSuiteRun(test_suite_params)
                                if by_tests:
                                    for test in [file_name for file_name in f_names if file_name.endswith(".spec.ts")]:
                                        test_suite_run = deepcopy(test_suite_run)
                                        test_suite_run.specific_test = test
                                        test_suite_runs.append(test_suite_run)
                                else:
                                    test_suite_runs.append(test_suite_run)
                    # else:
                    #     for name in f_names:
                    #         suite = TestSuite.from_abspath(os.path.join(root, name))
                    #         if suite.is_pytest_file:
                    #             test_suite_run = suite.create_TestSuiteRun(test_suite_params)
                    #             test_suite_runs.append(test_suite_run)

        # if not test_suite_runs:
        #     raise Exception("There are no test_suites")

        return sorted(test_suite_runs, key=lambda x: len(x.test_suite.get_assistants())), errors

    def _collect_test_suite_runs(self, test_suite_params, src, by_tests):
        # p = PipeCommunicatedPopen.from_obj_or_cls(TestSuiteRunCollector, "_get_suite_runs")
        # p.start_with_args(run_tests_container, src)
        # return p.wait_subprocess_result().result
        return TestSuiteRunCollector._get_suite_runs(test_suite_params, src, by_tests)

    def get_suite_runs(self, test_suite_params, src, by_tests):
        return self._collect_test_suite_runs(test_suite_params, src, by_tests)
