import logging
from typing import Any, Dict, Optional, cast

from app.core.config import Config, get_config_from_environment, setup_logging
from app.core.database import Database
from arq import Worker, run_worker
from arq.connections import RedisSettings
from arq.typing import WorkerSettingsType

from .tasks import hello_world

logger = logging.getLogger("__name__")
logger.addHandler(logging.NullHandler())


def create_redis_settings(config: Config) -> RedisSettings:
    return RedisSettings(host=config.redis_host, database=config.redis_db)


async def startup(ctx: Dict[str, Any]) -> None:
    db = Database(ctx["config"].database_uri)
    # Warning: This is running blocking IO and if this gets anymore heavy you should really run this in a thread pool
    db.connect()
    ctx["database"] = db


async def shutdown(ctx: Dict[str, Any]) -> None:
    ctx["database"].disconnect()


def create_worker(config_override: Optional[Config] = None) -> Worker:
    if config_override is not None:
        app_config = config_override
    else:
        app_config = get_config_from_environment()

    setup_logging(app_config)

    class WorkerSettings:
        functions = [hello_world]
        on_startup = startup
        on_shutdown = shutdown
        ctx = {"config": app_config}
        max_jobs = 4
        redis_settings = RedisSettings(
            host=app_config.redis_host, database=app_config.redis_db
        )

    return run_worker(cast(WorkerSettingsType, WorkerSettings))
