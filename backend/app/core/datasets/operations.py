import logging

import fiona
from app import models
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from sqlalchemy.orm import Session

logger = logging.getLogger("__name__")
logger.addHandler(logging.NullHandler())


class InvalidShapeFileError(Exception):
    """
    Raised when a file is either corrupt or not a shape file
    """


def upload_shapefile(session: Session, filename: str, contents: bytes) -> int:
    with fiona.BytesCollection(contents) as col:
        if col.driver != "ESRI Shapefile":
            raise InvalidShapeFileError(
                f"The file supplied '{filename}' is an invalid shape file"
            )
        dataset_row = models.Dataset(
            label=filename,
            description=f"Shape file made from file '{filename}'",
            schema=None,
        )
        feature_rows = []
        for unique_id, feature in col.items():
            attributes = feature["properties"]
            geometry = shape(feature["geometry"])
            if not geometry.is_valid:
                raise ValueError(f"Geometry from file '{filename}' is invalid")

            feature = models.Feature(
                attributes=attributes,
                geometry=from_shape(geometry, srid=3850),
                dataset=dataset_row,
            )
            feature_rows.append(feature)
        logger.info(f"Uploading {len(feature_rows)} features from '{filename}'")
        session.add_all(feature_rows)
        session.flush()
    return dataset_row.id
