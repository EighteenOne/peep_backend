import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DEBUG: Optional[bool] = os.getenv("DEBUG") == "True"

    TITLE: str = "Peep"

    ORIGINS: Optional[str] = os.getenv("ORIGINS")

    MYSQL_CONNECTION_STRING: str = os.getenv("MYSQL_CONNECTION_STRING")

    API_KEY: str = os.getenv("API_KEY")

    YANDEX_DISK_TOKEN: str = os.getenv("YANDEX_DISK_TOKEN")

    FROM_MAIL: str = os.getenv("FROM_MAIL")
    FROM_PASSWD: str = os.getenv("FROM_PASSWD")
    SERVER_ADR: str = os.getenv("SERVER_ADR")

    SENTRY_DSN: str = os.getenv("SENTRY_DSN")

    BOT_TOKEN: str = os.getenv("BOT_TOKEN")


settings = Settings()
