"""Contains unit conversion methods."""

import numpy as np

DEGREES_TO_RADIANS_RATIO = np.pi / 180.0
"""Numerical ratio between degrees and radians."""


def degrees_to_radians(degrees: float) -> float:
    """
    Utility method that converts an angle in degrees into radians.

    :param degrees: The angle in degrees to transform.
    :return: The result in radians.
    """
    return degrees * DEGREES_TO_RADIANS_RATIO


def radians_to_degrees(radians: float) -> float:
    """
    Utility method that converts an angle in radians into degrees.

    :param radians: The angle in radians to transform.
    :return: The result in degrees.
    """
    return radians / DEGREES_TO_RADIANS_RATIO
