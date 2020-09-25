from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import Base, IntKeyMixin


class Dataset(IntKeyMixin, Base):
    """
    Stores the metadata for a set of features
    """

    label = Column(String(256), nullable=False, index=True)
    description = Column(String(), nullable=False, index=True)
    schema = Column(JSONB(), nullable=False)

    __table_args__ = (Index("ix_schema", schema, postgresql_using="gin"),)

    features = relationship("Feature", uselist=True, back_populates="dataset")
