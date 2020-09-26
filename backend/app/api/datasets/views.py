from typing import List

from app.core.datasets.operations import (
    get_dataset_by_id,
    get_datasets,
    upload_shapefile,
)
from core.exc import DatasetNotFoundError
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from starlette.requests import Request

router = APIRouter()


class ShapeUploaded(BaseModel):
    dataset_href: str


class Attribute(BaseModel):
    name: str
    display: str
    type: str


class Dataset(BaseModel):
    label: str
    description: str
    schema_: List[Attribute] = Field(..., alias="schema")

    class Config:
        orm_mode = True


@router.post("/shapefile/", response_model=ShapeUploaded)
def upload_shape(request: Request, shape_file: UploadFile = File(...)) -> ShapeUploaded:
    """
    Upload a new shape file

    This will eventually be offloaded to the ARQ worker but keep it simple for now and do it synchronously

    """
    contents = shape_file.file.read()
    with request.app.database.session_scope() as session:
        upload_shapefile(session, shape_file.filename, contents)
    return ShapeUploaded(dataset_href="/datasets/1")


@router.get("/{dataset_id}", response_model=Dataset)
def get_dataset(request: Request, dataset_id: int) -> Dataset:
    with request.app.database.session_scope() as session:
        try:
            dataset = get_dataset_by_id(session, dataset_id)
        except DatasetNotFoundError as e:
            raise HTTPException(404, str(e))

        return Dataset.from_orm(dataset)


@router.get("/", response_model=List[Dataset])
def get_all_datasets(request: Request) -> List[Dataset]:
    with request.app.database.session_scope() as session:
        datasets = get_datasets(session)
        return list(map(Dataset.from_orm, datasets))
