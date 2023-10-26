#!/usr/bin/python3
"""Unittest for Review model"""

import unittest
from models.review import Review


class Test_Review_model(unittest.TestCase):
    """
    test class for the review modle.
    """

    def test_init_values(self):
        """test inilaization values for review model"""

        my_model = Review()
        self.assertEqual(my_model.text, "")
        self.assertEqual(my_model.place_id, "")
        self.assertEqual(my_model.user_id, "")
