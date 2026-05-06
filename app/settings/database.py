from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    user: str
    host: str
    port: int
    password: str
    name: str

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")
