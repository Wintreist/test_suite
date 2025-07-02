from pydantic import BaseModel


class TestSuiteParams(BaseModel):
    """
    У параметров ДОЛЖНО быть дефолтное значение
    Можно передавать что-то пустое, но TestSuiteParams не должен падать если его создать без передачи параметров
    """

    pass
