import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


def _get_robo_dir():
    if os.name == "nt":
        return Path("C:/ROBO")
    elif os.name == "posix":
        return Path("/mnt/ROBO")
    else:
        raise Exception("Unknown OS")


class TestSuiteSettings(BaseSettings):
    ROBO_DIR: Path = Field(default_factory=_get_robo_dir)
    REMOTE_SERVERS: list[str] = Field(
        default=[
            "192.168.13.47",
            "192.168.120.120",
            "192.168.116.1",
            "192.168.116.2",
        ]
    )

    @property
    def REPORTS_DIR(self):
        return self.ROBO_DIR.joinpath("Reports")


class ExecutorSettings(BaseSettings):
    port: int = 8998
