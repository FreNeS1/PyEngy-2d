"""Contains the test suite for the app class."""
import unittest
from unittest.mock import Mock

from node import Node
from pyengy.app import App


def get_test_app() -> App:
    """
    Auxiliary method to create a test app.

    :return: A test app with a mock scene
    """
    scene = Mock(wraps=Node("SCENE", children=[]))
    return App("test_app", scene)


class AppTestSuite(unittest.TestCase):
    """Test cases for the App class."""

    def test_app_start_starts_if_not_alive(self):
        """
        - Given: An app that is not alive.
        - When: Calling ``start``.
        - Then: Should start the app.
        """
        app = get_test_app()
        app._app.start = Mock()
        app._app.is_alive = lambda: False

        app._stop_event.set()
        app.start()

        app._app.start.assert_called_once()
        self.assertTrue(not app._stop_event.is_set())

    def test_app_start_does_not_start_if_alive(self):
        """
        - Given: An app that is alive.
        - When: Calling ``start``.
        - Then: Should not restart the app.
        """
        app = get_test_app()
        app._app.start = Mock()
        app._app.is_alive = lambda: True

        app._stop_event.set()
        app.start()

        app._app.start.assert_not_called()
        self.assertTrue(app._stop_event.is_set())

    def test_app_wait_with_timeout_calls_join_with_timeout(self):
        """
        - Given: An app that is alive.
        - When: Calling ``wait``.
        - Then: Should relay the call to thread.join with given timeout.
        """
        app = get_test_app()
        app._app.join = Mock()

        timeout = 23.4
        app.wait(timeout)

        app._app.join.assert_called_with(timeout)

    def test_app_stop_sets_stop_flag_if_alive_and_joins_thread(self):
        """
        - Given: An app that is alive.
        - When: Calling ``stop``.
        - Then: Should set the stop flag.
        """
        app = get_test_app()
        app._stop_event.clear()
        app._app.join = Mock()
        app._app.is_alive = lambda: True

        app.stop()

        app._app.join.assert_called_once()
        self.assertTrue(app._stop_event.is_set())

    def test_app_stop_does_not_stop_if_not_alive(self):
        """
        - Given: An app that is not alive.
        - When: Calling ``stop``.
        - Then: Should do nothing.
        """
        app = get_test_app()
        app._stop_event.clear()
        app._app.join = Mock()
        app._app.is_alive = lambda: False

        app.stop()

        app._app.join.assert_not_called()
        self.assertTrue(not app._stop_event.is_set())


if __name__ == '__main__':
    unittest.main()
