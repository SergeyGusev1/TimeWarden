from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool = False
    DATABASE_URL: str = 'sqlite:///./timewarden.db'

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
