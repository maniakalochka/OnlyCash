from pathlib import Path
from typing import Any, Literal, Optional

from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # --- Application settings --- #
    APP_NAME: str = "OnlyCash"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # --- Database settings --- #
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_URL: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def set_db_url(cls, values) -> Any:
        values["DB_URL"] = (
            f"postgresql://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        )
        return values

    model_config = {
        "env_file": env_path,
        "validate_default": True,
    }


settings = Settings()  # type: ignore
