import logging
from contextlib import contextmanager
from time import sleep
from typing import Generator

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request

logger = logging.getLogger("__name__")
logger.addHandler(logging.NullHandler())


class Database:
    def __init__(self, uri: str):
        self.uri = uri
        self.engine: Engine = create_engine(self.uri)
        self._session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def connect(self, max_retries: int = 5, retry_delay: int = 5) -> None:
        retry_count = 0
        while retry_count < max_retries:
            logger.info(f"Attempting to connect to DB (Attempt={retry_count + 1})")
            try:
                retry_count += 1
                self.engine.connect()
                logger.info("DB Connection successful")
                return
            except OperationalError as e:
                logger.warning(f"Failed to connect to DB: {str(e)}")
            sleep(retry_delay)
        raise RuntimeError(f"Could not connect to DB after {max_retries} attempts")

    def disconnect(self) -> None:
        logger.info("Disconnecting from DB")
        self.engine.dispose()

    def session(self) -> Session:
        return self._session_maker()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        session = self._session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def get_session(request: Request) -> Generator[Session, None, None]:
    session = request.app.database.session()
    try:
        yield session
    finally:
        session.close()
