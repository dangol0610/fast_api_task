from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="user")
    DB_PASS: str = Field(default="password")
    DB_NAME: str = Field(default="database")

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_BROKER_DB: int = Field(default=0)
    REDIS_RESULT_DB: int = Field(default=1)
    REDIS_CACHE_DB: int = Field(default=2)

    REDIS_PASSWORD: str = Field(default="")

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: EmailStr
    SMTP_FROM: EmailStr
    GMAIL_PASS: str
    MESSAGE: str

    TESTING: bool = False

    SECRET_KEY: str = Field(default="")
    ALG: str = "HS256"

    model_config = SettingsConfigDict(env_file="task/.env")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def redis_cache_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_CACHE_DB}"

    @property
    def redis_broker_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_BROKER_DB}"

    @property
    def redis_result_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_RESULT_DB}"


settings = Settings()
