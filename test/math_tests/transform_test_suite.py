"""Contains the test suite for the transform util."""

import unittest

import numpy as np

from pyengy.math.transform import Transform2D


class TransformTestSuite(unittest.TestCase):
    """Test cases for the Transform class."""

    def test_identity(self):
        """
        - Given: -
        - When: Initializing a transform with the identity method.
        - Then: Should return a transform with an identity matrix, (0, 0) position, 0 rotation and (1, 1).
        """
        i_transform = Transform2D.identity()

        self.assertTrue(np.array_equal(np.eye(3), i_transform.matrix))
        self.assertAlmostEqual(0, i_transform.position[0])
        self.assertAlmostEqual(0, i_transform.position[1])
        self.assertAlmostEqual(0, i_transform.rotation)
        self.assertAlmostEqual(1, i_transform.size[0])
        self.assertAlmostEqual(1, i_transform.size[1])

    def test_transform_normalizes_angles(self):
        """
        - Given: -
        - When: Initializing a transform with a rotation below 0 or above 2π radians.
        - Then: Should normalize to an angle between 0 and 2π radians.
        """
        transform_1 = Transform2D((0, 0), -np.pi, (1, 1))
        transform_2 = Transform2D((0, 0), 5 * np.pi, (1, 1))

        self.assertAlmostEqual(np.pi, transform_1.rotation)
        self.assertAlmostEqual(np.pi, transform_2.rotation)

    def test_transform_normalizes_double_negative_scaling(self):
        """
        - Given: -
        - When: Initializing a transform with a double negative scale.
        - Then: Should normalize to a rotation and a positive scale.
        """
        transform = Transform2D((0, 0), (3 / 2) * np.pi, (-1, -2))

        self.assertAlmostEqual((1 / 2) * np.pi, transform.rotation)
        self.assertAlmostEqual(1, transform.size[0])
        self.assertAlmostEqual(2, transform.size[1])

    def test_transform_move_before_applies_translation_before_transform(self):
        """
        - Given: A transform
        - When: Calling method move with true before flag.
        - Then: Should apply a translation before the transform.
        """
        transform = Transform2D((1, 1), (1 / 2) * np.pi, (1, 2))

        m_transform = transform.move(0, 1, before=True)

        self.assertAlmostEqual(1, m_transform.position[0])
        self.assertAlmostEqual(2, m_transform.position[1])
        self.assertAlmostEqual((1 / 2) * np.pi, m_transform.rotation)
        self.assertAlmostEqual(1, m_transform.size[0])
        self.assertAlmostEqual(2, m_transform.size[1])

    def test_transform_move_after_applies_translation_after_transform(self):
        """
        - Given: A transform
        - When: Calling method move with false before flag.
        - Then: Should apply a translation after the transform.
        """
        transform = Transform2D((1, 1), (1 / 2) * np.pi, (1, 2))

        m_transform = transform.move(0, 1, before=False)

        self.assertAlmostEqual(-1, m_transform.position[0])
        self.assertAlmostEqual(1, m_transform.position[1])
        self.assertAlmostEqual((1 / 2) * np.pi, m_transform.rotation)
        self.assertAlmostEqual(1, m_transform.size[0])
        self.assertAlmostEqual(2, m_transform.size[1])

    def test_transform_rotate_before_applies_rotation_before_transform(self):
        """
        - Given: A transform
        - When: Calling method rotate with true before flag.
        - Then: Should apply a rotation before the transform.
        """
        transform = Transform2D((1, 1), (1 / 2) * np.pi, (1, 2))

        r_transform = transform.rotate(np.pi, before=True)

        self.assertAlmostEqual(-1, r_transform.position[0])
        self.assertAlmostEqual(-1, r_transform.position[1])
        self.assertAlmostEqual((3 / 2) * np.pi, r_transform.rotation)
        self.assertAlmostEqual(1, r_transform.size[0])
        self.assertAlmostEqual(2, r_transform.size[1])

    def test_transform_rotate_after_applies_translation_after_transform(self):
        """
        - Given: A transform
        - When: Calling method rotate with false before flag.
        - Then: Should apply a rotation after the transform.
        """
        transform = Transform2D((1, 1), (1 / 2) * np.pi, (1, 2))

        r_transform = transform.rotate(np.pi, before=False)

        self.assertAlmostEqual(1, r_transform.position[0])
        self.assertAlmostEqual(1, r_transform.position[1])
        self.assertAlmostEqual((3 / 2) * np.pi, r_transform.rotation)
        self.assertAlmostEqual(1, r_transform.size[0])
        self.assertAlmostEqual(2, r_transform.size[1])

    def test_transform_scale_before_applies_scaling_before_transform(self):
        """
        - Given: A transform
        - When: Calling method scale with true before flag.
        - Then: Should apply scaling before the transform.
        """
        transform = Transform2D((1, 1), (1 / 2) * np.pi, (1, 2))

        s_transform = transform.scale(1.5, 1, before=True)

        self.assertAlmostEqual(1.5, s_transform.position[0])
        self.assertAlmostEqual(1, s_transform.position[1])
        self.assertAlmostEqual((1 / 2) * np.pi, s_transform.rotation)
        self.assertAlmostEqual(1, s_transform.size[0])
        self.assertAlmostEqual(3, s_transform.size[1])

    def test_transform_scale_after_applies_scaling_after_transform(self):
        """
        - Given: A transform
        - When: Calling method scale with false before flag.
        - Then: Should apply a rotation after the transform.
        """
        transform = Transform2D((1, 1), (1 / 2) * np.pi, (1, 2))

        s_transform = transform.scale(1.5, 1, before=False)

        self.assertAlmostEqual(1, s_transform.position[0])
        self.assertAlmostEqual(1, s_transform.position[1])
        self.assertAlmostEqual((1 / 2) * np.pi, s_transform.rotation)
        self.assertAlmostEqual(1.5, s_transform.size[0])
        self.assertAlmostEqual(2, s_transform.size[1])

    def test_transform_apply_composes_transforms(self):
        """
        - Given: Some transforms
        - When: Calling apply method with transform.
        - Then: Should compose the transforms into another in order.
        """
        transform_1 = Transform2D((100, 200), (1 / 4) * np.pi, (2, 1))
        transform_2 = Transform2D((200, -100), (-1 / 4) * np.pi, (1, 2))

        g_transform = transform_1.apply(transform_2)

        self.assertAlmostEqual(453.5534, g_transform.position[0], 3)
        self.assertAlmostEqual(412.1319, g_transform.position[1], 3)
        self.assertAlmostEqual(0.32175, g_transform.rotation, 3)
        self.assertAlmostEqual(1.581139, g_transform.size[0], 3)
        self.assertAlmostEqual(3.162277, g_transform.size[1], 3)


if __name__ == '__main__':
    unittest.main()
