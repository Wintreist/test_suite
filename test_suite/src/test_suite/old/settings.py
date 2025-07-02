import os

from ecosystem_settings import EcosystemSettings
from py_axxonsoft import AxxonSoftSettings
from vm_hub.conf import EXECUTOR_PORT  # noqa: F401


class TestSuiteSettings(EcosystemSettings):
    ROOT_DIR = os.path.dirname(__file__)
    GLOBAL_VARIABLES = {
        "ROBO_DIR": AxxonSoftSettings.ROBO_DIR,
    }
