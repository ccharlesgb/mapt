import fiona
from sqlalchemy.orm import Session


class InvalidShapeFileError(Exception):
    """
    Raised when a file is either corrupt or not a shape file
    """


def upload_shapefile(session: Session, filename: str, contents: bytes) -> None:
    with fiona.BytesCollection(contents) as col:
        if col.driver != "ESRI Shapefile":
            raise InvalidShapeFileError(
                f"The file supplied '{filename}' is an invalid shape file"
            )
        for unique_id, feature in col.items():
            print(unique_id)
            print(feature)
