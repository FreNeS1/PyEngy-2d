"""Contains the test suite for the time utils."""

import unittest
from unittest.mock import Mock

import pyengy
from pyengy.util.time_utils import get_current_time, get_timestamp

MOCK_START_TIME = 1593605662.8467812
MOCK_TIME_TIME = 1593782146.3329251
EXPECTED_CURRENT_TIME = 176483486
EXPECTED_TIMESTAMP = "49:01:23.486"


class TimeUtilsTestSuite(unittest.TestCase):
    """Test cases for the time utils file."""

    @classmethod
    def setUpClass(cls):
        """Mock time and current time values."""
        pyengy.util.time_utils.START_TIME = MOCK_START_TIME
        pyengy.util.time_utils.time = Mock(return_value=MOCK_TIME_TIME)

    def test_get_current_time_returns_current_time_since_start_time(self):
        """
        - Given: Start time
        - When: Calling ``get_current_time``.
        - Then: Should return current time since start time.
        """
        self.assertEqual(EXPECTED_CURRENT_TIME, get_current_time())

    def test_get_timestamp_returns_current_time_since_start_time_in_timestamp_format(self):
        """
        - Given: Start time
        - When: Calling ``get_timestamp``.
        - Then: Should return current timestamp since start time.
        """
        self.assertEqual(EXPECTED_TIMESTAMP, get_timestamp())


if __name__ == '__main__':
    unittest.main()
