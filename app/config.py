from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 8000
    cors_allowed_origins: str = "*"
    environment: str = "development"
    model_path: str = "models/model_quantized.onnx"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
