from app.core.config import Config
from app.core.database import Database
from fastapi import FastAPI


class MaptAPI(FastAPI):  # type: ignore
    database: Database
    config: Config
