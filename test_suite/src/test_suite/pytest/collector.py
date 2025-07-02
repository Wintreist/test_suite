import re
from enum import IntEnum
from pathlib import Path

import pytest

from test_suite.pytest.params import PyTestSuiteParams
from test_suite.pytest.suite import PyTestSuite


class SplitMethod(IntEnum):
    MODULE = 0
    CLASS = 1
    FUNCTION = 2
    PARAMS = 3
    """
    Указывается тип, по которому будут тесты делиться. Например
        tests/test_.py::TestClass::test_st[abacoo-gogbkk]
        tests/test_.py::TestClass::test_st[gogbkk-abacoo]
        tests/test_.py::TestClass::test_st[baa-dcc]
        tests/test_.py::TestClass::test_st[aab-ccd]
        tests/test_.py::TestClass::test_st[a-c]
        tests/test_.py::TestClass::test_st[-]
        tests/test_.py::TestClass::test_another_one
        tests/test_.py::test_is_palindrome_permutation[cabab]
        tests/test_.py::test_is_palindrome_permutation[hello]

        * SplitMethod.PARAMS - Разделит параметризированные тесты друг от друга (Так как выше)
        * SplitMethod.FUNCTION - Разделит только по функциям:
            tests/test_.py::TestClass::test_st
            tests/test_.py::TestClass::test_another_one
            tests/test_.py::test_is_palindrome_permutation
        * SplitMethod.CLASS - Разделит по классам и функциям, если у тех нет класса:
            tests/test_.py::TestClass
            tests/test_.py::test_is_palindrome_permutation
        * SplitMethod.MODULE - Разделит только по файлам, в которых находятся тесты:
            tests/test_.py
    """


class PyTestSuiteCollector:
    creating_class = PyTestSuite

    def __init__(
        self,
        directory: Path | str,
        shared_params: PyTestSuiteParams | None = None,
        split_method: SplitMethod = SplitMethod.FUNCTION,
    ):
        if not isinstance(directory, Path):
            directory = Path(directory)
        assert directory.exists(), "Указанная директория не найдена"
        if shared_params is None:
            shared_params = PyTestSuiteParams()

        self.directory = directory
        self.shared_params = shared_params
        self.split_method = split_method

    def get_suite_runs(self):
        split_plugin = self.SplitCollectPlugin(self.split_method)
        pytest.main(
            ["--collect-only", str(self.directory)],
            plugins=[split_plugin],
        )
        return [
            self.creating_class(
                name=test_name,
                params=self.shared_params,
            )
            for test_name in split_plugin.items
        ]

    class SplitCollectPlugin:
        func_pattern = re.compile(pattern=r"(.*)\[.*\]")
        class_pattern = re.compile(pattern=r"(.*::.*)::.*")
        module_pattern = re.compile(pattern=r"(.*)::.*")

        def __init__(self, split_method: SplitMethod):
            self.split_method = split_method

        def pytest_collection_modifyitems(self, items: list[pytest.Function]):
            seen = set()

            for item in items:
                nodeid = item.nodeid
                if self.split_method == SplitMethod.PARAMS:
                    key = nodeid
                elif self.split_method == SplitMethod.FUNCTION:
                    key = self.split_to_func(nodeid)
                elif self.split_method == SplitMethod.CLASS:
                    key = self.split_to_class(nodeid)
                elif self.split_method == SplitMethod.MODULE:
                    key = self.split_to_module(nodeid)

                if key not in seen:
                    seen.add(key)

            self.items = list(seen)

        def split_to_func(self, name: str):
            result = self.func_pattern.search(name)
            if result is None:
                # Означает, что у функции нет параметризации
                return name
            return str(result.group(1))

        def split_to_class(self, name: str):
            name = self.split_to_func(name)

            result = self.class_pattern.search(name)
            if result is None:
                # Означает, что у функции нет класса
                return name
            return str(result.group(1))

        def split_to_module(self, name: str):
            origin_name = name
            name = self.split_to_class(name)

            result = self.module_pattern.search(name)
            if result is None:
                raise Exception(
                    f"По какой-то причине, имя теста ({origin_name}) не подходит под pattern. Обратитесь к разработчику."
                )
            return str(result.group(1))
