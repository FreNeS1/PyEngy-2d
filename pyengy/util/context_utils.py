"""Contains the context class."""

from typing import List, Optional, Type, Dict, Any

from pyengy.error import PyEngyError


class Context:
    """
    The context class is essentially a dictionary of elements with methods to retrieve, set and delete entries with dot
    separated keys, similarly to a propperties object. For example:

    >>> context = Context({"root": {"branch": {"leaf": "value"}}}
    >>> context.get("root.branch.leaf")
    "value"
    >>> context.set("root.branch.leaf", "new_value")
    >>> context.get("root.branch.leaf")
    "new_value"
    >>> context.remove("root.branch.leaf")
    "new_value"
    >>> context.get("root.branch.leaf", raise_if_missing=False)
    None
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize a new Context object with given data.

        :param data: The data to initialize the context with.
        """
        self.data = data

    def __str__(self) -> str:
        context_string = "Context object {"
        for key, value in self.data.items():
            context_string += "\n  {}: {}".format(key, value)
        context_string += "\n}"
        return context_string

    def get(self, path: str, raise_if_missing: bool = True, item_type: Optional[Type] = None) -> Any:
        """
        Retrieve a value with a dot separated path key. For example:

        >>> context = Context({"root": {"branch": {"leaf": "value"}}}
        >>> context.get("root.branch.leaf")
        "value"

        :param path: The dot separated path of the key we want to retrieve.
        :param raise_if_missing: Defines behavior when key is missing. If True, will raise a PyEngyError. Otherwise
                                 will return None.
        :param item_type: Defines the type of the context item. If item is not type will raise a PyEngyError.
        :return: The value of the given key.
        """
        try:
            return self.__retrieve(self.__parse_path(path), item_type)
        except KeyError as err:
            if raise_if_missing:
                raise PyEngyError("Could not retrieve context item at \"{}\", item does not exist".format(path), [err])
            return None
        except TypeError as err:
            raise PyEngyError("Could not retrieve context item at \"{}\", path is illegal".format(path), [err])
        except ValueError as err:
            raise PyEngyError("Bad context item at \"{}\", is not {}".format(path, item_type.__class__.__name__), [err])

    def set(self, path: str, value: Any) -> None:
        """
        Set a value with a dot separated path key. For example:

        >>> context = Context({"root": {"branch": {"leaf": "value"}}}
        >>> context.get("root.branch.leaf")
        "value"
        >>> context.set("root.branch.leaf", "new_value")
        >>> context.get("root.branch.leaf")
        "new_value"

        :param path: The dot separated path of the key we want to retrieve.
        :param value: The value to set the key with.
        """
        try:
            self.__provide(self.__parse_path(path), value)
        except TypeError as err:
            raise PyEngyError("Could not set context item at \"{}\", path is illegal".format(path), [err])

    def remove(self, path: str, raise_if_missing: bool = True) -> Any:
        """
        Remove a value with a dot separated path key from the context. For example:

        >>> context = Context({"root": {"branch": {"leaf": "value"}}}
        >>> context.get("root.branch.leaf")
        "value"
        >>> context.remove("root.branch.leaf")
        "value"
        >>> context.get("root.branch.leaf", raise_if_missing=False)
        None

        :param path: The dot separated path of the key we want to retrieve.
        :param raise_if_missing: Defines behavior when key is missing. If True, will raise a PyEngyError. Otherwise
                                 will return None and ignore the delete operation.
        :return: The value of the deleted key.
        """
        try:
            return self.__delete(self.__parse_path(path))
        except KeyError as err:
            if raise_if_missing:
                raise PyEngyError("Could not delete context item at \"{}\", item does not exist".format(path), [err])
        except TypeError as err:
            raise PyEngyError("Could not delete context item at \"{}\", path is illegal".format(path), [err])

    def __retrieve(self, parsed_path: List[str], item_type: Optional[Type]) -> Any:
        """
        Internal method to retrieve a value from the internal dictionary.

        :param parsed_path: The list of keys to transverse.
        :return: The value from the internal data at the given parsed path.
        """
        current = self.data
        for i in range(0, len(parsed_path) - 1):
            key = parsed_path[i]
            current = current[key]
        item = current[parsed_path[len(parsed_path) - 1]]

        if item_type is not None:
            if not isinstance(item, item_type):
                raise ValueError("Bad item type")

        return item

    def __provide(self, parsed_path: List[str], value: Any) -> None:
        """
        Internal method to set a value from the internal dictionary.

        :param parsed_path: The list of keys to transverse.
        :param value: The value to set.
        """
        current = self.data
        for i in range(0, len(parsed_path) - 1):
            key = parsed_path[i]
            if key in current:
                current = current[key]
            else:
                current[key] = {}
                current = current[key]
        current[parsed_path[len(parsed_path) - 1]] = value

    def __delete(self, parsed_path: List[str]) -> Any:
        """
        Internal method to delete a value from the internal dictionary.

        :param parsed_path: The list of keys to transverse.
        :return: The value deleted from the internal data at the given parsed path.
        """
        current = self.data
        for i in range(0, len(parsed_path) - 1):
            key = parsed_path[i]
            current = current[key]
        val = current[parsed_path[len(parsed_path) - 1]]
        del current[parsed_path[len(parsed_path) - 1]]
        return val

    @staticmethod
    def __parse_path(path) -> List[str]:
        """
        Auxiliary method to parse a dot separated path into a list of keys.

        :param path: The dot separated path.
        :return: The list of keys.
        """
        return path.split(".")
