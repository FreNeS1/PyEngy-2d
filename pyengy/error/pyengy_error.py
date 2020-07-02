"""Contains the PyEngyError class."""

from __future__ import annotations

from typing import List, Optional

from pyengy.util.time_utils import get_timestamp


class PyEngyError(Exception):
    """Base error for every type of exception raised within the engine. Can handle error composition."""

    def __init__(self, message: str, caused_by: Optional[List[Exception]] = None) -> None:
        """
        Instantiates a new PyEngyError.

        :param message: Human readable description of the error.
        :param caused_by: List of exceptions that caused this one to be raised, if any.
        """
        super().__init__(message)

        self.timestamp = get_timestamp()
        """Timestamp at the time that the error was raised."""
        self.message = message
        """Descriptive human readable message of the error."""
        self.caused_by: List[Exception] = caused_by if caused_by is not None else []
        """List of errors that caused this one to be raised or that this one contains."""

    def __str__(self) -> str:
        error_string = "[{}] PyEngyError: {}.".format(self.timestamp, self.message)
        if len(self.caused_by) != 0:
            error_string += " Caused by: ["
            for error_cause in self.caused_by:
                error_string += "\n  {}".format(self.__string_error_cause(error_cause))
            error_string += "\n]"
        return error_string

    @staticmethod
    def __string_error_cause(error_cause: Exception) -> str:
        """
        Converts an error cause into a string. If error is a PyEngy error, will use custom error format. If not will
        use default error format.

        :param error_cause: The error cause to cast into string
        :return: The error cause as a string
        """
        if isinstance(error_cause, PyEngyError):
            return str(error_cause).replace("\n", "\n  ")
        if error_cause.args[0]:
            return "{}: {}".format(str(error_cause.__class__.__name__), str(error_cause))
        return "Raised exception of type {}".format(str(error_cause.__class__.__name__))
