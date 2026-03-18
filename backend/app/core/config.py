from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = 'TimeWarden'
    DEBUG: bool = False
    DATABASE_URL: str = 'sqlite:///./timewarden.db'

    CORS_ORIGINS: list[str] = ['http://localhost:3000']

    TELEGRAM_BOT_TOKEN: str = ''
    TELEGRAM_CHAT_ID: str = ''

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
