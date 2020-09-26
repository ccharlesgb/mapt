import logging
import os
from typing import Any, Dict, List, Type, Union

from pydantic import BaseSettings, validator

_env_prefix = "mapt_"


class Config(BaseSettings):
    app_env: str
    root_log_level: int = logging.DEBUG

    title: str = "Mapt"
    description: str = "Shape file uploader/sharing application"

    @validator("root_log_level")
    def is_logging_level(
        cls, v: Union[str, int], values: List[str], **kwargs: Dict[str, Any]
    ) -> int:
        # Weird function it returns the integer repr if it is valid.
        # If you supply it a valid integer like logging.DEBUG it returns the string "DEBUG"
        # Otherwise it returns f"Level {v}" if it isn't valid
        level = logging.getLevelName(v)
        if isinstance(level, int):
            return level
        elif isinstance(level, str):
            if not level.startswith("Level "):
                return int(v)
        raise ValueError(f"Level name is {level}")

    database_uri: str

    redis_host: str
    redis_db: int

    class Config:
        env_prefix = _env_prefix


class ConfigLocal(Config):
    """
    This config is for when you are in the local development environment
    """

    app_env: str = "local"

    redis_host = "redis"
    redis_db = 0


_configs: Dict[str, Type[Config]] = {
    cfg.__fields__["app_env"].default: cfg for cfg in [ConfigLocal]
}


def get_config_from_environment() -> Config:
    env_key = f"{_env_prefix.upper()}APP_ENV"
    try:
        app_env = os.environ[env_key]
    except KeyError:
        raise RuntimeError(
            f"FATAL!!! Could not determine configuration class as {env_key} is not defined in the environment"
        )
    try:
        config_klass = _configs[app_env]
    except KeyError:
        raise RuntimeError(
            f"FATAL!!! Could ont determine configuration from {env_key}={app_env}"
        )
    return config_klass()


def setup_logging(config: Config) -> None:
    root = logging.getLogger()
    root.handlers = []
    formatter = logging.Formatter(
        "%(asctime)s - %(process)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(config.root_log_level)
    stream_handler.setFormatter(formatter)
    root.addHandler(stream_handler)
    root.setLevel(config.root_log_level)
