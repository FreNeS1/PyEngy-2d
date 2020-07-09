"""Contains the test suite for the base node class."""

import unittest
from unittest.mock import MagicMock

from pygame.event import Event

from pyengy.error import NodeError
from pyengy.node import Node
from pyengy.util.context_utils import Context


def create_node_tree():
    """
    Auxiliary method to return an already prebuild node tree.

    :return: A node tree with a root, 2 branches and 5 leafs.
    """
    return Node("ROOT", children=[
        Node("BRANCH1", children=[
            Node("LEAF11"),
            Node("LEAF12"),
        ]),
        Node("BRANCH2", children=[
            Node("LEAF21"),
            Node("LEAF22"),
            Node("LEAF23"),
        ])
    ])


class NodeTestSuite(unittest.TestCase):
    """Test cases for the Node class."""

    def test_init_returns_a_well_defined_node(self):
        """
        - Given: -
        - When: Instantiating a node.
        - Then: Should create a node with correct parameters.
        """
        node = Node("NODE_NAME")

        self.assertEqual(id(node), node.id)
        self.assertEqual(True, node.active)
        self.assertEqual(True, node.visible)
        self.assertEqual("NODE_NAME", node.name)
        self.assertEqual("NODE_NAME", node.path)
        self.assertEqual(None, node.parent)
        self.assertEqual(0, len(node.children))

    def test_init_with_parent_returns_a_well_defined_node_structure(self):
        """
        - Given: -
        - When: Instantiating a node tree with parent.
        - Then: Should create a node tree with correct parameters.
        """
        test = Node("TEST")
        root = Node("ROOT", parent=test)
        branch1 = Node("BRANCH1", parent=root)
        branch2 = Node("BRANCH2", parent=root)
        leaf11 = Node("LEAF11", parent=branch1)
        leaf12 = Node("LEAF12", parent=branch1)
        leaf21 = Node("LEAF21", parent=branch2)
        leaf22 = Node("LEAF22", parent=branch2)
        leaf23 = Node("LEAF23", parent=branch2)

        self.assertEqual(id(branch2), branch2.id)
        self.assertEqual(True, branch2.active)
        self.assertEqual(True, branch2.visible)
        self.assertEqual("BRANCH2", branch2.name)
        self.assertEqual("TEST/ROOT/BRANCH2", branch2.path)
        self.assertEqual(root, branch2.parent)
        self.assertListEqual([leaf21, leaf22, leaf23], branch2.children)

    def test_init_with_children_returns_a_well_defined_node_structure(self):
        """
        - Given: -
        - When: Instantiating a node tree with children.
        - Then: Should create a node tree with correct parameters.
        """
        leaf11 = Node("LEAF11")
        leaf12 = Node("LEAF12")
        leaf21 = Node("LEAF21")
        leaf22 = Node("LEAF22")
        leaf23 = Node("LEAF23")
        branch1 = Node("BRANCH1", children=[leaf11, leaf12])
        branch2 = Node("BRANCH2", children=[leaf21, leaf22, leaf23])
        root = Node("ROOT", children=[branch1, branch2])
        test = Node("TEST", children=[root])

        self.assertEqual(id(branch1), branch1.id)
        self.assertEqual(True, branch1.active)
        self.assertEqual(True, branch1.visible)
        self.assertEqual("BRANCH1", branch1.name)
        self.assertEqual("TEST/ROOT/BRANCH1", branch1.path)
        self.assertIs(root, branch1.parent)
        self.assertListEqual([leaf11, leaf12], branch1.children)

    def test_init_when_cyclic_dependency_raises_exception(self):
        """
        - Given: -
        - When: Instantiating a node tree with a cyclic dependency.
        - Then: Should throw an exception.
        """
        a = Node("A", parent=None)
        b = Node("B", parent=a)

        self.assertRaises(NodeError, lambda: Node("C", parent=b, children=[a]))

    def test_init_when_name_collision_raises_exception(self):
        """
        - Given: -
        - When: Instantiating a node tree with a cyclic dependency.
        - Then: Should throw an exception.
        """
        a = Node("A", parent=None)
        b = Node("B", parent=a)

        self.assertRaises(NodeError, lambda: Node("B", parent=a))

    def test_get_node_with_existing_id_returns_node(self):
        """
        - Given: A node tree structure.
        - When: Retrieving node by id that exists.
        - Then: Should retrieve the node.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        leaf11 = [n for n in branch1.children if n.name == "LEAF11"][0]
        leaf12 = [n for n in branch1.children if n.name == "LEAF12"][0]

        self.assertIs(leaf12.get_node(leaf11.id), leaf11)

    def test_get_node_with_non_existing_id_returns_none(self):
        """
        - Given: A node tree structure.
        - When: Retrieving node by id that does not exist.
        - Then: Should return None.
        """
        root = create_node_tree()

        self.assertIsNone(root.get_node(-1))

    def test_get_node_with_existing_absolute_path_returns_node(self):
        """
        - Given: A node tree structure.
        - When: Retrieving node by absolute path that exists.
        - Then: Should retrieve the node.
        """
        root = create_node_tree()
        branch2 = [n for n in root.children if n.name == "BRANCH2"][0]
        leaf21 = [n for n in branch2.children if n.name == "LEAF21"][0]
        leaf23 = [n for n in branch2.children if n.name == "LEAF23"][0]

        self.assertIs(leaf23.get_node("ROOT/BRANCH2/LEAF21"), leaf21)

    def test_get_node_with_missing_path_returns_none(self):
        """
        - Given: A node tree structure.
        - When: Retrieving node by path that does not exist.
        - Then: Should return None.
        """
        root = create_node_tree()

        self.assertIsNone(root.get_node("ROOT/BRANCH2/LEAF12"))

    def test_set_parent_to_none_resets_old_parent(self):
        """
        - Given: A node tree structure.
        - When: Setting node parent to None.
        - Then: Should reset old parent and set new one.
        """
        root = create_node_tree()
        branch2 = [n for n in root.children if n.name == "BRANCH2"][0]
        leaf23 = [n for n in branch2.children if n.name == "LEAF23"][0]

        leaf23.set_parent(None)

        self.assertIs(None, leaf23.parent)
        self.assertEqual("LEAF23", leaf23.path)
        self.assertNotIn(leaf23, branch2.children)

    def test_set_parent_node_sets_node_parent_and_resets_old_parent(self):
        """
        - Given: A node tree structure.
        - When: Setting node parent to an existing node.
        - Then: Should reset old parent and set new one.
        """
        root = create_node_tree()
        branch2 = [n for n in root.children if n.name == "BRANCH2"][0]
        leaf23 = [n for n in branch2.children if n.name == "LEAF23"][0]

        leaf23.set_parent(root)

        self.assertIs(root, leaf23.parent)
        self.assertEqual("ROOT/LEAF23", leaf23.path)
        self.assertIn(leaf23, root.children)
        self.assertNotIn(leaf23, branch2.children)

    def test_set_parent_node_with_cyclic_dependency_raises_error(self):
        """
        - Given: A node tree structure.
        - When: Setting node parent to an existing node creating a cyclic dependency.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        leaf11 = [n for n in branch1.children if n.name == "LEAF11"][0]

        self.assertRaises(NodeError, lambda: root.set_parent(leaf11))

    def test_set_parent_node_with_name_collision_raises_error(self):
        """
        - Given: A node tree structure.
        - When: Setting node parent to an existing node creating a name collision.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]

        new_leaf11 = Node("LEAF11")
        self.assertRaises(NodeError, lambda: new_leaf11.set_parent(branch1))

    def test_set_children_to_none_resets_old_parent(self):
        """
        - Given: A node tree structure.
        - When: Setting node children to None.
        - Then: Should reset old children and set new one.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        branch2 = [n for n in root.children if n.name == "BRANCH2"][0]

        root.set_children(None)

        self.assertIs(None, branch1.parent)
        self.assertIs(None, branch2.parent)
        self.assertEqual("BRANCH1", branch1.path)
        self.assertEqual("BRANCH2", branch2.path)
        self.assertNotIn(branch1, root.children)
        self.assertNotIn(branch2, root.children)

    def test_set_children_nodes_sets_node_children_and_resets_old_parent(self):
        """
        - Given: A node tree structure.
        - When: Setting node children to an existing node.
        - Then: Should reset old children and set new ones.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        branch2 = [n for n in root.children if n.name == "BRANCH2"][0]
        leaf11 = [n for n in branch1.children if n.name == "LEAF11"][0]
        leaf12 = [n for n in branch1.children if n.name == "LEAF12"][0]

        root.set_children([branch1, branch2, leaf11, leaf12])

        self.assertIs(root, branch1.parent)
        self.assertIs(root, branch2.parent)
        self.assertIs(root, leaf11.parent)
        self.assertIs(root, leaf12.parent)
        self.assertEqual("ROOT/BRANCH1", branch1.path)
        self.assertEqual("ROOT/BRANCH2", branch2.path)
        self.assertEqual("ROOT/LEAF11", leaf11.path)
        self.assertEqual("ROOT/LEAF12", leaf12.path)
        self.assertIn(branch1, root.children)
        self.assertIn(branch2, root.children)
        self.assertIn(leaf11, root.children)
        self.assertIn(leaf12, root.children)
        self.assertNotIn(leaf11, branch1.children)
        self.assertNotIn(leaf12, branch1.children)

    def test_set_children_node_with_cyclic_dependency_raises_error(self):
        """
        - Given: A node tree structure.
        - When: Setting node children to an existing node creating a cyclic dependency.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        leaf12 = [n for n in branch1.children if n.name == "LEAF12"][0]

        self.assertRaises(NodeError, lambda: leaf12.set_children([root]))

    def test_set_children_nodes_with_name_collision_raises_error(self):
        """
        - Given: A node tree structure.
        - When: Setting node children to an existing node creating a name collision.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        branch2 = [n for n in root.children if n.name == "BRANCH2"][0]

        new_branch2 = Node("BRANCH2")
        self.assertRaises(NodeError, lambda: root.set_children([branch1, branch2, new_branch2]))

    def test_add_child_node_sets_node_as_child_and_resets_old_parent(self):
        """
        - Given: A node tree structure.
        - When: Adding node as a child to an existing node.
        - Then: Should reset old parent and set itself as child.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        branch2 = [n for n in root.children if n.name == "BRANCH2"][0]
        leaf23 = [n for n in branch2.children if n.name == "LEAF23"][0]

        branch1.add_child(leaf23)

        self.assertIs(branch1, leaf23.parent)
        self.assertEqual("ROOT/BRANCH1/LEAF23", leaf23.path)
        self.assertIn(leaf23, branch1.children)
        self.assertNotIn(leaf23, branch2.children)

    def test_add_child_node_with_cyclic_dependency_raises_error(self):
        """
        - Given: A node tree structure.
        - When: Adding node child to an existing node creating a cyclic dependency.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        leaf11 = [n for n in branch1.children if n.name == "LEAF11"][0]

        self.assertRaises(NodeError, lambda: leaf11.add_child(root))

    def test__add_child_node_with_name_collision_raises_error(self):
        """
        - Given: A node tree structure.
        - When: Setting node parent to an existing node creating a name collision.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]

        new_leaf11 = Node("LEAF11")
        self.assertRaises(NodeError, lambda: branch1.add_child(new_leaf11))

    def test_remove_child_node_with_existing_id_resets_parent(self):
        """
        - Given: A node tree structure.
        - When: Removing a child node with an existing id.
        - Then: Should reset old parent and set itself as child.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        leaf12 = [n for n in branch1.children if n.name == "LEAF12"][0]

        branch1.remove_child(leaf12.id)

        self.assertIsNone(leaf12.parent)
        self.assertEqual("LEAF12", leaf12.path)
        self.assertNotIn(leaf12, branch1.children)

    def test_remove_child_node_with_non_existing_id_raises_exception(self):
        """
        - Given: A node tree structure.
        - When: Removing a child node with an non existing id.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]

        self.assertRaises(NodeError, lambda: branch1.remove_child(-1))

    def test_remove_child_node_with_existing_name_resets_parent(self):
        """
        - Given: A node tree structure.
        - When: Removing a child node with an existing name.
        - Then: Should reset old parent and set itself as child.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        leaf12 = [n for n in branch1.children if n.name == "LEAF12"][0]

        branch1.remove_child(leaf12.name)

        self.assertIsNone(leaf12.parent)
        self.assertEqual("LEAF12", leaf12.path)
        self.assertNotIn(leaf12, branch1.children)

    def test_remove_child_node_with_non_existing_name_raises_exception(self):
        """
        - Given: A node tree structure.
        - When: Removing a child node with an non existing name.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]

        self.assertRaises(NodeError, lambda: branch1.remove_child(""))

    def test_remove_child_node_with_existing_instance_resets_parent(self):
        """
        - Given: A node tree structure.
        - When: Removing a child node with an existing instance.
        - Then: Should reset old parent and set itself as child.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]
        leaf12 = [n for n in branch1.children if n.name == "LEAF12"][0]

        branch1.remove_child(leaf12)

        self.assertIsNone(leaf12.parent)
        self.assertEqual("LEAF12", leaf12.path)
        self.assertNotIn(leaf12, branch1.children)

    def test_remove_child_node_with_non_existing_instance_raises_exception(self):
        """
        - Given: A node tree structure.
        - When: Removing a child node with an non existing instance.
        - Then: Should raise an exception.
        """
        root = create_node_tree()
        branch1 = [n for n in root.children if n.name == "BRANCH1"][0]

        self.assertRaises(NodeError, lambda: branch1.remove_child(Node("")))

    def test_build_node_calls_self_build(self):
        """
        - Given: A node tree structure.
        - When: Calling render on a node.
        - Then: Should handle event self and children.
        """
        context = Context({})
        node = Node("NODE")
        child = Node("CHILD", parent=node)
        node._build_self = MagicMock()
        child._build_self = MagicMock()

        node.build(context)

        node._build_self.assert_called_with(context)
        child._build_self.assert_called_with(context)

    def test_render_node_calls_self_render(self):
        """
        - Given: A node tree structure.
        - When: Calling render on a node.
        - Then: Should handle event self and children.
        """
        delta = 12.1248
        context = Context({})
        node = Node("NODE")
        child = Node("CHILD", parent=node)
        node._render_self = MagicMock()
        child._render_self = MagicMock()

        node.render(delta, context)

        node._render_self.assert_called_with(delta, context)
        child._render_self.assert_called_with(delta, context)

    def test_render_invisible_node_does_not_call_self_render(self):
        """
        - Given: A node tree structure.
        - When: Calling render on an invisible node.
        - Then: Should not render self or children.
        """
        delta = 12.1248
        context = Context({})
        node = Node("NODE")
        child = Node("CHILD", parent=node)
        node._render_self = MagicMock()
        child._render_self = MagicMock()

        node.visible = False
        node.render(delta, context)

        node._render_self.assert_not_called()
        child._render_self.assert_not_called()

    def test_update_node_calls_self_update(self):
        """
        - Given: A node tree structure.
        - When: Calling update on a node.
        - Then: Should update self and children.
        """
        delta = 12.1248
        context = Context({})
        node = Node("NODE")
        child = Node("CHILD", parent=node)
        node._update_self = MagicMock()
        child._update_self = MagicMock()

        node.update(delta, context)

        node._update_self.assert_called_with(delta, context)
        child._update_self.assert_called_with(delta, context)

    def test_update_inactive_node_does_not_call_self_update(self):
        """
        - Given: A node tree structure.
        - When: Calling update on an inactive node.
        - Then: Should not update self or children.
        """
        delta = 12.1248
        context = Context({})
        node = Node("NODE")
        child = Node("CHILD", parent=node)
        node._update_self = MagicMock()
        child._update_self = MagicMock()

        node.active = False
        node.update(delta, context)

        node._update_self.assert_not_called()
        child._update_self.assert_not_called()

    def test_handle_event_node_calls_self_handle_event(self):
        """
        - Given: A node tree structure.
        - When: Calling handle event on a node.
        - Then: Should handle event self and children.
        """
        event = Event(-1, {})
        context = Context({})
        node = Node("NODE")
        child = Node("CHILD", parent=node)
        node._handle_event_self = MagicMock()
        child._handle_event_self = MagicMock()

        node.handle_event(event, context)

        node._handle_event_self.assert_called_with(event, context)
        child._handle_event_self.assert_called_with(event, context)

    def test_handle_event_inactive_node_does_not_call_self_handle_event(self):
        """
        - Given: A node tree structure.
        - When: Calling handle event on an inactive node.
        - Then: Should not handle event self or children.
        """
        event = Event(-1, {})
        context = Context({})
        node = Node("NODE")
        child = Node("CHILD", parent=node)
        node._handle_event_self = MagicMock()
        child._handle_event_self = MagicMock()

        node.active = False
        node.handle_event(event, context)

        node._handle_event_self.assert_not_called()
        child._handle_event_self.assert_not_called()


if __name__ == '__main__':
    unittest.main()
