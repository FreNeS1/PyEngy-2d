"""Contains the Transform2D class."""

from __future__ import annotations

from typing import Tuple

import numpy as np


class Transform2D:
    """
    Class that contains 2D position, rotation and scale. Can manage composition through transformation matrices.

    Position is measured with left to right X coordinates and up to down Y coordinates. The rotation is measured
    clockwise, in radians. Scale is applied without shearing.

    All calculations will be made with an internal numpy matrix to minimize numeric error.
    """

    def __init__(self, position: Tuple[float, float], rotation: float, scale: Tuple[float, float]) -> None:
        """
        Initialize a transformation matrix with a given position, rotation and scale. Does not handle shearing.

        :param position: Position of the transform, given left to right X coordinates and up to down Y coordinates.
        :param rotation: Rotation of the transform, clockwise in radians.
        :param scale: Scale of the transform.
        """
        theta, sx, sy = self.__normalize(rotation, scale[0], scale[1])
        self.position = position
        """Position of the transform, given left to right X coordinates and up to down Y coordinates."""
        self.rotation = theta
        """Rotation of the transform, clockwise in radians. Will be between 0 and 2π radians."""
        self.size = (sx, sy)
        """Scale of the transform."""
        self.matrix = self.__build_matrix(self.position, self.rotation, self.size)
        """Transformation matrix."""

    def move(self, tx: float, ty: float, before=True) -> Transform2D:
        """
        Apply a translation to the transform.

        :param tx: The movement to apply to the transform in the X axis.
        :param ty: The movement to apply to the transform in the Y axis.
        :param before: If true, the movement will be applied before current transform. Otherwise will be applied after.
        :return: The resulting transform.
        """
        t_matrix = np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ], dtype=np.float64)

        transform = Transform2D.identity()
        transform.matrix = np.dot(t_matrix, self.matrix) if before else np.dot(self.matrix, t_matrix)
        transform.position, transform.rotation, transform.size = self.__resolve_components(transform.matrix)
        return transform

    def rotate(self, theta: float, before=False) -> Transform2D:
        """
        Apply a rotation to the transform.

        :param theta: The movement to apply to the transform.
        :param before: If true, the rotation will be applied before current transform. Otherwise will be applied after.
        :return: The resulting transform.
        """
        r_matrix = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ], dtype=np.float64)

        transform = Transform2D.identity()
        transform.matrix = np.dot(r_matrix, self.matrix) if before else np.dot(self.matrix, r_matrix)
        transform.position, transform.rotation, transform.size = self.__resolve_components(transform.matrix)
        return transform

    def scale(self, sx: float, sy: float, before=False) -> Transform2D:
        """
        Apply a scale factor to the transform.

        :param sx: The scale factor to apply to the transform in the X axis.
        :param sy: The scale factor to apply to the transform in the X axis.
        :param before: If true, the movement will be applied before current transform. Otherwise will be applied after.
        :return: The resulting transform.
        """
        s_matrix = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ], dtype=np.float64)

        transform = Transform2D.identity()
        transform.matrix = np.dot(s_matrix, self.matrix) if before else np.dot(self.matrix, s_matrix)
        transform.position, transform.rotation, transform.size = self.__resolve_components(transform.matrix)
        return transform

    def apply(self, other: Transform2D) -> Transform2D:
        """
        Apply a transform to another. The resulting transform will be the composition of both, applying the transform
        given to the current one.

        :param other: The transform to apply to the given one.
        :return: The resulting transform.
        """
        transform = Transform2D.identity()
        transform.matrix = np.dot(self.matrix, other.matrix)
        transform.position, transform.rotation, transform.size = self.__resolve_components(transform.matrix)
        return transform

    @classmethod
    def __build_matrix(cls, position: Tuple[float, float], rotation: float, scale: Tuple[float, float]) -> np.ndarray:
        """
        Auxiliary method to build a transformation matrix from a given position, rotation and scale.

        :param position: Position of the transform, given left to right and up to down coordinates.
        :param rotation: The clockwise rotation in radians.
        :param scale: The x and y scale without shearing.
        :return: The transformation matrix
        """
        tx, ty = position[0], position[1]
        theta = rotation
        sx, sy = scale[0], scale[1]

        return np.array([
            [np.multiply(sx, np.cos(theta)), np.multiply(sy, -np.sin(theta)), tx],
            [np.multiply(sx, np.sin(theta)), np.multiply(sy, np.cos(theta)), ty],
            [0, 0, 1]
        ], dtype=np.float64)

    @classmethod
    def __resolve_components(cls, matrix: np.ndarray) -> Tuple[Tuple[float, float], float, Tuple[float, float]]:
        """
        Auxiliary method to resolve readable components from a transformation matrix. Operations on the transform
        should be made with the matrix to avoid numeric issues, so this method will be used mostly to set the new
        position, rotation and scale after an operation.

        :param matrix: The transformation matrix to extract.
        :return: The extracted and normalized position, rotation and scale.
        """
        tx, ty = matrix[0][2], matrix[1][2]
        theta = np.arctan2(-matrix[0][1], matrix[0][0])
        if ((-3 / 4) * np.pi < theta < (-1 / 4) * np.pi) or ((1 / 4) * np.pi < theta < (3 / 4) * np.pi):
            sx, sy = matrix[1][0] / np.sin(theta), matrix[0][1] / -np.sin(theta)
        else:
            sx, sy = matrix[0][0] / np.cos(theta), matrix[1][1] / np.cos(theta)
        theta, sx, sy = cls.__normalize(theta, sx, sy)

        return (tx, ty), theta, (sx, sy)

    @classmethod
    def __normalize(cls, theta: float, scale_x: float, scale_y: float) -> Tuple[float, float, float]:
        """
        Normalizes rotation and scale values. Will allow only positive rotation values between 0 and 2π radians. Scale
        will be transformed to avoid double negative scaling.

        :param theta: The raw rotation.
        :param scale_x: The raw X scaling factor. Can be negative.
        :param scale_y: The raw Y scaling factor. Can be negative.
        :return: The normalized values for rotation and scale.
        """
        n_theta = theta
        n_scale_x = scale_x
        n_scale_y = scale_y

        if scale_x < 0 and scale_y < 0:
            n_scale_x = -scale_x
            n_scale_y = -scale_y
            n_theta = theta + np.pi

        n_theta = n_theta % (2 * np.pi)

        return n_theta, n_scale_x, n_scale_y

    @staticmethod
    def identity() -> Transform2D:
        """
        Returns the identity transform, which has no translation and rotation, and unit scale factor.

        :return: The identity transform
        """
        return Transform2D(position=(0, 0), rotation=0, scale=(1, 1))
