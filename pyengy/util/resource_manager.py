"""Contains the ResourceManager class."""

import os
from typing import Dict

import pygame

from pyengy.error import ResourceError

IMAGES_PATH = "images"
"""Default parent path for image type resources."""


class ResourceManager:
    """
    Basic resource manager. Will load each resource once and pass by reference to nodes that require the resource.
    Each resource is identified by it's path. When loading resources, requires the relative path with file extension.
    """

    def __init__(self, resources_path: str):
        """
        Initializes a new resource manager with a default resources path.

        :param resources_path: The absolute or relative path from the execution to the app resources.
        """
        self._resources_path = resources_path
        self._images: Dict[str, pygame.Surface] = {}

    def get_image(self, path: str) -> pygame.Surface:
        """
        Retrieves an image resource. If the resource requires modification make a copy of it first to avoid modifying
        the manager version.

        :param path: The image path, relative to the images folder, to load and/or retrieve.
        :return: The loaded and converted PyGame Surface.
        """
        if path in self._images:
            return self._images[path]

        resource_full_path = os.path.join(self._resources_path, IMAGES_PATH, path)
        try:
            raw_image = pygame.image.load(resource_full_path)
            image = raw_image.convert_alpha()
            self._images[path] = image
            return image
        except (pygame.error, FileNotFoundError) as e:
            raise ResourceError("IMAGE", resource_full_path, "Could not load resource", [e])

    def clear_image(self, path: str) -> None:
        """
        Clears an image resource, unloading it from the manager.

        :param path: The image path, relative to the images folder, to clear.
        """
        if path in self._images:
            del self._images[path]
