#!/usr/bin/python3
"""Unittest for Amenity model
"""
import unittest
from models.amenity import Amenity


class Test_Amenity_model(unittest.TestCase):
    """
    test class for the Amenity modle.
    """
    def test_init_values(self):
        """test inilaization values for Amenity model"""

        my_model = Amenity()
        self.assertEqual(my_model.name, "")
