from pydantic import BaseModel, Field
from test_suite.pytest import PyTestSuite


class SuiteRequest(BaseModel):
    repo_url: str = Field(
        title="Repository URL",
        description="ssh ссылка на репозиторий",
        examples=[
            "ssh://git@src.axxonsoft.dev/qa/axxonnext_detectorpack_autotests.git",
            "ssh://git@src.axxonsoft.dev/qa/axxonnext_autotests_git.git",
        ],
    )
    branch: str = Field(
        title="Название ветки",
        description="Указывается название ветки на которой будут запущены автотесты",
        examples=["major", "minor", "prestable", "stable"],
    )
    suite: PyTestSuite
