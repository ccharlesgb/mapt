from app.core.config import Config
from app.core.database import Database
from arq import ArqRedis
from fastapi import FastAPI


class MaptAPI(FastAPI):  # type: ignore
    database: Database
    config: Config
    task_queue: ArqRedis
