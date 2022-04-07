from typing import Tuple
from pydantic import AnyHttpUrl
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

# App configurations
DEBUG = env("DEBUG", bool, False)
APP_NAME = env("APP_NAME")
SECRET_KEY = env("SECRET_KEY")
VERSION = env("VERSION", default=1)

# CORS
CORS_ORIGIN_WHITELIST: Tuple[AnyHttpUrl] = env(
    "CORS_ORIGIN_WHITELIST",
    lambda v: tuple(s.strip() for s in v.split(",")) if v else tuple(""),
    default=(),
)
CORS_ALLOW_METHODS: Tuple[str] = env(
    "CORS_ALLOW_METHODS",
    lambda v: tuple(s.strip() for s in v.split(",")) if v else tuple(""),
    default=("OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"),
)

# Token
TOKEN_ALGORITHM = env("TOKEN_ALGORITHM", default="HS256")
TOKEN_EXPIRE_MINUTES = env("TOKEN_EXPIRE_MINUTES", cast=int, default=30)

# Database configurations
DATABASE_HOST = env("DATABASE_HOST")
DATABASE_USER = env("DATABASE_USER")
DATABASE_PASSWORD = env("DATABASE_PASSWORD")
DATABASE_NAME = env("DATABASE_NAME")
SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://{}:{}@{}/{}".format(
    DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME
)

# Logging configurations
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "[%(levelname)s][%(asctime)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        }
    },
    "loggers": {
        "fastapi": {
            "handlers": ["default"],
            "level": env("LOGGING_LEVEL", default="DEBUG"),
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["default"],
            "level": env("DATABASE_LOG_LEVEL", default="WARN"),
        },
    },
}
