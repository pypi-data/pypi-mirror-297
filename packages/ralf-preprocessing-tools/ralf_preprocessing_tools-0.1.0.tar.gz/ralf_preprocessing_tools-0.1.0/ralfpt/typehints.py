from typing import Annotated, TypedDict

from PIL.Image import Image

PilImage = Annotated[Image, "PIL Image"]


class Coordinates(TypedDict):
    left: float
    top: float
    right: float
    bottom: float

    center_x: float
    center_y: float
    width: float
    height: float


class Element(TypedDict):
    label: int
    coordinates: Coordinates
