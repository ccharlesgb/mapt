from typing import Optional

from app.api import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config

origins = ["http://localhost:3000"]


def create_app(config_override: Optional[config.Config] = None):
    if config_override is not None:
        app_config = config_override
    else:
        app_config = config.get_config_from_environment()
    app = FastAPI(title=app_config.title, description=app_config.description)
    app.config = app_config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app
