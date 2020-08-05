"""Contains the test suite for the resource utils."""

import unittest

import pygame
import snapshottest

from pyengy.error import ResourceError
from pyengy.util import ResourceManager


class ResourceManagerTestSuite(snapshottest.TestCase):
    """Test cases for the resource manager class."""

    def test_resource_manager_retrieves_image_resources(self):
        """
        - Given: An image
        - When: Retrieving the image through resource manager.
        - Then: Should store resource path and resource dictionary.
        """
        pygame.display.set_mode((100, 100))
        resource_manager = ResourceManager("test_resources")
        test_image = resource_manager.get_image("target.png")

        self.assertMatchSnapshot(pygame.image.tostring(test_image, 'RGBX', False))

    def test_resource_manager_passes_image_resources_by_reference(self):
        """
        - Given: An image
        - When: Retrieving the image through resource manager multiple times.
        - Then: Should retrieve the same image resource instance.
        """
        pygame.display.set_mode((100, 100))
        resource_manager = ResourceManager("test_resources")
        test_image_1 = resource_manager.get_image("target.png")
        test_image_2 = resource_manager.get_image("target.png")
        test_image_3 = resource_manager.get_image("target.png")

        self.assertIs(test_image_1, test_image_2)
        self.assertIs(test_image_2, test_image_3)

    def test_resource_manager_raises_error_if_no_resource(self):
        pygame.display.set_mode((100, 100))
        resource_manager = ResourceManager("test_resources")

        self.assertRaises(ResourceError, lambda: resource_manager.get_image("missing_image.png"))


if __name__ == '__main__':
    unittest.main()
