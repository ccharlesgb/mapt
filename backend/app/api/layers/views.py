from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Layer(BaseModel):
    id: int
    label: str
    group: str


def get_fake_layers() -> List[Layer]:
    test_groups = ("lines", "shapes", "points")

    layers: List[Layer] = []
    index = 1
    for group in test_groups:
        for i in range(0, 3):
            layers.append(Layer(id=index, group=group, label=f"Layer{index}"))
    return layers


@router.get("/", response_model=List[Layer])
def get_layers() -> List[Layer]:
    return get_fake_layers()
