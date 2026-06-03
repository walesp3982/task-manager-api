from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    NAME: str = "Task_Manager_API"
    """
    Value in minutes
    Default 3 days
    """
    TIME_USER_SESSION: int = 4320
    """
    Value in minutes
    Default 10 minutes
    """
    TIME_USER_TOKEN: int = 10

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",
    )
