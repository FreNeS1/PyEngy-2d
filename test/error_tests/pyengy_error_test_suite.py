"""Contains the test suite for the time utils."""

import unittest

from pyengy.error import PyEngyError


def raise_(e: Exception):
    """
    Auxiliary method to raise an exception.

    :param e: The exception to raise.
    """
    raise e


class PyEngyErrorTestSuite(unittest.TestCase):
    """Test cases for the PyEngyError class."""

    def test_py_engy_error_can_be_raised(self):
        """
        - Given: -
        - When: Calling a method that raises a PyEngyError.
        - Then: Should raise the PyEngyError.
        """
        self.assertRaises(PyEngyError, lambda: raise_(PyEngyError("Test error")))

    def test_py_engy_error_can_contain_other_errors(self):
        """
        - Given: A group of errors.
        - When: Raising a PyEngyError with contained errors.
        - Then: Should raise the PyEngyError with contained errors.
        """
        err_2_1 = ValueError("Test basic error")
        err_2 = PyEngyError("Test PyEngy error", [err_2_1])
        err_1 = TypeError("Test type error")

        try:
            raise PyEngyError("Test root PyEngy error", [err_1, err_2])
        except PyEngyError as err:
            self.assertListEqual(err.caused_by, [err_1, err_2])

    def test_py_engy_error_can_display_other_errors(self):
        """
        - Given: A group of errors.
        - When: Raising and printing PyEngyError with contained errors.
        - Then: Should print the PyEngyError and the contained errors.
        """
        err_2_1 = ValueError("Test basic error")
        err_2 = PyEngyError("Test PyEngy error", [err_2_1])
        err_1 = TypeError("Test type error")

        try:
            raise PyEngyError("Test root PyEngy error", [err_1, err_2])
        except PyEngyError as err:
            error_string = str(err)
            self.assertIn("Test basic error", error_string)
            self.assertIn("Test PyEngy error", error_string)
            self.assertIn("Test type error", error_string)
            self.assertIn("Test root PyEngy error", error_string)


if __name__ == '__main__':
    unittest.main()
