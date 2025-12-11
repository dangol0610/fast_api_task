from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="alchemytask_db")
    POSTGRES_HOST: str = Field(default="postgres")
    POSTGRES_PORT: int = Field(default=5432)

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
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

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
