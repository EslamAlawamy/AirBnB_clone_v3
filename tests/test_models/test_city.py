#!/usr/bin/python3
"""Unittest for City model"""

import unittest
from models.city import City


class Test_City_model(unittest.TestCase):
    """
    test class for the city model.
    """

    my_model = City()

    def test_init_values(self):
        """test inilaization values for City model"""

        self.assertEqual(self.my_model.name, "")
        self.assertEqual(self.my_model.state_id, "")
