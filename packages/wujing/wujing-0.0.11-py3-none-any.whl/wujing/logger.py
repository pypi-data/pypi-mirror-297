import sys
from threading import Lock
from typing import Literal

from loguru import logger
from pydantic import BaseModel, constr, ConfigDict, field_validator


# Define a model for logging configuration
class LoggingConfig(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    log_file_name: constr(min_length=1)
    level: Literal['DEBUG', 'INFO', 'TRACE', 'WARNING', 'ERROR'] = "DEBUG"
    console: bool = False

    @field_validator('log_file_name', mode='before')
    def validate_log_file_name(cls, v):
        if not v:
            raise ValueError('log_file_name cannot be None or empty')
        return v


# Global variable to track configuration status and lock
logging_configured = False
lock = Lock()


def configure_loguru(config: LoggingConfig):
    global logging_configured

    if logging_configured:
        return

    with lock:
        if logging_configured:
            return

        try:
            logger.remove()
            _add_console_output(config.console, config.level)
            _add_file_output(config.log_file_name, config.level)

            logging_configured = True
        except Exception as e:
            logger.error(f"Failed to configure logging: {e}")


def _add_console_output(console: bool, level: str):
    if console:
        logger.add(
            sys.stdout,
            format="{time} {level} {message}",
            level=level,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )


def _add_file_output(log_file_name: str, level: str):
    logger.add(
        log_file_name,
        rotation="100MB",
        format="{time} {level} {message}",
        level=level,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        serialize=True,
    )


if __name__ == '__main__':
    # Example usage
    try:
        config = LoggingConfig(log_file_name="app.log", level="DEBUG", console=True)
        configure_loguru(config)
    except ValueError as e:
        print(f"Configuration error: {e}")

    logger.info("555", extra={"sid": "xxx"})
