import math
from typing import Any, List, Optional

import cv2
import numpy as np
from PIL import Image

from ralfpt.typehints import Element, PilImage


def dilate_mask(
    original_mask: np.ndarray, kernel_size: int = 5, iterations: int = 8
) -> np.ndarray:
    assert kernel_size > 0 and kernel_size % 2 == 1
    assert iterations > 0

    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)

    dilated_mask = cv2.dilate(
        original_mask.astype("uint8"), kernel, iterations=iterations
    )
    return dilated_mask.astype("float32")  # typing: ignore


def get_mask(image_width: int, image_height: int, elements: List[Element]) -> PilImage:
    canvas = np.zeros((image_height, image_width, 1), dtype=np.float32)

    # draw bounding boxes
    for element in elements:
        coord = element["coordinates"]

        x1 = math.floor(image_width * coord["left"])
        x2 = math.ceil(image_width * coord["right"])
        y1 = math.floor(image_height * coord["top"])
        y2 = math.ceil(image_height * coord["bottom"])

        cv2.rectangle(
            canvas,
            pt1=(x1, y1),
            pt2=(x2, y2),
            color=(1, 1, 1),
            thickness=-1,
            lineType=cv2.LINE_4,
            shift=0,
        )

    canvas = dilate_mask(canvas)
    return Image.fromarray((canvas * 255).astype(np.uint8))


def apply_inpainting(
    image: PilImage, elements: List[Element], inpainter: Optional[Any] = None
) -> PilImage:
    image = image.convert("RGB") if image.mode != "RGB" else image
    image_width, image_height = image.size

    mask = get_mask(
        image_width=image_width,
        image_height=image_height,
        elements=elements,
    )

    if inpainter is None:
        from simple_lama_inpainting import SimpleLama

        inpainter = SimpleLama()

    result = inpainter(image, mask)
    result = result.resize(image.size)

    return result
