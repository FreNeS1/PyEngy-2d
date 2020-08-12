"""Contains the test suite for the Node 2D class."""

import unittest

import numpy as np

from pyengy.node import Node2D


class Node2DTestSuite(unittest.TestCase):
    """Test cases for the Node 2D class."""

    def test_init_returns_a_well_defined_node(self):
        """
        - Given: -
        - When: Instantiating a node.
        - Then: Should create a node with correct parameters.
        """
        node = Node2D("NODE_2D_NAME", position=(2, 5), rotation=180, scale=(0.5, 0.5))

        self.assertEqual(id(node), node.id)
        self.assertEqual(True, node.active)
        self.assertEqual(True, node.visible)
        self.assertEqual("NODE_2D_NAME", node.name)
        self.assertEqual("NODE_2D_NAME", node._path)
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
        self.assertEqual(node.global_transform, node.transform)

    def test_init_with_parent_returns_a_well_defined_node_structure(self):
        """
        - Given: -
        - When: Instantiating a node tree with parent.
        - Then: Should create a node tree with correct parameters.
        """
        test = Node2D("TEST")
        root = Node2D("ROOT", position=(10, 5), rotation=90, scale=(2, 1), parent=test)
        branch1 = Node2D("BRANCH1", position=(1, 1), parent=root)
        branch2 = Node2D("BRANCH2", position=(1, -1), parent=root)
        leaf11 = Node2D("LEAF11", position=(1, 1), parent=branch1)
        leaf12 = Node2D("LEAF12", position=(1, 0), parent=branch1)
        leaf21 = Node2D("LEAF21", position=(1, 1), parent=branch2)
        leaf22 = Node2D("LEAF22", position=(1, 0), parent=branch2)
        leaf23 = Node2D("LEAF23", position=(1, -1), parent=branch2)

        self.assertEqual(id(branch2), branch2.id)
        self.assertEqual(True, branch2.active)
        self.assertEqual(True, branch2.visible)
        self.assertEqual("BRANCH2", branch2.name)
        self.assertEqual("TEST/ROOT/BRANCH2", branch2._path)
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

    def test_init_with_children_returns_a_well_defined_node_structure(self):
        """
        - Given: -
        - When: Instantiating a node tree with children.
        - Then: Should create a node tree with correct parameters.
        """
        leaf11 = Node2D("LEAF11", position=(1, -1))
        leaf12 = Node2D("LEAF12", position=(1, 0))
        leaf21 = Node2D("LEAF21", position=(1, -1))
        leaf22 = Node2D("LEAF22", position=(1, 0))
        leaf23 = Node2D("LEAF23", position=(1, 1))
        branch1 = Node2D("BRANCH1", position=(1, 1), children=[leaf11, leaf12])
        branch2 = Node2D("BRANCH2", position=(1, -1), children=[leaf21, leaf22, leaf23])
        root = Node2D("ROOT", position=(5, 5), rotation=90, scale=(3, 1), children=[branch1, branch2])
        test = Node2D("TEST", children=[root])

        self.assertEqual(id(branch1), branch1.id)
        self.assertEqual(True, branch1.active)
        self.assertEqual(True, branch1.visible)
        self.assertEqual("BRANCH1", branch1.name)
        self.assertEqual("TEST/ROOT/BRANCH1", branch1._path)
        self.assertIs(root, branch1.parent)
        self.assertListEqual([leaf11, leaf12], branch1.children)
        self.assertEqual((1, 1), branch1.position)
        self.assertAlmostEqual(0, branch1.rotation)
        self.assertEqual((1, 1), branch1.scale)
        self.assertEqual((1, 1), branch1.transform.position)
        self.assertAlmostEqual(0, branch1.transform.rotation)
        self.assertEqual((1, 1), branch1.transform.size)
        self.assertEqual((4, 8), branch1.global_position)
        self.assertAlmostEqual(90, branch1.global_rotation)
        self.assertEqual((3, 1), branch1.global_scale)
        self.assertEqual((4, 8), branch1.global_transform.position)
        self.assertAlmostEqual((1 / 2) * np.pi, branch1.global_transform.rotation)
        self.assertEqual((3, 1), branch1.global_transform.size)

    def test_set_position_updates_transform(self):
        """
        - Given: A 2D node.
        - When: Updating the position.
        - Then: Should update its transform.
        """
        node = Node2D("NODE", position=(6, 5), rotation=180, scale=(-1, 1))
        node.position = (1, 54)

        self.assertEqual((1, 54), node.position)
        self.assertEqual((1, 54), node.transform.position)

    def test_set_rotation_updates_transform(self):
        """
        - Given: A 2D node.
        - When: Updating the rotation.
        - Then: Should update its transform.
        """
        node = Node2D("NODE", position=(6, 5), rotation=180, scale=(-1, 1))
        node.rotation = 270

        self.assertEqual(270, node.rotation)
        self.assertEqual((3 / 2) * np.pi, node.transform.rotation)

    def test_set_size_updates_transform(self):
        """
        - Given: A 2D node.
        - When: Updating the size.
        - Then: Should update its transform.
        """
        node = Node2D("NODE", position=(6, 5), rotation=180, scale=(-1, 1))
        node.scale = (-1, 2)

        self.assertEqual((-1, 2), node.scale)
        self.assertEqual((-1, 2), node.transform.size)

    def test_set_parent_updates_transform(self):
        """
        - Given: A parent 2D node.
        - When: Setting a node as a child of another.
        - Then: Should update its global transform.
        """
        parent = Node2D("PARENT", position=(1, 5), rotation=0, scale=(0.5, 0.5))
        child = Node2D("CHILD", position=(2, 4), rotation=0, scale=(1, 1))
        parent.add_child(child)

        self.assertEqual((2, 4), child.position)
        self.assertAlmostEqual(0, child.rotation)
        self.assertEqual((1, 1), child.scale)
        self.assertEqual((2, 7), child.global_position)
        self.assertAlmostEqual(0, child.global_rotation)
        self.assertEqual((0.5, 0.5), child.global_scale)

    def test_update_parent_updates_transform(self):
        """
        - Given: A parent 2D node.
        - When: Updating the parameters of the parent.
        - Then: Should update its children.
        """
        parent = Node2D("PARENT", position=(2, 3), rotation=0, scale=(1, 1))
        child = Node2D("CHILD", parent=parent, position=(6, 0), rotation=0, scale=(2, 1))
        parent.scale = (0.5, 0.5)

        self.assertEqual((6, 0), child.position)
        self.assertAlmostEqual(0, child.rotation)
        self.assertEqual((2, 1), child.scale)
        self.assertEqual((5, 3), child.global_position)
        self.assertAlmostEqual(0, child.global_rotation)
        self.assertEqual((1, 0.5), child.global_scale)


if __name__ == '__main__':
    unittest.main()
