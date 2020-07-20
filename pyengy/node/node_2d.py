"""Contains the Node2D class."""

from typing import Optional, List, Tuple

from pyengy.math import Transform2D
from .node import Node


class Node2D(Node):
    """
    Represents a given 2D node in an environment.

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
        self._transform = Transform2D(position, rotation, scale)
        self._global_transform = self._transform
        super().__init__(name, parent, children)

    def _on_parent_changed(self):
        super()._on_parent_changed()
        self._on_parent_transform_changed()

    def _on_parent_transform_changed(self):
        """
        Auxiliary method to call when the a transform changes. Updates the transform when the parent changes or moves.
        Will call itself on the node children automatically if they are Node2D nodes.
        """
        if self.parent is not None and isinstance(self.parent, Node2D):
            self._global_transform = self.parent._global_transform.apply(self._transform)
        else:
            self._global_transform = self._transform

        for child in self.children:
            if isinstance(child, Node2D):
                child._on_parent_transform_changed()
