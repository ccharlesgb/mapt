import logging
from typing import Optional

from app.api import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .database import Database
from .klass import MaptAPI

origins = ["http://localhost:3000"]


def create_app(config_override: Optional[config.Config] = None) -> FastAPI:
    if config_override is not None:
        app_config = config_override
    else:
        app_config = config.get_config_from_environment()
    app = MaptAPI(title=app_config.title, description=app_config.description)
    app.config = app_config
    setup_logging(app)
    setup_db(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


def setup_logging(app: MaptAPI) -> None:
    root = logging.getLogger()
    root.handlers = []
    formatter = logging.Formatter(
        "%(asctime)s - %(process)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(app.config.root_log_level)
    stream_handler.setFormatter(formatter)
    root.addHandler(stream_handler)
    root.setLevel(app.config.root_log_level)


def setup_db(app: MaptAPI) -> None:
    app.database = Database(app.config.database_uri)

    @app.on_event("startup")
    def connect_to_db() -> None:
        app.database.connect()

    @app.on_event("shutdown")
    def disconnect_from_db() -> None:
        app.database.disconnect()
