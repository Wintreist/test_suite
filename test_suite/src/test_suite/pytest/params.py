from pathlib import Path

from pydantic import Field
from robo_settings import ROBOSettings

from test_suite.base.params import TestSuiteParams

robo_settings = ROBOSettings()  # type: ignore


class PyTestSuiteParams(TestSuiteParams):
    """
    У параметров ДОЛЖНО быть дефолтное значение
    Можно передавать что-то пустое, но PyTestSuiteParams не должен падать если его создать без передачи параметров
    """

    alluredir: Path = Field(default=robo_settings.ROBO_DIR.joinpath("allure", "reports"))
    pass


"""
# conftest.py
import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--screen_record", type=bool)


@pytest.fixture
def screen_record(request: pytest.FixtureRequest):
    result: bool = request.config.getoption("--screen_record")
    return result

# params.py
class PyTestSuiteParams(BaseModel):
    screen_record: bool = True
    pass
"""
