"""Contains the test suite for the Node 2D Sprite class."""
import unittest
from unittest.mock import Mock

import numpy as np
import pygame
import snapshottest

from pyengy.node import Node2D
from pyengy.node.graphics import Node2DSprite
from pyengy.util import Context, ResourceManager


class Node2DSpriteTestSuite(snapshottest.TestCase):
    """Test cases for the Node 2D Sprite class."""

    def test_init_returns_a_well_defined_node(self):
        """
        - Given: -
        - When: Instantiating a node.
        - Then: Should create a node with correct parameters.
        """
        node = Node2DSprite("NODE_2D_SPRITE_NAME", "TEXTURE_PATH.png", position=(2, 5), rotation=180, scale=(0.5, 0.5),
                            texture_offset=(2, 3), texture_size=None)

        self.assertEqual(id(node), node.id)
        self.assertEqual(True, node.active)
        self.assertEqual(True, node.visible)
        self.assertEqual("NODE_2D_SPRITE_NAME", node.name)
        self.assertEqual("NODE_2D_SPRITE_NAME", node.path)
        self.assertEqual(None, node.parent)
        self.assertEqual(0, len(node.children))
        self.assertEqual((2, 5), node.position)
        self.assertAlmostEqual(180, node.rotation)
        self.assertEqual((0.5, 0.5), node.scale)
        self.assertEqual((2, 5), node.transform.position)
        self.assertAlmostEqual(np.pi, node.transform.rotation)
        self.assertEqual((0.5, 0.5), node.transform.size)
        self.assertEqual((2, 5), node.global_position)
        self.assertAlmostEqual(180, node.global_rotation)
        self.assertEqual((0.5, 0.5), node.global_scale)
        self.assertEqual(node.transform, node.global_transform)
        self.assertEqual("TEXTURE_PATH.png", node.texture_path)
        self.assertEqual((2, 3), node.texture_offset)
        self.assertEqual(None, node.texture_size)

    def test_init_with_parent_returns_a_well_defined_node_structure(self):
        """
        - Given: -
        - When: Instantiating a node tree with parent.
        - Then: Should create a node tree with correct parameters.
        """
        test = Node2DSprite("TEST", "T_TEST.png")
        root = Node2DSprite("ROOT", "T_ROOT.png", position=(10, 5), rotation=90, scale=(2, 1), parent=test)
        branch1 = Node2DSprite("BRANCH1", "T_BRANCH1.png", position=(1, 1), texture_offset=(1, 7), parent=root)
        branch2 = Node2DSprite("BRANCH2", "T_BRANCH2.png", position=(1, -1), texture_size=(10, 10), parent=root)
        leaf11 = Node2DSprite("LEAF11", "T_LEAF11.png", position=(1, 1), parent=branch1)
        leaf12 = Node2DSprite("LEAF12", "T_LEAF12.png", position=(1, 0), parent=branch1)
        leaf21 = Node2DSprite("LEAF21", "T_LEAF21.png", position=(1, 1), parent=branch2)
        leaf22 = Node2DSprite("LEAF22", "T_LEAF22.png", position=(1, 0), parent=branch2)
        leaf23 = Node2DSprite("LEAF23", "T_LEAF23.png", position=(1, -1), parent=branch2)

        self.assertEqual(id(branch2), branch2.id)
        self.assertEqual(True, branch2.active)
        self.assertEqual(True, branch2.visible)
        self.assertEqual("BRANCH2", branch2.name)
        self.assertEqual("TEST/ROOT/BRANCH2", branch2.path)
        self.assertEqual(root, branch2.parent)
        self.assertListEqual([leaf21, leaf22, leaf23], branch2.children)
        self.assertEqual((1, -1), branch2.position)
        self.assertAlmostEqual(0, branch2.rotation)
        self.assertEqual((1, 1), branch2.scale)
        self.assertEqual((1, -1), branch2.transform.position)
        self.assertAlmostEqual(0, branch2.transform.rotation)
        self.assertEqual((1, 1), branch2.transform.size)
        self.assertEqual((11, 7), branch2.global_position)
        self.assertAlmostEqual(90, branch2.global_rotation)
        self.assertEqual((2, 1), branch2.global_scale)
        self.assertEqual((11, 7), branch2.global_transform.position)
        self.assertAlmostEqual((1 / 2) * np.pi, branch2.global_transform.rotation)
        self.assertEqual((2.0, 1), branch2.global_transform.size)
        self.assertEqual("T_BRANCH2.png", branch2.texture_path)
        self.assertEqual((0, 0), branch2.texture_offset)
        self.assertEqual((10, 10), branch2.texture_size)

    def test_init_with_children_returns_a_well_defined_node_structure(self):
        """
        - Given: -
        - When: Instantiating a node tree with children.
        - Then: Should create a node tree with correct parameters.
        """
        leaf11 = Node2DSprite("LEAF11", "T_LEAF11.png", position=(1, -1))
        leaf12 = Node2DSprite("LEAF12", "T_LEAF12.png", position=(1, 0))
        leaf21 = Node2DSprite("LEAF21", "T_LEAF21.png", position=(1, -1))
        leaf22 = Node2DSprite("LEAF22", "T_LEAF22.png", position=(1, 0))
        leaf23 = Node2DSprite("LEAF23", "T_LEAF23.png", position=(1, 1))
        branch1 = Node2DSprite("BRANCH1", "T_BRANCH1.png", texture_offset=(1, 7), children=[leaf11, leaf12])
        branch2 = Node2DSprite("BRANCH2", "T_BRANCH2.png", texture_size=(10, 10), children=[leaf21, leaf22, leaf23])
        root = Node2DSprite("ROOT", "T_ROOT.png", position=(5, 5), rotation=90, children=[branch1, branch2])
        test = Node2DSprite("TEST", "T_TEST.png", children=[root])

        self.assertEqual(id(branch1), branch1.id)
        self.assertEqual(True, branch1.active)
        self.assertEqual(True, branch1.visible)
        self.assertEqual("BRANCH1", branch1.name)
        self.assertEqual("TEST/ROOT/BRANCH1", branch1.path)
        self.assertIs(root, branch1.parent)
        self.assertListEqual([leaf11, leaf12], branch1.children)
        self.assertEqual((0, 0), branch1.position)
        self.assertAlmostEqual(0, branch1.rotation)
        self.assertEqual((1, 1), branch1.scale)
        self.assertEqual((0, 0), branch1.transform.position)
        self.assertAlmostEqual(0, branch1.transform.rotation)
        self.assertEqual((1, 1), branch1.transform.size)
        self.assertEqual((5, 5), branch1.global_position)
        self.assertAlmostEqual(90, branch1.global_rotation)
        self.assertEqual((1, 1), branch1.global_scale)
        self.assertEqual((5, 5), branch1.global_transform.position)
        self.assertAlmostEqual((1 / 2) * np.pi, branch1.global_transform.rotation)
        self.assertEqual((1, 1), branch1.global_transform.size)
        self.assertEqual("T_BRANCH1.png", branch1.texture_path)
        self.assertEqual((1, 7), branch1.texture_offset)
        self.assertEqual(None, branch1.texture_size)

    def test_build_updates_sprite_surface(self):
        """
        - Given: -
        - When: Building a Sprite 2D Node.
        - Then: Should update sprite surface.
        """
        node = Node2DSprite("NODE_2D_SPRITE_NAME", "TEXTURE_PATH.png", texture_offset=(2, 3), texture_size=None)
        node._update_sprite_surface = Mock()

        screen = pygame.display.set_mode((300, 300))
        resource_manager = ResourceManager("test_resources")
        context = Context({
            "metadata": {"app_name": "default"},
            "app": {"screen": screen, "resource_manager": resource_manager}
        })
        node.build(context)

        node._update_sprite_surface.assert_called_once()

    def test_texture_path_updates_sprite_surface(self):
        """
        - Given: -
        - When: Changing a Sprite 2D Node texture path.
        - Then: Should update sprite surface.
        """
        node = Node2DSprite("NODE_2D_SPRITE_NAME", "TEXTURE_PATH.png", texture_offset=(2, 3), texture_size=None)
        node._update_sprite_surface = Mock()

        node.texture_path = "NEW_TEXTURE_PATH.png"

        self.assertEqual("NEW_TEXTURE_PATH.png", node.texture_path)
        node._update_sprite_surface.assert_called_once()

    def test_texture_offset_updates_sprite_surface(self):
        """
        - Given: -
        - When: Changing a Sprite 2D Node texture offset.
        - Then: Should update sprite surface.
        """
        node = Node2DSprite("NODE_2D_SPRITE_NAME", "TEXTURE_PATH.png", texture_offset=(2, 3), texture_size=None)
        node._update_sprite_surface = Mock()

        node.texture_offset = (1, 1)

        self.assertEqual((1, 1), node.texture_offset)
        node._update_sprite_surface.assert_called_once()

    def test_texture_size_updates_sprite_surface(self):
        """
        - Given: -
        - When: Changing a Sprite 2D Node texture path.
        - Then: Should update sprite surface.
        """
        node = Node2DSprite("NODE_2D_SPRITE_NAME", "TEXTURE_PATH.png", texture_offset=(2, 3), texture_size=None)
        node._update_sprite_surface = Mock()

        node.texture_size = (10, 10)

        self.assertEqual((10, 10), node.texture_size)
        node._update_sprite_surface.assert_called_once()

    def test_sprite_render_is_consistent(self):
        """
        - Given: A built sprite scene.
        - When: Creating a sprite display.
        - Then: Should render the display surface consistently.
        """
        root = Node2D("ROOT", position=(50, -60), rotation=15, scale=(5, 2))
        sprite = Node2DSprite("NODE_2D_SPRITE_NAME", "target.png", parent=root, position=(20, 49), rotation=0,
                              scale=(1, 4), texture_offset=(4, 4), texture_size=(24, 24))

        screen = pygame.display.set_mode((300, 300))
        resource_manager = ResourceManager("test_resources")
        context = Context({
            "metadata": {"app_name": "default"},
            "app": {"screen": screen, "resource_manager": resource_manager}
        })
        sprite.build(context)
        sprite.render(100, context)

        self.assertMatchSnapshot(pygame.image.tostring(screen, 'RGBX', False))


if __name__ == '__main__':
    unittest.main()
