import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from app.utils.util import read_file

BASE_PATH = Path(__file__).resolve().parents[2]  # 파일 위치가 변경되면 확인 필요.

RESOURCES_PATH = BASE_PATH / "resources"
LOGS_PATH = BASE_PATH / "logs"

PROMPTS_PATH = RESOURCES_PATH / "prompts"
CHARACTER_PATH = PROMPTS_PATH / "character"


class Settings(BaseSettings):

    # DB & Redis
    database_url: str
    redis_host: str
    redis_port: int

    # llm api key
    google_api_key: str

    # log
    log_level: str


def _settings():

    load_dotenv(dotenv_path=BASE_PATH / ".env", override=True)

    env = os.getenv("APP_ENV")
    if env:
        load_dotenv(dotenv_path=BASE_PATH / f".env.{env}", override=True)

    return Settings()


settings = _settings()

BASE = read_file(CHARACTER_PATH / "base.txt")
SEARCH = read_file(CHARACTER_PATH / "search.txt")
FRIENDLY = read_file(CHARACTER_PATH / "friendly.txt")
FAMILY = read_file(CHARACTER_PATH / "family.txt")