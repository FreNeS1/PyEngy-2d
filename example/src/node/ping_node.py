"""Contains the Node class."""

from typing import Optional, List

from pyengy.node import Node
from pyengy.util import Context


class PingNode(Node):
    """
    Example custom node that pings to the logger periodically. Instead of storing the accumulated value locally it uses
    the context of the application."""

    def __init__(self, name: str, ping_time: int = 1000, parent: Optional[Node] = None,
                 children: Optional[List[Node]] = None):
        """
        Instantiates a new Ping Node.

        :param name: Name of the node.
        :param ping_time: Ping interval of the node, in milliseconds.
        :param parent: The parent node. If not specified, the node will assume to have no parent or reference.
        :param children: The children nodes. If not specified, the node will not append any children.
        """
        super().__init__(name, parent=parent, children=children)
        self.context_ping_acc_addr = ""
        """Context address of the ping node accumulator. Will be generated on node build."""
        self.ping_time = ping_time
        """Ping interval of the node, can be changed at any point."""

    def _build_self(self, context: Context) -> None:
        super()._build_self(context)
        self.context_ping_acc_addr = "scene.{}.ping_acc".format(self.name)
        context.set(self.context_ping_acc_addr, 0)

    def _update_self(self, delta: float, context: Context) -> None:
        ping_acc = context.get(self.context_ping_acc_addr)
        ping_acc += delta
        if ping_acc > self.ping_time:
            self._logger.info("PING")
            ping_acc -= self.ping_time
        context.set(self.context_ping_acc_addr, ping_acc)
