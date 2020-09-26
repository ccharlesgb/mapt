from fastapi import APIRouter

from . import datasets, layers

# This is the parent router of the entire API. Any testresources should be added under this
router = APIRouter()
router.include_router(layers.router, prefix="/layers")
router.include_router(datasets.router, prefix="/datasets")
