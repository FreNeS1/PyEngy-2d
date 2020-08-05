"""Contains the test suite for the context utils."""

import unittest
from typing import Dict, Any

from pyengy.error import PyEngyError
from pyengy.util.context_utils import Context


def get_test_data() -> Dict[str, Any]:
    """
    Auxiliary method to return test data args.

    :return: Test data.
    """
    return {
        "root": {
            "branch1": {"number": 23, "string": "value"},
            "branch2": {"object": object(), "boolean": True}
        }
    }


class ContextUtilsTestSuite(unittest.TestCase):
    """Test cases for the context class."""

    def test_context_init_saves_given_data(self):
        """
        - Given: Test data
        - When: Initializing context with given data.
        - Then: Should return a context with given data.
        """
        data = get_test_data()
        context = Context(data)

        self.assertIs(data, context.data)

    def test_context_get_returns_value_at_path(self):
        """
        - Given: Context with test data
        - When: Calling ``get`` with an existing key path.
        - Then: Should return the item at given key path.
        """
        data = get_test_data()
        context = Context(data)

        test_dict = context.get("root.branch1")

        self.assertIs(test_dict, data["root"]["branch1"])

    def test_context_get_raises_error_if_path_contains_item(self):
        """
        - Given: Context with test data
        - When: Calling ``get`` with an illegal key path.
        - Then: Should raise an error.
        """
        data = get_test_data()
        context = Context(data)

        self.assertRaises(PyEngyError, lambda: context.get("root.branch2.object.bad_key"))

    def test_context_get_raises_error_if_missing_key_and_raise_if_missing_is_set(self):
        """
        - Given: Context with test data
        - When: Calling ``get`` with a missing key path and raise if missing set.
        - Then: Should raise an error.
        """
        data = get_test_data()
        context = Context(data)

        self.assertRaises(PyEngyError, lambda: context.get("root.branch2.missing", raise_if_missing=True))

    def test_context_get_returns_none_if_missing_key_and_raise_if_missing_is_not_set(self):
        """
        - Given: Context with test data
        - When: Calling ``get`` with a missing key path and raise if missing not set.
        - Then: Should return None.
        """
        data = get_test_data()
        context = Context(data)

        self.assertEqual(None, context.get("root.branch2.missing", raise_if_missing=False))

    def test_context_get_returns_value_if_correct_type(self):
        """
        - Given: Context with test data
        - When: Calling ``get`` with a matching item type.
        - Then: Should return expected item.
        """
        data = get_test_data()
        context = Context(data)

        self.assertEqual(data["root"]["branch2"]["object"], context.get("root.branch2.object", item_type=object))

    def test_context_get_raises_error_if_mismatched_type(self):
        """
        - Given: Context with test data
        - When: Calling ``get`` with a mismatched item type.
        - Then: Should raise an error.
        """
        data = get_test_data()
        context = Context(data)

        self.assertRaises(PyEngyError, lambda: context.get("root.branch2.boolean", item_type=str))

    def test_context_set_changes_value_at_path(self):
        """
        - Given: Context with test data
        - When: Calling ``set`` with an existing key path.
        - Then: Should set the item at given key path.
        """
        data = get_test_data()
        context = Context(data)

        context.set("root.branch1.number", 532)

        self.assertEqual(532, data["root"]["branch1"]["number"])

    def test_context_set_raises_error_if_path_contains_item(self):
        """
        - Given: Context with test data
        - When: Calling ``set`` with an illegal key path.
        - Then: Should raise an error.
        """
        data = get_test_data()
        context = Context(data)

        self.assertRaises(PyEngyError, lambda: context.get("root.branch2.boolean.bad_key"))

    def test_context_set_creates_internal_dicts_if_missing_key(self):
        """
        - Given: Context with test data
        - When: Calling ``set`` with a missing key path.
        - Then: Should set the item at given key path creating any necessary intermediate dicts.
        """
        data = get_test_data()
        context = Context(data)

        context.set("root.branch3.new_key", "new_value")

        self.assertEqual("new_value", data["root"]["branch3"]["new_key"])

    def test_context_remove_deletes_value_at_path(self):
        """
        - Given: Context with test data
        - When: Calling ``remove`` with an existing key path.
        - Then: Should remove and return the item at given key path.
        """
        data = get_test_data()
        context = Context(data)

        removed = context.remove("root.branch1.string")

        self.assertEqual("value", removed)
        self.assertDictEqual({"number": 23}, data["root"]["branch1"])

    def test_context_remove_raises_error_if_path_contains_item(self):
        """
        - Given: Context with test data
        - When: Calling ``remove`` with an illegal key path.
        - Then: Should raise an error.
        """
        data = get_test_data()
        context = Context(data)

        self.assertRaises(PyEngyError, lambda: context.remove("root.branch2.object.bad_key"))

    def test_context_remove_raises_error_if_missing_key_and_raise_if_missing_is_set(self):
        """
        - Given: Context with test data
        - When: Calling ``remove`` with a missing key path and raise if missing set.
        - Then: Should raise an error.
        """
        data = get_test_data()
        context = Context(data)

        self.assertRaises(PyEngyError, lambda: context.remove("root.branch2.missing", raise_if_missing=True))

    def test_context_remove_returns_none_if_missing_key_and_raise_if_missing_is_not_set(self):
        """
        - Given: Context with test data
        - When: Calling ``remove`` with a missing key path and raise if missing not set.
        - Then: Should return None.
        """
        data = get_test_data()
        context = Context(data)

        self.assertEqual(None, context.remove("root.branch2.missing", raise_if_missing=False))


if __name__ == '__main__':
    unittest.main()
