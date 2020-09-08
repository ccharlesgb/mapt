from fastapi import APIRouter
from . import layers

# This is the parent router of the entire API. Any resources should be added under this
router = APIRouter()
router.include_router(layers.router, prefix="/layers")
