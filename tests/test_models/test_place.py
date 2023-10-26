#!/usr/bin/python3
"""Unittest for Place model
"""
import unittest
from models.place import Place


class Test_Place_model(unittest.TestCase):
    """
    test class for the Place model.
    """

    def test_init_values(self):
        """test inilaization values for Place model"""

        my_model = Place()
        self.assertEqual(my_model.city_id, "")
        self.assertEqual(my_model.user_id, "")
        self.assertEqual(my_model.name, "")
        self.assertEqual(my_model.description, "")
        self.assertEqual(my_model.number_rooms, 0)
        self.assertEqual(my_model.number_bathrooms, 0)
        self.assertEqual(my_model.price_by_night, 0)
        self.assertEqual(my_model.latitude, 0.0)
        self.assertEqual(my_model.max_guest, 0.0)
        self.assertEqual(my_model.longitude, 0.0)
        self.assertEqual(my_model.amenity_ids, [])
