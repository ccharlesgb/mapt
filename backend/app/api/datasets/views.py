from app.core.datasets import upload_shapefile
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from starlette.requests import Request

router = APIRouter()


class ShapeUploaded(BaseModel):
    dataset_href: str
    file_size: float


@router.post("/shapes/", response_model=ShapeUploaded)
async def upload_shape(
    request: Request, shape_file: UploadFile = File(...)
) -> ShapeUploaded:
    """
    Upload a new shape file
    """
    contents = await shape_file.read()
    with request.app.database.session_scope() as session:
        upload_shapefile(session, shape_file.filename, contents)
    return ShapeUploaded(dataset_href="/datasets/1", file_size=len(contents))
