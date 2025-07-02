from typing import List

from .constants import TestSuiteType


class RequiredParam:
    def __init__(self, name, param_type, default, descrption):
        self.name = name
        self.param_type = param_type
        self.default = default
        self.descrption = descrption


class RequiredTestParams:
    def __init__(self):
        self.d: List[RequiredParam] = []

    def add(self, param: RequiredParam):
        # if len(args) == 1:
        #    assert isinstance(args[0], Param), args
        self.d.append(param)


class TestSuiteConfig:
    def __init__(self, **kwargs):
        self.supported_os = kwargs.pop("supported_os")
        self.type = kwargs.pop("type", TestSuiteType.PYTEST)
        self._required_params = kwargs.pop("required_params", RequiredTestParams())

    @property
    def required_params(self) -> List[RequiredParam]:
        return self._required_params.d

    @required_params.setter
    def required_params(self, value: RequiredTestParams):
        self._required_params = value
