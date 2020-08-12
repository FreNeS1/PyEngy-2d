"""Contains the Node2D class."""

from typing import Optional, List, Tuple

from pyengy.math import Transform2D
from pyengy.math.unit_conversions import degrees_to_radians, radians_to_degrees
from pyengy.node.node import Node


class Node2D(Node):
    """
    Base 2D node.

    Contains the basic logic for 2D interaction: position, rotation and scaling in a 2D plane. By itself represents a
    transform or environment. Node2D and nodes that inherit from it can be encapsulated, and transforms will chain
    between them.
    """

    def __init__(self, name: str, parent: Optional[Node] = None, children: Optional[List[Node]] = None,
                 position: Tuple[float, float] = (0, 0), rotation: float = 0, scale: Tuple[float, float] = (1, 1)):
        """
        Instantiates a new Node2D.

        :param name: The human readable name of the node. Does not need to be globally unique, but should be unique
                     between the children of the same parent.
        :param parent: The parent node. If not specified, the node will assume to have no parent or reference.
        :param children: The children nodes. If not specified, the node will not append any children.
        :param position: The relative position of this node to its parent, or the origin of the screen.
        :param rotation: The relative rotation of this node to its parent, or the origin of the screen.
        :param scale: The relative scale of this node to its parent, or the origin of the screen.
        """
        self.transform = Transform2D(position, degrees_to_radians(rotation), scale)
        """Transform of the node to its parent."""
        self.global_transform = self.transform
        """Global transform of the node."""
        super().__init__(name, parent, children)

    @property
    def position(self) -> Tuple[float, float]:
        """Relative position of the node to its parent."""
        return self.transform.position

    @property
    def rotation(self) -> float:
        """Relative rotation of the node to its parent. Measured clockwise and in degrees."""
        return radians_to_degrees(self.transform.rotation)

    @property
    def scale(self) -> Tuple[float, float]:
        """Relative size of the node to its parent."""
        return self.transform.size

    @property
    def global_position(self) -> Tuple[float, float]:
        """Global position of the node."""
        return self.global_transform.position

    @property
    def global_rotation(self) -> float:
        """Global rotation of the node. Measured clockwise and in degrees."""
        return radians_to_degrees(self.global_transform.rotation)

    @property
    def global_scale(self) -> Tuple[float, float]:
        """Global size of the node."""
        return self.global_transform.size

    @position.setter
    def position(self, position: Tuple[float, float]):
        self.transform.position = position
        self._on_transform_changed()

    @rotation.setter
    def rotation(self, rotation: float):
        self.transform.rotation = degrees_to_radians(rotation)
        self._on_transform_changed()

    @scale.setter
    def scale(self, scale: Tuple[float, float]):
        self.transform.size = scale
        self._on_transform_changed()

    def _on_parent_changed(self) -> None:
        super()._on_parent_changed()
        self._on_transform_changed()

    def _on_transform_changed(self) -> None:
        """
        Auxiliary method to call when the transform changes. Updates the transform when the parent changes or moves.
        Will call itself on the node children automatically if they are Node2D nodes.
        """
        self.transform.update()

        if self.parent is not None and isinstance(self.parent, Node2D):
            self.global_transform = self.parent.global_transform.apply(self.transform)
        else:
            self.global_transform = self.transform

        for child in self.children:
            if isinstance(child, Node2D):
                child._on_transform_changed()
