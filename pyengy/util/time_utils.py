"""
This file contains utility methods for interacting with time. To work correctly this module should be loaded at the
start of the program.

It contains the utility methods:

- ``get_current_time`` - Returns the current execution time in milliseconds.
- ``get_timestamp`` - Returns a timestamp of the current execution time in milliseconds.
"""

from time import time
from typing import Dict

from pyengy.error import PyEngyError

START_TIME: Dict[str, float] = {"default": time() * 1000}
"""The start time of the given apps. Key "default" is used as time reference when no app is given."""

TIMESTAMP_FORMAT: str = "{:02d}:{:02d}:{:02d}.{:03d}"
"""Format of the timestamp. Should be able to display hours, minutes, seconds and millis."""


def reset_time(app: str = "default") -> None:
    """Resets START TIME to current time for a given app."""
    START_TIME[app] = time() * 1000


def get_current_time(app: str = "default") -> float:
    """
    Calculates and returns the current execution time.

    :return: Current time in milliseconds.
    """
    try:
        return (time() * 1000) - START_TIME[app]
    except KeyError as err:
        raise PyEngyError("App \"{}\" does not exist or was not registered".format(app), [err])


def get_timestamp(app: str = "default") -> str:
    """
    Calculates and returns a timestamp for the current execution time.

    :return: Timestamp of current time.
    """
    return __time_to_timestamp(int(get_current_time(app)))


def __time_to_timestamp(time_millis: int) -> str:
    """
    Auxiliary method to create a timestamp from a time in milliseconds.

    :param time_millis: The time in milliseconds.
    :return: The parsed timestamp.
    """
    millis = time_millis % 1000
    seconds = int((time_millis - millis) / 1000 % 60)
    minutes = int(((time_millis - millis) / 1000 - seconds) / 60 % 60)
    hours = int((((time_millis - millis) / 1000 - seconds) / 60 - minutes) / 60)
    return TIMESTAMP_FORMAT.format(hours, minutes, seconds, millis)
