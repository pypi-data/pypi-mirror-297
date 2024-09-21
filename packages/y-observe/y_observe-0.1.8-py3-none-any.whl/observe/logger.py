import json
import logging
import os
import sys
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

from loguru import logger
from opentelemetry.trace import get_current_span

DEFAULT_OVERWRITE_LOGGERS = [
    "uvicorn.access",
    "uvicorn",
    "uvicorn.error",
    "fastapi",
    "gunicorn.access",
    "gunicorn",
    "gunicorn.error",
    "flask",
]
DEFAULT_LEVEL = "debug"
DEFAULT_RETENTION = "1 months"
DEFAULT_ROTATION = "20 days"
DEFAULT_FORMAT = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> extras={extra}"


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except (AttributeError, ValueError) as e:
            try:
                level = self.loglevel_mapping[record.levelno]
            except KeyError:
                get_logger().debug(
                    "Lost logger", message=record.getMessage(), record=record
                )
                return

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # log = logger.bind(trace_id="app")
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class Logger:
    @classmethod
    def make_logger(
        cls,
        config_path: Path = None,
        path=None,
        level="debug",
        retention="1 months",
        rotation="20 days",
        format_=DEFAULT_FORMAT,
    ):
        if config_path is not None:
            config = cls.load_logging_config(config_path)
            logging_config = config.get("logger")

            return cls.customize_logging(
                logging_config.get("path"),
                level=logging_config.get("level"),
                retention=logging_config.get("retention"),
                rotation=logging_config.get("rotation"),
                format_=logging_config.get("format"),
            )

        return cls.customize_logging(
            filepath=path,
            level=level,
            retention=retention,
            rotation=rotation,
            format_=format_,
        )

    @classmethod
    def customize_logging(
        cls,
        filepath: Path | None,
        level: str,
        rotation: str,
        retention: str,
        format_: str,
    ):
        if filepath is not None:
            os.makedirs(filepath.parent, exist_ok=True)

        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format_,
        )
        if filepath is not None:
            logger.add(
                filepath,
                rotation=rotation,
                retention=retention,
                enqueue=True,
                backtrace=True,
                level=level.upper(),
                format=format_,
            )
        return logger.bind()

    @classmethod
    def load_logging_config(cls, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config


@lru_cache()
def get_logger():
    config_path = os.environ.get("LOG_CONFIG")
    if config_path is not None:
        return Logger.make_logger(config_path=Path(config_path))

    return Logger.make_logger(
        path=Path(os.environ.get("LOG_PATH")) if os.environ.get("LOG_PATH") else None,
        level=os.environ.get("LOG_LEVEL", DEFAULT_LEVEL),
        retention=os.environ.get("LOG_RETENTION", DEFAULT_RETENTION),
        rotation=os.environ.get("LOG_ROTATION", DEFAULT_ROTATION),
        format_=os.environ.get("LOG_FORMAT", DEFAULT_FORMAT),
    )


def init_loggers(overwrite_loggers: list[str] = None):
    # create logger to setup customisations
    _ = get_logger()

    # root logger
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    # additional packages loggers that need to be overwritten
    if overwrite_loggers is None:
        overwrite_loggers = []

    for _log in overwrite_loggers:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]
    return


@contextmanager
def get_context_logger():
    log = get_logger()
    context = get_current_span().get_span_context()
    log = log.bind(trace_id=context.trace_id, span_id=context.span_id)
    try:
        yield log
    finally:
        pass


__all__ = [
    "get_logger",
    "get_context_logger",
    "init_loggers",
    "DEFAULT_OVERWRITE_LOGGERS",
    "DEFAULT_FORMAT",
]
