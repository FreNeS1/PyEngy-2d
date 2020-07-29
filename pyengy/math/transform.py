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
        self.position = position
        """Position of the transform, given left to right X coordinates and up to down Y coordinates."""
        self.rotation = rotation
        """Rotation of the transform, clockwise in radians. Will be between 0 and 2π radians."""
        self.size = scale
        """Scale of the transform."""
        self.matrix = np.eye(3, dtype=np.float64)
        """Transformation matrix."""
        self.__build_matrix()

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
        transform.__resolve_components()
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
        transform.__resolve_components()
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
        transform.__resolve_components()
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
        transform.__resolve_components()
        return transform

    def update(self):
        """Update the internal matrix of the transform."""
        self.__build_matrix()

    def __build_matrix(self):
        """
        Auxiliary method to rebuild the transformation matrix from the transform position, rotation and scale.
        Normalizes rotation and scale by default.
        """
        self.__normalize()
        tx, ty = self.position[0], self.position[1]
        theta = self.rotation
        sx, sy = self.size[0], self.size[1]

        self.matrix = np.array([
            [np.multiply(sx, np.cos(theta)), np.multiply(sy, -np.sin(theta)), tx],
            [np.multiply(sx, np.sin(theta)), np.multiply(sy, np.cos(theta)), ty],
            [0, 0, 1]
        ], dtype=np.float64)

    def __resolve_components(self):
        """
        Auxiliary method to resolve readable components from a transformation matrix. Operations on the transform
        should be made with the matrix to avoid numeric issues, so this method will be used mostly to set the new
        position, rotation and scale after an operation.
        """
        tx, ty = self.matrix[0][2], self.matrix[1][2]
        theta = np.arctan2(self.matrix[1][0], self.matrix[0][0])

        if ((-3 / 4) * np.pi < theta < (-1 / 4) * np.pi) or ((1 / 4) * np.pi < theta < (3 / 4) * np.pi):
            sx_sign = -np.sign(self.matrix[0][1]) * np.sign(np.sin(theta))
            sy_sign = np.sign(self.matrix[1][0]) * np.sign(np.sin(theta))
        else:
            sx_sign = np.sign(self.matrix[0][0]) * np.sign(np.cos(theta))
            sy_sign = np.sign(self.matrix[1][1]) * np.sign(np.cos(theta))

        sx = sx_sign * np.sqrt(np.square(self.matrix[0][0]) + np.square(self.matrix[1][0]))
        sy = sy_sign * np.sqrt(np.square(self.matrix[0][1]) + np.square(self.matrix[1][1]))

        self.position = (tx, ty)
        self.rotation = theta
        self.size = (sx, sy)
        self.__normalize()

    def __normalize(self):
        """
        Normalizes rotation and scale values. Will allow only positive rotation values between 0 and 2π radians. Scale
        will be transformed to avoid double negative scaling.
        """
        if self.size[0] < 0 and self.size[1] < 0:
            self.size = (-self.size[0], -self.size[1])
            self.rotation = self.rotation + np.pi
        self.rotation = self.rotation % (2 * np.pi)

    @staticmethod
    def identity() -> Transform2D:
        """
        Returns the identity transform, which has no translation and rotation, and unit scale factor.

        :return: The identity transform
        """
        return Transform2D(position=(0, 0), rotation=0, scale=(1, 1))
