from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="user")
    DB_PASS: str = Field(default="password")
    DB_NAME: str = Field(default="database")

    SECRET_KEY: str = Field(default="")
    ALG: str = "HS256"

    model_config = SettingsConfigDict(env_file="task/.env")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
