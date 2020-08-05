"""Contains the ResourceError class."""

from __future__ import annotations

from typing import List, Optional

from .pyengy_error import PyEngyError


class ResourceError(PyEngyError):
    """Error raised when a resource is invalid or cannot be loaded."""

    def __init__(self, res_type: str, res_path: str, message: str, caused_by: Optional[List[Exception]] = None) -> None:
        """
        Instantiates a new ResourceError.

        :param res_type: Type of resource that caused the error.
        :param res_path: Path (identifier) of resource that caused the error.
        :param message: Human readable description of the error.
        :param caused_by: List of exceptions that caused this one to be raised, if any.
        """
        super().__init__(message, caused_by)

        self.resource_type = res_type
        """Type of resource that caused the error."""
        self.resource_path = res_path
        """Path (identifier) of resource that caused the error."""

    def _error_string(self):
        return "ResourceError for {} at \"{}\": {}.".format(self.resource_type, self.resource_path, self.message)
