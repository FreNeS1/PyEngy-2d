"""Contains the Node class."""

from __future__ import annotations

from typing import Optional, List, Union

from pygame.event import EventType

from pyengy.error import PyEngyError, NodeError
from pyengy.util.context_utils import Context
from pyengy.util.logger_utils import get_logger, PyEngyLoggerWrapper


class Node:
    """
    Base simple Node.

    Contains the basic logic for node encapsulation and delegating. Instantiate the node with the constructor and then
    build the root node. Each node should handle it's own render with ``_render_self``, update with ``_update_self``
    and event handling with ``_handle_event_self``.

    If a node is inactive it will not update or handle events, and neither will its children. If a node is invisible it
    will not render, and neither will its children
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
        self.app_name = ""
        """App name of the node, given at build time."""
        self.name = name
        """
        Name of the node. Will be used for user friendly interactions on log, display or error. Does not need to be
        globally unique, but should be unique between the children of the same parent and readonly.
        """
        self.visible = True
        """Marks if an node is visible. Invisible nodes do not render, and neither will its children."""
        self.active = True
        """Marks if an node is active. Inactive nodes do not update or handle events, and neither will its children."""
        self._path = name
        """Internal attribute for path."""
        self._parent: Optional[Node] = None
        """Internal attribute for parent."""
        self._children: List[Node] = []
        """Internal attribute for children."""
        self._logger: Optional[PyEngyLoggerWrapper] = None
        """Logger for the node. Will be instantiated as a PyEngyNode when node is built."""

        if parent:
            self.parent = parent
        if children:
            self.children = children

    def __str__(self) -> str:
        self_str = self.get_display_name()
        if len(self.children) != 0:
            children_str = list(map(lambda child: "\n  {}".format(str(child).replace("\n", "\n  ")), self.children))
            self_str = "{} {{{}\n}}".format(self_str, "".join(children_str))
        return self_str

    @property
    def path(self):
        return self._path

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    @parent.setter
    def parent(self, parent: Optional[Node]) -> None:
        """
        Sets the node parent. Will reset previous.

        :param parent: The node to set as parent. If None then set as a root node.
        """
        if self.parent:
            self.parent.remove_child(self)
        if parent:
            parent.add_child(self)

    @children.setter
    def children(self, children: Optional[List[Node]]) -> None:
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
        return "{} {} at {}".format(self.__class__.__name__, self.id, self._path)

    def get_node(self, identifier: Union[int, str]) -> Optional[Node]:
        """
        Retrieves a node. Node retrieved should be a relative of the node. Delegates the search to the root node.

        :param identifier: The id, or fully qualified path of the node to retrieve.
        :return: The retrieved node or None if node does not exist or was not found.
        """
        if self.parent:
            return self.parent.get_node(identifier)

        # Identifier is an id
        if isinstance(identifier, int):
            return self.__find_node_by_id(identifier)

        # Identifier is a fully qualified path.
        if not identifier.startswith("{}/".format(self.name)):
            return None
        return self.__find_node_by_path(identifier[len(self.name) + 1:])

    def add_child(self, child: Node) -> None:
        """
        Adds a child to this node.

        :param child: The node to add as a child.
        :raises NodeError: If there is a cyclic node dependency or a name collision within the new node.
        """
        if self.__cyclic_node_dependency([child]):
            raise NodeError(self.get_identifier(), "Cyclic dependency with ({})".format(child.get_identifier()))
        if any([child.name == c.name for c in self._children]):
            raise NodeError(self.get_identifier(), "Not unique name for child \"{}\"".format(child.name))
        if child._parent:
            child._parent.remove_child(child)

        child._parent = self
        self._children.append(child)
        child._on_parent_changed()

    def remove_child(self, child: Union[int, str, Node]) -> None:
        """
        Removes a child from this node.

        :param child: The child id, name or instance to remove.
        :raises NodeName: If the node does not exist or is not a child.
        """
        # Child is an ID
        if isinstance(child, int):
            catcher = [c for c in self._children if c.id == child]
            if len(catcher) == 0:
                raise NodeError(self.get_identifier(), "No child with id \"{}\"".format(child))
            child_node = catcher[0]

        # Child is a name
        elif isinstance(child, str):
            catcher = [c for c in self._children if c.name == child]
            if len(catcher) == 0:
                raise NodeError(self.get_identifier(), "No child with name \"{}\"".format(child))
            child_node = catcher[0]

        # Child is a node
        else:
            if child not in self._children:
                raise NodeError(self.get_identifier(), "\"{}\" is not a child".format(child.get_identifier()))
            child_node = child

        child_node._parent = None
        self._children.remove(child_node)
        child_node._on_parent_changed()

    def build(self, context: Context):
        """
        Builds the node. This should always be called once before doing any operations with the node

        :param context: Contains the context data of the application.
        """
        try:
            self._build_self(context)
        except PyEngyError as err:
            self._logger.error(NodeError(self.get_identifier(), "Could not build node", [err]))
        for child in self.children:
            child.build(context)

    def render(self, delta: float, context: Context) -> None:
        """
        Renders the node. This render can be called at a fixed rate to match display rate.

        :param delta: The time since the last render in milliseconds.
        :param context: Contains the context data of the application.
        """
        if self.visible:
            try:
                self._render_self(delta, context)
            except PyEngyError as err:
                self._logger.error(NodeError(self.get_identifier(), "Could not render node", [err]))
            for child in self.children:
                child.render(delta, context)

    def update(self, delta: float, context: Context) -> None:
        """
        Updates the node and its children. This updates are done as fast as possible.

        :param delta: The time frame since the last update in milliseconds.
        :param context: Contains the context data of the application.
        """
        if self.active:
            try:
                self._update_self(delta, context)
            except PyEngyError as err:
                self._logger.error(NodeError(self.get_identifier(), "Could not update node", [err]))
            for child in self.children:
                child.update(delta, context)

    def handle_event(self, event: EventType, context: Context) -> None:
        """
        Handles a node event. Events are handled before updates.

        :param event: The event to handle.
        :param context: Contains the context data of the application.
        """
        if self.active:
            try:
                self._handle_event_self(event, context)
            except PyEngyError as err:
                self._logger.error(NodeError(self.get_identifier(), "Could not handle event {}".format(event), [err]))
            for child in self.children:
                child.handle_event(event, context)

    def _build_self(self, context: Context) -> None:
        """
        Handles the node build.

        :param context: Contains the context data of the application.
        """
        self.app_name = context.get("metadata.app_name", item_type=str)
        self._logger = get_logger(self._path, self.app_name)

    def _render_self(self, delta: float, context: Context) -> None:
        """
        Handles the node render.

        :param delta: The time since the last update in milliseconds.
        :param context: Contains the context data of the application.
        """

    def _update_self(self, delta: float, context: Context) -> None:
        """
        Handles the node update.

        :param delta: The time since the last render in milliseconds.
        :param context: Contains the context data of the application.
        """

    def _handle_event_self(self, event: EventType, context: Context) -> None:
        """
        Handles the node event.

        :param event: The event to handle.
        :param context: Contains the context data of the application.
        """

    def _on_parent_changed(self):
        """
        Auxiliary method to update a node when it's parent changes. By default updates the path.
        Will call itself on the node children automatically.
        """
        self._path = "{}/{}".format(self.parent._path, self.name) if self.parent is not None else self.name
        if self._logger is not None:
            self._logger = get_logger(self._path, self.app_name)
        for child in self.children:
            child._on_parent_changed()

    def __find_node_by_id(self, id_value: int) -> Optional[Node]:
        """
        Auxiliary method to retrieve a node from an id. First call to this method should be delegated to a root node.

        :param id_value: The id of the node to retrieve.
        :return: The retrieved node or None if node does not exist or was not found.
        """
        if self.id == id_value:
            return self
        catcher = [c.__find_node_by_id(id_value) for c in self.children]
        if len(catcher) == 0:
            return None
        return catcher[0]

    def __find_node_by_path(self, path: str) -> Optional[Node]:
        """
        Auxiliary method to retrieve a node from a path. First call to this method should be delegated to a root node.

        :param path: The path of the node to retrieve.
        :return: The retrieved node or None if node does not exist or was not found.
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
        return catcher[0].__find_node_by_path(path[separator_index + 1:])

    def __cyclic_node_dependency(self, seen: List[Node]) -> bool:
        """
        Auxiliary method to check for cyclic dependencies between nodes.

        :param seen: The list of nodes already seen.
        :return: True if there is a cyclic dependency between the nodes. False otherwise.
        """
        if self in seen:
            return True
        if self.parent is not None:
            seen.append(self)
            return self.parent.__cyclic_node_dependency(seen)
        return False
