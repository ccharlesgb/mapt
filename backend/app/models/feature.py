from geoalchemy2 import Geometry
from sqlalchemy import Column, Index
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base, IntKeyMixin


class Feature(Base, IntKeyMixin):
    """
    Stores the raw shape file information
    """

    __tablename__ = "features"
    attributes = Column(JSONB())
    geometry = Column(Geometry(srid=3850), index=True)

    __table_args__ = (
        Index("ix_attributes", attributes, postgresql_using="gin"),
        {"schema": "mapt"},
    )
