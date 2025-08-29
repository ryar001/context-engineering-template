from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BINANCE_API_KEY: str
    BINANCE_API_SECRET: str
    GEMINI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings() # type: ignore