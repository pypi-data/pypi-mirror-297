import logging
from typing import Optional, Tuple

from ralfpt.typehints import Coordinates

logger = logging.getLogger(__name__)


def _compare(low: float, high: float) -> Tuple[float, float]:
    return (high, low) if low > high else (low, high)


def clamp_w_tol(
    value: float, tolerance: float = 5e-3, vmin: float = 0.0, vmax: float = 1.0
) -> float:
    """
    Clamp the value to [vmin, vmax] range with tolerance.
    """
    assert vmin - tolerance <= value <= vmax + tolerance, value
    return max(vmin, min(vmax, value))


def validate_coordinates(coordinates: Coordinates) -> None:
    """
    Check if all values are valid (i.e. in [0, 1] range).
    """
    assert 0.0 <= coordinates["left"] <= 1.0, coordinates
    assert 0.0 <= coordinates["center_x"] <= 1.0, coordinates
    assert 0.0 <= coordinates["right"] <= 1.0, coordinates
    assert 0.0 <= coordinates["width"] <= 1.0, coordinates
    assert coordinates["left"] <= coordinates["right"], coordinates

    assert 0.0 <= coordinates["top"] <= 1.0, coordinates
    assert 0.0 <= coordinates["center_y"] <= 1.0, coordinates
    assert 0.0 <= coordinates["bottom"] <= 1.0, coordinates
    assert 0.0 <= coordinates["height"] <= 1.0, coordinates
    assert coordinates["top"] <= coordinates["bottom"], coordinates


def has_valid_area(width: float, height: float, thresh: float = 1e-3, **kwargs) -> bool:
    """
    Check whether the area is smaller than the threshold.
    """
    area = width * height
    valid = area > thresh
    if not valid:
        logger.debug(f"Filtered by {area=} = {width=} * {height=}")
    return valid


def load_from_pku_ltrb(
    box: Tuple[float, float, float, float],
    global_width: Optional[int] = None,
    global_height: Optional[int] = None,
) -> Coordinates:
    left, top, right, bottom = box

    if global_width and global_height:
        left /= global_width
        right /= global_width
        top /= global_height
        bottom /= global_height

    left, right = clamp_w_tol(left), clamp_w_tol(right)
    top, bottom = clamp_w_tol(top), clamp_w_tol(bottom)

    left, right = _compare(left, right)
    top, bottom = _compare(top, bottom)

    center_x = clamp_w_tol((left + right) / 2)
    center_y = clamp_w_tol((top + bottom) / 2)
    width, height = right - left, bottom - top

    coordinates = Coordinates(
        left=left,
        center_x=center_x,
        right=right,
        width=width,
        top=top,
        center_y=center_y,
        bottom=bottom,
        height=height,
    )
    validate_coordinates(coordinates)

    return coordinates


def load_from_cgl_ltwh(
    ltwh: Tuple[float, float, float, float],
    global_width: Optional[int] = None,
    global_height: Optional[int] = None,
) -> Coordinates:
    left, top, width, height = ltwh

    if global_width and global_height:
        left /= global_width
        width /= global_width
        top /= global_height
        height /= global_height

    left, right = clamp_w_tol(left), clamp_w_tol(left + width)
    top, bottom = clamp_w_tol(top), clamp_w_tol(top + height)

    left, right = _compare(left, right)
    top, bottom = _compare(top, bottom)

    center_x = clamp_w_tol((left + right) / 2)
    center_y = clamp_w_tol((top + bottom) / 2)
    width, height = right - left, bottom - top

    coordinates = Coordinates(
        left=left,
        center_x=center_x,
        right=right,
        width=width,
        top=top,
        center_y=center_y,
        bottom=bottom,
        height=height,
    )
    validate_coordinates(coordinates)

    return coordinates
