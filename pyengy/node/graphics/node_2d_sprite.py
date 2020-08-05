"""Contains the Node2D class."""
from typing import Tuple, Optional, List

import numpy as np
import pygame
from pygame import Surface

from pyengy.error import NodeError
from pyengy.node.node import Node
from pyengy.node.node_2d import Node2D
from pyengy.util import Context, ResourceManager


class Node2DSprite(Node2D):

    def __init__(self, name: str, texture_path: str, parent: Optional[Node] = None,
                 children: Optional[List[Node]] = None, position: Tuple[float, float] = (0, 0), rotation: float = 0,
                 scale: Tuple[float, float] = (1, 1), texture_offset: Tuple[int, int] = (0, 0),
                 texture_size: Optional[Tuple[int, int]] = None):
        super().__init__(name, parent, children, position, rotation, scale)

        self._texture_path = texture_path
        """Internal attribute for texture path."""
        self._texture_offset = texture_offset
        """Internal attribute for texture offset."""
        self._texture_size = texture_size
        """Internal attribute for sprite size."""
        self._sprite_surface: Surface = Surface((0, 0))
        """Internal attribute for sprite surface. Generated on build."""
        self._resource_manager: Optional[ResourceManager] = None
        """Resource manager of the Node. Used to load the image."""

    @property
    def texture_path(self) -> str:
        """Relative path to the texture resource of the sprite."""
        return self._texture_path

    @property
    def texture_offset(self) -> Tuple[int, int]:
        """Offset of the sprite relative to the top left corner of the texture resource."""
        return self._texture_offset

    @property
    def texture_size(self) -> Tuple[int, int]:
        """Size of the texture. If None, raw texture size with offset will be used."""
        return self._texture_size

    @property
    def sprite_surface(self) -> Surface:
        """Sprite PyGame surface."""
        return self._sprite_surface

    @texture_path.setter
    def texture_path(self, texture_path: str):
        self._texture_path = texture_path
        self._update_sprite_surface()

    @texture_offset.setter
    def texture_offset(self, texture_offset: Tuple[int, int]):
        self._texture_offset = texture_offset
        self._update_sprite_surface()

    @texture_size.setter
    def texture_size(self, texture_size: Tuple[int, int]):
        self._texture_size = texture_size
        self._update_sprite_surface()

    def _build_self(self, context: Context) -> None:
        super()._build_self(context)
        self._resource_manager = context.get("app.resource_manager", item_type=ResourceManager)
        self._update_sprite_surface()

    def _render_self(self, delta: float, context: Context) -> None:
        screen: Surface = context.get("app.screen", item_type=Surface)
        render_surface, render_offset = self._render_sprite_surface()
        sprite_offset = (self.global_position[0] + render_offset[0], self.global_position[1] + render_offset[1])
        screen.blit(render_surface, sprite_offset)

    def _render_sprite_surface(self) -> Tuple[Surface, Tuple[float, float]]:
        """
        Builds the transformed sprite surface, with given scale and rotation, and calculates the offset.

        :return: The transformed surface, and the surface offset.
        """
        # Scale the image
        if self.global_scale != (1, 1):
            size = (int(self._texture_size[0] * self.global_scale[0]),
                    int(self._texture_size[1] * self.global_scale[1]))
            scaled_image = pygame.transform.scale(self._sprite_surface, size)
        else:
            scaled_image = self._sprite_surface

        # Rotate the image relative to top left corner
        if self.global_rotation != 0:
            rotated_image = pygame.transform.rotate(scaled_image, -self.global_rotation)
            offset = self.__calculate_rotation_offset_corner(scaled_image.get_size(), self.global_transform.rotation)
        else:
            rotated_image = scaled_image
            offset = (0.0, 0.0)

        return rotated_image, offset

    def _update_sprite_surface(self) -> None:
        """Updates the base resource texture of the sprite."""
        if self._resource_manager is None:
            raise NodeError(self.get_identifier(), "Cannot update a node that has not been built")

        raw_texture = self._resource_manager.get_image(self._texture_path)
        if self._texture_size is None:
            self._texture_size = (raw_texture.get_size()[0] - self._texture_offset[0],
                                  raw_texture.get_size()[1] - self._texture_offset[1])

        if self._texture_offset != (0, 0) or self._texture_size != raw_texture.get_size():
            self._sprite_surface = raw_texture.subsurface(self._texture_offset, self._texture_size)
        else:
            self._sprite_surface = raw_texture

    @staticmethod
    def __calculate_rotation_offset_corner(size: Tuple[float, float], rotation: float) -> Tuple[float, float]:
        """
        Auxiliary method that calculates the offset of a transform rotation, with the top left corner as a pivot.

        :param size: Size of the original non rotated image.
        :param rotation: Angle of the rotation in radians, counterclockwise.
        :return: The offset position.
        """
        w, h = size
        if rotation < (1 / 2) * np.pi:
            offset = (-h * np.sin(rotation), 0)
        elif rotation < np.pi:
            offset = (-np.abs(w * np.cos(rotation)) - np.abs(h * np.sin(rotation)), h * np.cos(rotation))
        elif rotation < (3 / 2) * np.pi:
            offset = (w * np.cos(rotation), -np.abs(w * np.sin(rotation)) - np.abs(h * np.cos(rotation)))
        else:
            offset = (0, w * np.sin(rotation))
        return offset
