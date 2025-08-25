import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.config.default import LOGS_PATH, settings

DEFAULT_LOG_FORMAT = "%(asctime)s #%(process)d %(name)s \t %(filename)s(%(lineno)s) \t %(levelname)s - %(message)s"

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
DEFAULT_LOG_LEVEL = LOG_LEVELS[settings.log_level.lower()]


def set_stream_handler(
    logger: logging.Logger,
    stream_format: str = DEFAULT_LOG_FORMAT,
):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(stream_format))
    logger.addHandler(stream_handler)

    return None


def _mkdir_log_path(log_path: str | Path):
    if not log_path:
        log_path = LOGS_PATH / "py.log"

    log_path = Path(log_path)
    # 경로상에 dir가 없을 경우, dir 생성
    log_path.parent.mkdir(parents=True, exist_ok=True)

    return log_path


def set_file_handler(
    logger: logging.Logger,
    log_path: str | Path = None,
    log_format: str = DEFAULT_LOG_FORMAT,
):
    log_path = _mkdir_log_path(log_path)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    return None


def set_timed_rotating_file_handler(
    logger: logging.Logger,
    log_path: str | Path,
    log_format: str = DEFAULT_LOG_FORMAT,
    when: str = "h",
    interval: int = 1,
    backup_count: int = 0,
):
    log_path = _mkdir_log_path(log_path)

    file_handler = TimedRotatingFileHandler(
        log_path,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    return None

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(DEFAULT_LOG_LEVEL)

    set_stream_handler(logger, DEFAULT_LOG_FORMAT)
    set_timed_rotating_file_handler(
        logger, LOGS_PATH / "py.log", DEFAULT_LOG_FORMAT, "W0", 1
    )

def suppress_external_loggers():
    # 외부 라이브러리 로그 레벨 설정
    logging.getLogger("google_genai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)