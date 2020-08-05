"""Contains the App class."""

import threading
from typing import Optional, Tuple

import pygame

from pyengy.node import Node
from pyengy.util import Context, ResourceManager
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

    def __init__(self, name, scene: Node, resource_path: str = "resources", window_size: Tuple[int, int] = (640, 480),
                 fullscreen: bool = False):
        """
        Instantiates a new PyEngy app.

        :param name: The name of the app. Should be unique.
        :param scene: The scene for the app to handle.
        :param resource_path: Path to the resources folder.
        :param window_size: The size of the window.
        :param fullscreen: If true, will set to fullscreen. Otherwise will set to window.
        """
        # Create the app variables and thread
        self.name = name
        self._scene = scene
        self._stop_event = threading.Event()
        self._app = threading.Thread(target=self.__run_app, name=name, daemon=True)

        # Set window parameters
        self._screen = None
        self._window_size = window_size
        self._fullscreen = fullscreen
        self._background = None

        # Set defaults for execution variables
        reset_time(self.name)
        self._previous_time = 0.0
        self._current_time = 0.0
        self._logger = get_logger("", self.name)
        self._context = Context({})
        self._resource_manager = ResourceManager(resource_path)

    def start(self) -> None:
        """Starts the app. Does nothing if the app is already running."""
        if self._app.is_alive():
            self._logger.debug("Trying to start a running app \"{}\"".format(self.name))
            return

        # Reset the time of app
        reset_time(self.name)
        self._logger.debug("Starting app \"{}\"".format(self.name))
        self._previous_time = get_current_time(self.name)
        self._current_time = get_current_time(self.name)

        # Start the thread
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
            },
            "app": {
                "screen": self._screen,
                "resource_manager": self._resource_manager
            }
        })

    def __run_app(self) -> None:
        """Method executed by the app thread. Initializes the app and then calls app loop."""
        # Build the PyGame window
        screen_flags = pygame.DOUBLEBUF
        if self._fullscreen:
            screen_flags = screen_flags | pygame.FULLSCREEN | pygame.HWACCEL
        self._screen = pygame.display.set_mode(self._window_size, screen_flags)

        # Set default background
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill((30, 15, 180))
        self._background = self._background.convert()

        # Build the context and the scene
        self._context = self.__build_context()
        self._scene.build(self._context)

        # Execute the app loop
        self.__app_loop()

    def __app_loop(self) -> None:
        """Internal app loop. Will handle events, updates and renders."""
        while not self._stop_event.is_set():
            self._current_time = get_current_time(self.name)
            delta = self._current_time - self._previous_time

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._stop_event.set()
                else:
                    self._scene.handle_event(event, self._context)

            # Handle updates
            self._scene.update(delta, self._context)

            # Render the app
            self._screen.blit(self._background, (0, 0))
            self._scene.render(delta, self._context)
            pygame.display.flip()

            # Update time for delta next update
            self._previous_time = self._current_time
