from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

router = APIRouter()


class ShapeUploaded(BaseModel):
    dataset_href: str
    file_size: float


@router.post("/shapes/", response_model=ShapeUploaded)
async def upload_shape(shape_file: UploadFile = File(...)) -> ShapeUploaded:
    """
    Upload a new shape file
    """
    contents = await shape_file.read()
    # TODO: 2 stage process
    # TODO: Put this blob somewhere then analyse it with fiona and upload it to PostGIS
    # TODO: Then return the newly created linnk to the dataset which will have some default settings which
    # TODO: The user can refine in the next stage of the form
    return ShapeUploaded(dataset_href="/datasets/1", file_size=len(contents))
