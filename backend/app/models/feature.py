from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import Base, IntKeyMixin


class Feature(IntKeyMixin, Base):
    """
    Stores information for a feature which has geometry and attributes
    """

    __tablename__ = "features"
    dataset_id = Column(Integer(), ForeignKey("Dataset.id"), index=True)
    attributes = Column(JSONB())
    geometry = Column(Geometry(srid=3850), index=True)

    __table_args__ = (Index("ix_attributes", attributes, postgresql_using="gin"),)

    dataset = relationship("Dataset", uselist=False, back_populates="features")
