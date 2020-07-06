"""Contains the Node class."""

from __future__ import annotations

from typing import Optional, List, Union

from pygame.event import EventType

from pyengy.error import NodeError


class Node:
    """
    Represents a given node in an environment. Contains the basic logic for node encapsulation and delegating
    interactions to the nodes themselves. Each node should handle it's own render with ``_render_self``, update with
    ``_update_self`` and event handling with ``_handle_event_self``.

    If a node is inactive it will not render, update or handle events, and neither will its children.
    """

    def __init__(self, name: str, parent: Optional[Node] = None, children: Optional[List[Node]] = None):
        """
        Instantiates a new Node. If setting the parent of children nodes creates a circular dependency, instantiating
        the node will raise a NodeException.

        :param name: The human readable name of the node. Does not need to be globally unique, but should be unique
                     between the children of the same parent.
        :param parent: The parent node. If not specified, the node will assume to have no parent or reference.
        :param children: The children nodes. If not specified, the node will not append any children.
        """
        self.id = id(self)
        """Unique identity id of the node. Same value as the identity of the object in python."""
        self.name = name
        """
        Name of the node. Will be used for user friendly interactions on log, display or error. Does not need to be
        globally unique, but should be unique between the children of the same parent.
        """
        self.path = name
        """Path of the node. Will be used to identify the node with user friendly notation. Should be unique."""
        self.active = True
        """
        Flag that marks if an node is active. Inactive nodes do not render, update or handle events, and neither will
        its children.
        """
        self.parent: Optional[Node] = None
        """Reference to the parent node. If None, this is a root node."""
        self.children: List[Node] = []
        """List of child nodes."""

        if parent:
            self.set_parent(parent)
        if children:
            self.set_children(children)

    def __str__(self):
        self_str = self.get_display_name()
        if len(self.children) != 0:
            self_str += " {"
            for child in self.children:
                self_str += "\n  {}".format(str(child).replace("\n", "\n  "))
            self_str += "\n}"
        return self_str

    def get_display_name(self) -> str:
        """
        Returns the display name of the node: class, name and id of the node.

        :return: Node display name.
        """
        return "{} {} ({})".format(self.__class__.__name__, self.name, self.id)

    def get_identifier(self) -> str:
        """
        Returns the full identification of a node: class, id and full path.

        :return: Node identifier.
        """
        return "{} {} at {}".format(self.__class__.__name__, self.id, self.path)

    def get_node(self, identifier: Union[int, str]) -> Optional[Node]:
        """
        Retrieves a node. Should be a descendant of this one.

        :param identifier: The id, path to retrieve
        :return: The retrieved node or None if node does not exist or was not found.
        """
        # Node is an ID
        if isinstance(identifier, int):
            if self.id == identifier:
                return self
            catcher = [c.get_node(identifier) for c in self.children]
            if len(catcher) == 0:
                return None
            return catcher[0]

        # Node is a path
        if self.name not in identifier:
            return self.__get_node_from_path(identifier)
        return self.__get_node_from_path(identifier[identifier.index(self.name) + len(self.name) + 1:])

    def set_parent(self, parent: Optional[Node]) -> None:
        """
        Sets the node parent. Will reset previous.

        :param parent: The node to set as parent. If None then set as a root node.
        """
        if self.parent:
            self.parent.remove_child(self)
        if parent:
            parent.add_child(self)

    def set_children(self, children: Optional[List[Node]]) -> None:
        """
        Sets the node children. Will reset previous.

        :param children: The nodes to set as children. If none will not set any.
        """
        previous_children = list(self.children)
        try:
            for child in previous_children:
                self.remove_child(child)
            if children is not None:
                for child in children:
                    self.add_child(child)
        except (NodeError, ValueError) as err:
            self.children = previous_children
            raise err

    def add_child(self, child: Node) -> None:
        """
        Adds a child to this node.

        :param child: The node to add as a child.
        :raises NodeError: If there is a cyclic node dependency or a name collision within the new node.
        """
        if self.__cyclic_node_dependency([child]):
            raise NodeError(self.get_identifier(), "Cyclic dependency with ({})".format(child.get_identifier()))
        if any([child.name == c.name for c in self.children]):
            raise NodeError(self.get_identifier(), "Not unique name for child \"{}\"".format(child.name))
        if child.parent:
            child.parent.remove_child(child)
        child.parent = self
        child.path = "{}/{}".format(self.path, child.name)
        self.children.append(child)

    def remove_child(self, child: Union[int, str, Node]) -> None:
        """
        Removes a child from this node.

        :param child: The child id, name or instance to remove.
        :raises NodeName: If the node does not exist or is not a child.
        """
        # Child is an ID
        if isinstance(child, int):
            catcher = [c for c in self.children if c.id == child]
            if len(catcher) == 0:
                raise NodeError(self.get_identifier(), "No child with id \"{}\"".format(child))
            child_node = catcher[0]

        # Child is a name
        elif isinstance(child, str):
            catcher = [c for c in self.children if c.name == child]
            if len(catcher) == 0:
                raise NodeError(self.get_identifier(), "No child with name \"{}\"".format(child))
            child_node = catcher[0]

        # Child is a node
        else:
            if child not in self.children:
                raise NodeError(self.get_identifier(), "\"{}\" is not a child".format(child.get_identifier()))
            child_node = child

        child_node.parent = None
        child_node.path = child_node.name
        self.children.remove(child_node)

    def update(self, delta: float) -> None:
        """
        Updates the node and its children. This updates are done as fast as possible.

        :param delta: The time frame since the last update in milliseconds.
        """
        if self.active:
            self._update_self(delta)
            for child in self.children:
                child.update(delta)

    def render(self, delta: float) -> None:
        """
        Renders the node. This render can be called at a fixed rate to match display rate.

        :param delta: The time since the last render in milliseconds.
        """
        if self.active:
            self._render_self(delta)
            for child in self.children:
                child.render(delta)

    def handle_event(self, event: EventType) -> None:
        """
        Handles a node event. Events are handled before updates.

        :param event: The event to handle.
        """
        if self.active:
            self._handle_event_self(event)
            for child in self.children:
                child.handle_event(event)

    def _render_self(self, delta: float) -> None:
        """
        Handles the node update.

        :param delta: The time since the last update in milliseconds.
        """

    def _update_self(self, delta: float) -> None:
        """
        Handles the node render.

        :param delta: The time since the last render in milliseconds.
        """

    def _handle_event_self(self, event: EventType) -> None:
        """
        Handles the node event.

        :param event: The event to handle.
        """

    def __get_node_from_path(self, path: str) -> Optional[Node]:
        """
        Auxiliary method to retrieve a node from a path chain

        :param path: The relative path of the node from the current one.
        :return: The node specified in the path if it exists.
        """
        if "/" not in path:
            catcher = [c for c in self.children if c.name == path]
            if len(catcher) == 0:
                return None
            return catcher[0]

        separator_index = path.index("/")
        catcher = [c for c in self.children if c.name == path[:separator_index]]
        if len(catcher) == 0:
            return None
        return catcher[0].__get_node_from_path(path[separator_index + 1:])

    def __cyclic_node_dependency(self, seen: List[Node]):
        """
        Auxiliary method to check for cyclic dependencies between nodes.

        :param seen: The list of nodes already seen.
        :return: True if there is a cyclic dependency between the nodes.
        """
        if self.parent in seen:
            return True
        if self.parent is not None:
            seen.append(self)
            return self.parent.__cyclic_node_dependency(seen)
        return False
