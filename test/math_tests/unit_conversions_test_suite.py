"""Contains the test suite for the unit conversion utils."""

import unittest

import numpy as np

from pyengy.math.unit_conversions import degrees_to_radians, radians_to_degrees

DEGREES_RADIANS_TESTS = [(0, 0), ((1 / 2) * np.pi, 90), (np.pi, 180), ((3 / 2) * np.pi, 270), (2 * np.pi, 360)]
"""Degrees to radians and radians to degrees test cases."""


class UnitConversionTestSuite(unittest.TestCase):
    """Test cases for the unit conversion methods."""

    def test_degrees_to_radians(self):
        """
        - Given: -
        - When: Transforming some angles from degrees to radians.
        - Then: Utility returns correct response.
        """
        for test in DEGREES_RADIANS_TESTS:
            self.assertAlmostEqual(test[0], degrees_to_radians(test[1]))

    def test_radians_to_degrees(self):
        """
        - Given: -
        - When: Transforming some angles from radians to degrees.
        - Then: Utility returns correct response.
        """
        for test in DEGREES_RADIANS_TESTS:
            self.assertAlmostEqual(test[1], radians_to_degrees(test[0]))


if __name__ == '__main__':
    unittest.main()
