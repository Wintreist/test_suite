from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import BaseModel
from pytest import ExitCode

from test_suite.base.test_suite import TestSuite
from test_suite.pytest.params import PyTestSuiteParams


class PyTestSuite(TestSuite):
    """
    :param str name: Текст, который будет передан в pytest как путь к тесту(-ам)
    :param PyTestSuiteParams params: Параметры которые будут переданы в pytest cli как параметры теста
    """

    # Параметры, которые нужны до запуска
    name: str
    params: PyTestSuiteParams
    print_output: bool = True
    # Параметры, которые можно использовать после запуска
    result_code: ExitCode | int | None = None

    def run(self):
        self.result_code = pytest.main([self.name, *self.pytest_cli_params])

    @property
    def pytest_cli_params(self):
        result = []
        # Вывод логов в консоль
        if self.print_output:
            result.append("--capture=no")
            result.append("--log-level=NOTSET")

        # Добавление параметров теста
        for key in self.params.model_fields_set:
            value = getattr(self.params, key)
            if value is None:
                continue
            result.append(f"--{key}")
            if isinstance(value, bool):
                continue
            elif isinstance(value, str | int | float):
                result.append(value)
            elif isinstance(value, Path):
                result.append(value.as_posix())
            elif isinstance(value, list):
                result.extend(value)
            elif isinstance(value, BaseModel):
                result.append(value.model_dump_json())

        return result
