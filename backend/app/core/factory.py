import logging
from typing import Optional

from app.api import router
from app.core.upload_worker.factory import create_redis_settings
from arq import create_pool
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Config, get_config_from_environment, setup_logging
from .database import Database
from .klass import MaptAPI

logger = logging.getLogger("__name__")
logger.addHandler(logging.NullHandler())

origins = ["http://localhost:3000"]


def create_app(config_override: Optional[Config] = None) -> FastAPI:
    if config_override is not None:
        app_config = config_override
    else:
        app_config = get_config_from_environment()
    app = MaptAPI(title=app_config.title, description=app_config.description)
    app.config = app_config
    setup_logging(app.config)
    setup_db(app)
    setup_task_queue(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


def setup_task_queue(app: MaptAPI) -> None:
    # ARQ is a fully async library so we need to do this in the startup event handler instead
    # Note this means you won't have access to the task_queue in all these sync factory functions but I haven't had
    # Issues with this
    @app.on_event("startup")
    async def create_task_queue() -> None:
        arq = await create_pool(create_redis_settings(app.config))
        app.task_queue = arq
        job = await arq.enqueue_job("hello_world")
        if job:
            print(await job.result())


def setup_db(app: MaptAPI) -> None:
    app.database = Database(app.config.database_uri)

    @app.on_event("startup")
    def connect_to_db() -> None:
        app.database.connect()

    @app.on_event("shutdown")
    def disconnect_from_db() -> None:
        app.database.disconnect()
