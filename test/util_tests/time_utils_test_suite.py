"""Contains the test suite for the time utils."""

import unittest
from unittest.mock import Mock

import pyengy
from pyengy.error import PyEngyError
from pyengy.util.time_utils import get_current_time, get_timestamp, reset_time

MOCK_START_TIME = {"test_app": 1593605674125.1613, "default": 1593605662846.7812}
MOCK_TIME_TIME = 1593782146.3329251

EXPECTED_RESET_START_TIME = MOCK_TIME_TIME * 1000
EXPECTED_CURRENT_TIME = {
    "test_app": MOCK_TIME_TIME * 1000 - MOCK_START_TIME["test_app"],
    "default": MOCK_TIME_TIME * 1000 - MOCK_START_TIME["default"]
}
EXPECTED_TIMESTAMP = {
    "test_app": "49:01:12.207",
    "default": "49:01:23.486"
}


class TimeUtilsTestSuite(unittest.TestCase):
    """Test cases for the time utils file."""

    @classmethod
    def setUp(cls):
        """Mock time and current time values."""
        pyengy.util.time_utils.START_TIME = MOCK_START_TIME
        pyengy.util.time_utils.time = Mock(return_value=MOCK_TIME_TIME)

    def test_reset_time_sets_default_start_time_to_current_time(self):
        """
        - Given: Start time
        - When: Calling ``reset_time``.
        - Then: Should reset the default start time to current time.
        """
        reset_time()

        self.assertEqual(EXPECTED_RESET_START_TIME, pyengy.util.time_utils.START_TIME["default"])
        self.assertEqual(MOCK_START_TIME["test_app"], pyengy.util.time_utils.START_TIME["test_app"])

    def test_reset_time_for_existing_app_sets_start_time_of_app_to_current_time(self):
        """
        - Given: Start time
        - When: Calling ``reset_time`` for a given app that exists.
        - Then: Should reset the app start time to current time.
        """
        reset_time("test_app")

        self.assertEqual(EXPECTED_RESET_START_TIME, pyengy.util.time_utils.START_TIME["test_app"])
        self.assertEqual(MOCK_START_TIME["default"], pyengy.util.time_utils.START_TIME["default"])

    def test_reset_time_for_non_existing_app_sets_start_time_of_app_to_current_time(self):
        """
        - Given: Start time
        - When: Calling ``reset_time`` for a given app that does not exist.
        - Then: Should reset the app start time to current time.
        """
        reset_time("missing_app")

        self.assertEqual(EXPECTED_RESET_START_TIME, pyengy.util.time_utils.START_TIME["missing_app"])

    def test_reset_time_sets_start_time_to_current_time(self):
        """
        - Given: Start time
        - When: Calling ``reset_time`` for a given app.
        - Then: Should reset the start time to current time for given app.
        """
        reset_time("test_app")

        self.assertEqual(EXPECTED_RESET_START_TIME, pyengy.util.time_utils.START_TIME["test_app"])
        self.assertEqual(MOCK_START_TIME["default"], pyengy.util.time_utils.START_TIME["default"])

    def test_get_current_time_returns_current_time_since_default_start_time(self):
        """
        - Given: Start time
        - When: Calling ``get_current_time``.
        - Then: Should return current time since default start time.
        """
        self.assertEqual(EXPECTED_CURRENT_TIME["default"], get_current_time())

    def test_get_current_time_for_existing_app_returns_current_time_since_app_start_time(self):
        """
        - Given: Start time
        - When: Calling ``get_current_time`` for a given app that exists.
        - Then: Should return current time since app start time.
        """
        self.assertEqual(EXPECTED_CURRENT_TIME["test_app"], get_current_time("test_app"))

    def test_get_current_time_for_non_existing_app_should_raise_error(self):
        """
        - Given: Start time
        - When: Calling ``get_current_time`` for a given app that does not exist.
        - Then: Should raise an exception.
        """
        self.assertRaises(PyEngyError, lambda: get_current_time("missing_app"))

    def test_get_timestamp_returns_timestamp_since_default_start_time(self):
        """
        - Given: Start time
        - When: Calling ``get_timestamp``.
        - Then: Should return timestamp since default start time.
        """
        self.assertEqual(EXPECTED_TIMESTAMP["default"], get_timestamp())

    def test_get_timestamp_for_app_returns_timestamp_since_app_start_time(self):
        """
        - Given: Start time
        - When: Calling ``get_current_time`` for a given app that exists.
        - Then: Should return timestamp since app start time.
        """
        self.assertEqual(EXPECTED_TIMESTAMP["test_app"], get_timestamp("test_app"))

    def test_get_timestamp_for_non_existing_app_should_raise_error(self):
        """
        - Given: Start time
        - When: Calling ``get_current_time`` for a given app that does not exist.
        - Then: Should raise an exception.
        """
        self.assertRaises(PyEngyError, lambda: get_timestamp("missing_app"))


if __name__ == '__main__':
    unittest.main()
