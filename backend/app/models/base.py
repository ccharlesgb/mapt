from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base


class IntKeyMixin:
    id = Column(Integer(), primary_key=True)


metadata = MetaData()
Base = declarative_base(metadata=metadata)
