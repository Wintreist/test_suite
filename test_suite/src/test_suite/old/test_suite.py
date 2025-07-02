# -*- coding: utf-8 -*-
import inspect
import os

from logging_lib import RootLogger as logger
from platform_helpers.import_helpers import import_from_module, import_module
from platform_helpers.path_helpers import base_of_path, path_abs2rel, path_rel2abs
from serialize import SerializableMetaclass

from test_suite.constants import TestSuiteType
from test_suite.test_suite_config import TestSuiteConfig
from test_suite.test_suite_params import TestSuiteParams
from test_suite.test_suite_run import PyTestSuiteRun

TEST_MODULE_NAME = "test"
TEST_FILE_NAME = "test.py"
TEST_CLASS_PREFIX = "Test"
TEST_PREFIX = "test_"


class TestClass:
    def __init__(self, cls):
        self.cls = cls

    @property
    def docs(self):
        return {
            "class": {self.cls.__name__: self.cls.__doc__.strip() if self.cls.__doc__ is not None else ""},
            "methods": {
                method.__name__: method.__doc__.strip() if method.__doc__ is not None else "" for method in self.test_methods
            },
        }

    @property
    def test_methods(self):
        return [
            test for name, test in inspect.getmembers(self.cls, predicate=inspect.isfunction) if name.startswith("test_")
        ]

    @property
    def tests(self):
        return [name for name, _ in inspect.getmembers(self.cls, predicate=inspect.isfunction) if name.startswith("test_")]


class TestSuite(metaclass=SerializableMetaclass):
    def __init__(self):
        """
        :param str abspath: Абсолютный путь к тест-кейсу на текущем компютере. Немеденно транфоррмируется
                            в относительный для внутренного хранения. Базовый путь.
        """
        self.paths = []
        self._dependency = None
        self._module = None
        self._type = None
        self._os_types = []

    @property
    def test_module(self):
        return os.path.join(self.abspath, TEST_FILE_NAME)

    @property
    def classes(self):
        module = import_module(f"{self.rel_import_path}.{TEST_MODULE_NAME}")
        return [
            TestClass(cls)
            for name, cls in inspect.getmembers(module, predicate=inspect.isclass)
            if name.lower().startswith(TEST_MODULE_NAME)
        ]

    @property
    def root_dir(self):
        return base_of_path(self.abspath)

    @property
    def package(self):
        return self.rel_import_path

    @property
    def parent_suite(self):
        return self.rel_import_path.rsplit(".", 1)[0]

    @property
    def suite(self):
        return self.rel_import_path.rsplit(".", 1)[1]

    @classmethod
    def from_relpath(cls, relpath):
        logger.debug(f"from_relpath relpath: {relpath}")
        obj = cls()
        obj.paths = os.path.relpath(relpath).split(os.sep)
        logger.debug(f"from_relpath obj.paths: {obj.paths}")
        return obj

    @classmethod
    def from_abspath(cls, abspath):
        logger.debug(f"from_abspath abspath: {abspath}")
        obj = cls()
        obj.paths = path_abs2rel(abspath).split(os.sep)
        logger.debug(f"from_abspath obj.paths: {obj.paths}")
        return obj

    @property
    def relpath(self):
        return os.path.join(*self.paths)

    @property
    def abspath(self):
        """
        Абсолютный путь к тест-кейсу на данном компьюетре.
        """
        logger.debug(f"paths: {self.paths}")
        return path_rel2abs(os.path.join(*self.paths))

    @property
    def rel_import_path(self):
        return self.relpath.replace(os.sep, ".")

    @property
    def suite_file_name(self):
        """
        :return: Название файла с тест-кейсом
        """
        return os.path.basename(self.abspath)

    @property
    def display_name(self):
        """
        Только для отображения на экране. Идетнтификация происходить по `relpath`. Можно позднее
        переделать этот метод.
        """
        return self.suite_file_name

    def robot_to_py(self):
        """
        Меняет в пути файла расширение 'robot' на 'py'. Относитлеьный или обсолютный путь -- не важно.
        """
        robot_path = os.path.normpath(self.abspath)
        (path, robot_name) = os.path.split(robot_path)
        py_name = robot_name.replace(".robot", ".py")
        return os.path.join(path, py_name)

    def split_py_path(self):
        """
        Получаем из пути к py-файлу путь к его директории и имя файла как модуля -- без расширения.
        Относитлеьный или обсолютный путь -- не важно.
        """
        py_path = os.path.normpath(self.py_path)
        py_dir, py_name = os.path.split(py_path)
        return py_dir, py_name.split(".")[0]

    @property
    def py_path(self):
        if self.is_robot:
            assert os.path.exists(self.robot_to_py()), "Robot file {} doesn't has py file ".format(self.abspath)
            return self.robot_to_py()
        elif self.is_pytest:
            return self.abspath
        elif self.is_go:
            raise NotImplementedError()
        else:
            raise NotImplementedError()

    @property
    def is_pytest(self):
        return self.is_pytest_file or self.is_pytest_package

    @property
    def is_pytest_package(self):
        return os.path.isdir(self.abspath)

    @property
    def is_pytest_file(self):
        return self.abspath.endswith(".py") and os.path.isfile(self.abspath) and not self.abspath.endswith("__init__.py")

    @property
    def is_pytest_report(self):
        return self.abspath.endswith(".py") and os.path.isdir(self.abspath)

    @property
    def is_robot(self):
        return self.abspath.endswith(".robot") and (os.path.isfile(self.abspath) or os.path.isdir(self.abspath))

    @property
    def is_go(self):
        return self.abspath.endswith(".go") and (os.path.isfile(self.abspath))

    @property
    def is_playwright(self):
        return self.is_playwright_file or self.is_playwright_package

    @property
    def is_playwright_package(self):
        if os.path.isdir(self.abspath):
            for filename in os.listdir(self.abspath):
                if filename.endswith(".spec.ts"):
                    return True

    @property
    def is_playwright_file(self):
        return self.abspath.endswith(".ts") and (os.path.isfile(self.abspath))

    @property
    def suite_type(self):
        if self.is_pytest:
            return TestSuiteType.PYTEST
        elif self.is_robot:
            return TestSuiteType.ROBOT
        elif self.is_go:
            return TestSuiteType.GO
        elif self.is_playwright:
            return TestSuiteType.PLAYWRIGHT
        else:
            raise NotImplementedError("Unknown suite type {}".format(self.abspath))

    def create_TestSuiteRun(self, test_suite_params):
        if self.is_pytest:
            return PyTestSuiteRun(self, test_suite_params)
        # elif self.is_playwright:
        #     return PlayWrightSuiteRun(self, test_suite_params)

        else:
            raise (Exception("Unknown suite type {}".format(self.abspath)))

    @property
    def is_suitable_robot_file(self):
        return (
            "__init__" not in self.abspath
            and "Resource" not in self.abspath
            and "Helper" not in self.abspath
            and self.is_robot
        )

    @property
    def is_suitable_pytest_file(self):
        return self.is_pytest and not os.path.exists(self.abspath.replace(".py", ".robot"))

    def get_assistants(self):
        """ "
        TODO: change to property
        """
        return self._get_attr_from_module(self.rel_import_path, "ASSISTANTS") or []

    @property
    def test_suite_params(self):
        params = self._get_attr_from_module(self.rel_import_path, "TEST_SUITE_PARAMS") or {}
        return TestSuiteParams(**params)

    @property
    def config(self) -> TestSuiteConfig:
        return self._get_attr_from_module(self.rel_import_path, "CONFIG") or None

    def _get_assistants_in_subprocess(self, stop_event=None):
        """
        Запускает новый процесс, цель которого -- выполнить :func:`_get_assistants`.
        Здесь мы используем :func:`Popen.communicate`, чтобы не импортировать файл тест-кейса в
        текущий процесс интерпретатора Python.
        """
        return self.get_assistants()

    @staticmethod
    def _get_attr_from_module(module_path, attr_name):
        try:
            attr = import_from_module(module_path, attr_name)
            # logger.info(f'Module path = {module_path}\n{attr_name} = {attr}')
            return attr
        except ImportError as ex:
            if f"no attribute '{attr_name}" not in ex.msg:
                logger.exception(f"{type(ex)} {ex}")
                raise
            # logger.debug(f"Can't find attribute {attr_name}. If test doesn't has the attribute, it's correct!")
            return None

    def _to_dict(self):
        return {
            "relpath": self.relpath,
            "type": self._type,
            "os_types": self._os_types,
        }

    @classmethod
    def _from_dict(cls, dict_):
        obj = cls.from_relpath(dict_["relpath"])
        obj._type = dict_["type"]
        obj._os_types = dict_["os_types"]
        return obj

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<TestSuite [{}]>".format(self.relpath)
