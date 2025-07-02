from __future__ import annotations

from abc import abstractmethod

from pydantic import BaseModel

from test_suite.base.params import TestSuiteParams


class TestSuite(BaseModel):
    # Параметры, которые нужны до запуска
    name: str
    params: TestSuiteParams
    # Параметры, которые можно использовать после запуска
    result_code: int | None = None

    @abstractmethod
    def run(self): ...
