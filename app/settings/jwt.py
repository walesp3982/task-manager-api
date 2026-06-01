from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    SECRET: str = Field(min_length=32, default="")

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        env_file=".env",
        extra="ignore",
    )
