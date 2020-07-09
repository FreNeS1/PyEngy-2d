"""This module wraps some custom utilities over the logger method."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict

from .time_utils import get_timestamp

LOGGER_PREFIX = "pyengy"
"""Prefix for loggers of PyEngy."""

LOG_FILE_FORMAT = "./logs/{}_{}.log"
"""Default format for log files."""

FORMAT = "[{timestamp}] {levelname:>8}: {displayname} - {message}"
"""Default format for loggers of PyEngy."""

CONSOLE_LOGGER_LEVEL = logging.INFO
"""Default log level for console logging of PyEngy."""

FILE_LOGGER_LEVEL = logging.DEBUG
"""Default log level for console logging of PyEngy."""

__INITIALIZED_LOGGERS: Dict[str, PyEngyLoggerWrapper] = {}
"""List of initialized loggers to avoid double initialization."""


def get_logger(name: str = "", app_name: str = "default") -> PyEngyLoggerWrapper:
    """
    Method to create a custom PyEngy logger. This logger should be used for all PyEngy entities within an app. It
    manages console and file output.

    :param app_name: The name of the app. Will be used to create the file log.
    :param name: The name of the logger. Usually the fully qualified name of the entity that is logging.
    :return: A pyengy logger wrapper, that will call the default logger with added information and custom format.
    """
    # Check if logger was already initialized
    logger_id = "{}.{}".format(app_name, name)
    if logger_id in __INITIALIZED_LOGGERS:
        return __INITIALIZED_LOGGERS[logger_id]

    # If not found initialize it
    logger = logging.getLogger(logger_id)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(FORMAT, style="{")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONSOLE_LOGGER_LEVEL)

    file_path = LOG_FILE_FORMAT.format(app_name, datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(FILE_LOGGER_LEVEL)

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Save the initialized logger and return it
    logger_wrapper = PyEngyLoggerWrapper(logger, app_name, name)
    __INITIALIZED_LOGGERS[logger_id] = logger_wrapper
    return logger_wrapper


class PyEngyLoggerWrapper:
    """PyEngy wrapper for the python logger. Should not be initialized directly, but from the ``get_logger`` method."""

    def __init__(self, source_logger: logging.Logger, app_name: str, display_name: str):
        """
        Instantiates a PyEngyLoggerWrapper. Should not be initialized directly, but from the ``get_logger`` method.

        :param source_logger: The default logger to wrap
        :param display_name: The name of the logger. Usually the fully qualified name of the entity that is logging.
        """
        self._logger = source_logger
        """Internal logger of the wrapper."""
        self.display_name = display_name
        """Display name of the logger."""
        self.app_name = app_name
        """Display name of the logger."""

    def debug(self, msg, *args, **kwargs) -> None:
        """
        Log "msg % args" with severity "DEBUG".

        :param msg: The message to log. Can be a format string with "%".
        :param args: Format tuple for the log message if log message is a format string with "%".
        :param kwargs: Keyword arguments of the log. Same as default logger
        """
        parsed_kwargs = self.__parse_kwargs(**kwargs)
        self._logger.debug(msg, *args, **parsed_kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        """
        Log "msg % args" with severity "INFO".

        :param msg: The message to log. Can be a format string with "%".
        :param args: Format tuple for the log message if log message is a format string with "%".
        :param kwargs: Keyword arguments of the log. Same as default logger
        """
        parsed_kwargs = self.__parse_kwargs(**kwargs)
        self._logger.info(msg, *args, **parsed_kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        """
        Log "msg % args" with severity "WARNING".

        :param msg: The message to log. Can be a format string with "%".
        :param args: Format tuple for the log message if log message is a format string with "%".
        :param kwargs: Keyword arguments of the log. Same as default logger
        """
        parsed_kwargs = self.__parse_kwargs(**kwargs)
        self._logger.warning(msg, *args, **parsed_kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        """
        Log "msg % args" with severity "ERROR".

        :param msg: The message to log. Can be a format string with "%".
        :param args: Format tuple for the log message if log message is a format string with "%".
        :param kwargs: Keyword arguments of the log. Same as default logger
        """
        parsed_kwargs = self.__parse_kwargs(**kwargs)
        self._logger.error(msg, *args, **parsed_kwargs)

    def critical(self, msg, *args, **kwargs) -> None:
        """
        Log "msg % args" with severity "CRITICAL".

        :param msg: The message to log. Can be a format string with "%".
        :param args: Format tuple for the log message if log message is a format string with "%".
        :param kwargs: Keyword arguments of the log. Same as default logger
        """
        parsed_kwargs = self.__parse_kwargs(**kwargs)
        self._logger.critical(msg, *args, **parsed_kwargs)

    def __parse_kwargs(self, **kwargs) -> Dict:
        """
        Auxiliary method to append custom information to logger kwargs.

        :param kwargs: THe original kwargs.
        :return: The parsed kwargs.
        """
        parsed_kwargs = kwargs
        parsed_kwargs["extra"] = {} if "extra" not in kwargs else kwargs["extra"]
        parsed_kwargs["extra"]["timestamp"] = get_timestamp(self.app_name)
        parsed_kwargs["extra"]["displayname"] = self.display_name
        return parsed_kwargs
