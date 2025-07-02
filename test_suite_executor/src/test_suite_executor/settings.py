from pydantic_settings import BaseSettings, SettingsConfigDict


class ExecutorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ExecutorSettings__",
        env_nested_delimiter="__",
    )

    port: int = 8888
