import logging
import logging.config
import os


LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": (
                "%(asctime)s "
                "%(levelname)s "
                "%(name)s "
                "%(message)s"
            ),
        },
        "detailed": {
            "format": (
                "%(asctime)s "
                "%(levelname)s "
                "%(name)s "
                "%(filename)s:%(lineno)d "
                "%(message)s"
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": LOG_LEVEL,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}


def configure_logging() -> None:
    logging.config.dictConfig(
        LOGGING_CONFIG
    )