"""Contains the NodeError class."""

from __future__ import annotations

from typing import List, Optional

from .pyengy_error import PyEngyError


class NodeError(PyEngyError):
    """Error raised when a basic interaction with a node cannot be completed. For example, cyclic node dependencies."""

    def __init__(self, node: str, message: str, caused_by: Optional[List[Exception]] = None) -> None:
        """
        Instantiates a new NodeError.

        :param message: Human readable description of the error.
        :param caused_by: List of exceptions that caused this one to be raised, if any.
        """
        super().__init__(message, caused_by)

        self.node = node
        """Valid identifier of the node that raised the exception. Usually the string representation of the node."""

    def _error_string(self):
        return "NodeError for node ({}): {}.".format(self.node, self.message)
