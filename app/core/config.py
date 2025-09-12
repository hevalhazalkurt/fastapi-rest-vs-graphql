from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    POOL_SIZE: int | None = None
    ECHO: bool | None = None
    MAX_OVERFLOW: int | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
