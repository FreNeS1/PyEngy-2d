"""Contains the App class."""

import threading
from typing import Optional

from pyengy.node import Node
from pyengy.util.context_utils import Context
from pyengy.util.logger_utils import get_logger
from pyengy.util.time_utils import get_current_time, reset_time

APP_FORCE_STOP_TIMEOUT = 5
"""Timeout for the application stop method in seconds."""


class App:
    """
    Main class of the PyEngy package. This class acts as a controller for a given scene: builds the scene once, and
    then executes a game loop, calling update, render and handle events periodically on the scene.

    The app uses a separate thread to run, that can be controlled with the ``start`` and ``stop`` methods. To wait for
    the app to close or stop, use the ``wait`` method, which will call the join method on the app thread.
    """

    def __init__(self, name, scene: Node):
        """
        Instantiates a new PyEngy app.

        :param name: The name of the app. Should be unique.
        :param scene: The scene for the app to handle.
        """
        self.name = name
        self._scene = scene
        self._stop_event = threading.Event()
        self._app = threading.Thread(target=self.__app_loop, name=name, daemon=True)

        reset_time(self.name)
        self._previous_time = 0.0
        self._current_time = 0.0
        self._logger = get_logger("", self.name)
        self._context = Context({})

    def start(self) -> None:
        """Starts the app. Does nothing if the app is already running."""
        if self._app.is_alive():
            self._logger.debug("Trying to start a running app \"{}\"".format(self.name))
            return

        reset_time(self.name)
        self._logger.debug("Starting app \"{}\"".format(self.name))
        self._previous_time = get_current_time(self.name)
        self._current_time = get_current_time(self.name)
        self._context = self.__build_context()
        self._scene.build(self._context)
        self._stop_event.clear()
        self._app.start()

    def wait(self, timeout: Optional[float] = None) -> None:
        """
        Waits for the app to stop, or for a given timeout.

        :param timeout: The timeout of the wait operation.
        """
        timeout_msg = " with {:.3f}s timeout".format(timeout) if timeout is not None else ""
        self._logger.debug("Waiting for app \"{}\"{}".format(self.name, timeout_msg))
        self._app.join(timeout)

    def stop(self) -> None:
        """Starts the app. Does nothing if the app is already stopped."""
        if not self._app.is_alive():
            self._logger.debug("Trying to stop a non running app \"{}\"".format(self.name))
            return

        self._logger.debug("Stopping app \"{}\"".format(self.name))
        self._stop_event.set()
        self._app.join(APP_FORCE_STOP_TIMEOUT)
        if self._app.is_alive():
            self._logger.warning("App \"{}\" thread did not stop correctly".format(self.name))

    def __build_context(self) -> Context:
        """
        Auxiliary method to build the context of the app.

        :return: The context of the app.
        """
        return Context({
            "metadata": {
                "app_name": self.name
            }
        })

    def __app_loop(self) -> None:
        """Internal method to execute to run an app."""
        while not self._stop_event.is_set():
            self._current_time = get_current_time(self.name)
            delta = self._current_time - self._previous_time

            self._scene.update(delta, self._context)
            self._scene.render(delta, self._context)

            self._previous_time = self._current_time

# if __name__ == '__main__':
#
#     def ping(delta, context):
#         acc = context.get("test.acc")
#         acc += delta
#         if acc > 1000:
#             print("PING")
#             acc -= 1000
#         context.set("test.acc", acc)
#
#
#     s = Node("ROOT", children=[
#         Node("BRANCH1", children=[
#             Node("LEAF11"),
#             Node("LEAF12"),
#         ]),
#         Node("BRANCH2", children=[
#             Node("LEAF21"),
#             Node("LEAF22"),
#             Node("LEAF23"),
#         ])
#     ])
#     app = App("test_app", s)
#     app._context.set("test.acc", 0)
#
#     s.get_node("ROOT/BRANCH1/LEAF12")._update_self = ping
#     app.start()
#     app._context.set("test.acc", 0)
#     app.wait(5)
#     app.stop()
