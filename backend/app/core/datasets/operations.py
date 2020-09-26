import logging
from typing import Any, Dict, List, Tuple

import fiona
from app import models
from app.core.exc import DatasetNotFoundError
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger("__name__")
logger.addHandler(logging.NullHandler())


class InvalidShapeFileError(Exception):
    """
    Raised when a file is either corrupt or not a shape file
    """


def parse_schema(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    attributes = []
    for field, type_ in schema.items():
        datatype, parameter = type_.split(":")
        attributes.append({"name": field, "display": field.title(), "type": datatype})
    return attributes


def parse_shapefile(
    filename: str, contents: bytes
) -> Tuple[models.Dataset, List[models.Feature]]:
    with fiona.BytesCollection(contents) as col:
        if col.driver != "ESRI Shapefile":
            raise InvalidShapeFileError(
                f"The file supplied '{filename}' is an invalid shape file"
            )

        schema = parse_schema(col.schema["properties"])

        dataset_row = models.Dataset(
            label=filename,
            description=f"Shape file made from file '{filename}'",
            schema=schema,
        )
        feature_rows = []
        for unique_id, feature in col.items():
            attributes = feature["properties"]
            geometry = shape(feature["geometry"])
            if not geometry.is_valid:
                raise InvalidShapeFileError(
                    f"Geometry from file '{filename}' is invalid"
                )

            feature = models.Feature(
                attributes=attributes,
                geometry=from_shape(geometry, srid=3850),
                dataset=dataset_row,
            )
            feature_rows.append(feature)
    return dataset_row, feature_rows


def upload_shapefile(session: Session, filename: str, contents: bytes) -> int:
    dataset, feature_rows = parse_shapefile(filename, contents)
    logger.info(f"Uploading {len(feature_rows)} features from '{filename}'")
    session.add_all(feature_rows)
    session.flush()
    return dataset.id


def get_dataset_by_id(session: Session, pk: int) -> models.Dataset:
    try:
        dataset = session.query(models.Dataset).filter(models.Dataset.id == pk).one()
    except NoResultFound:
        raise DatasetNotFoundError(f"Could not find Dataset with pk={pk}")
    return dataset


def get_datasets(session: Session) -> List[models.Dataset]:
    return session.query(models.Dataset).all()
