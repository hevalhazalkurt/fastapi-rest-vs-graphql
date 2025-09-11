from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    POOL_SIZE:int
    ECHO: bool
    MAX_OVERFLOW:int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
