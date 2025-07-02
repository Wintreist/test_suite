# -*- coding: utf-8 -*-
from enum import IntEnum, StrEnum


class TestSuiteType(StrEnum):
    ROBOT = "robot"
    PYTEST = "py"
    GO = "go"
    PLAYWRIGHT = "ts"


class SuiteResult(StrEnum):
    FAIL = "FAIL"
    PASS = "PASS"
    NOT_RESULT = "NOT RESULT"


class PyTestReturnCodes(IntEnum):
    EXIT_OK = 0
    EXIT_TESTSFAILED = 1
    EXIT_INTERRUPTED = 2
    EXIT_INTERNALERROR = 3
    EXIT_USAGEERROR = 4
    EXIT_NOTESTSCOLLECTED = 5
    EXIT_CUSTOM = -1
