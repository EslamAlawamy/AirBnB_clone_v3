#!/usr/bin/python3
"""Unittest for User model"""

import unittest
from models.user import User


class Test_User_model(unittest.TestCase):
    """
    test class for the User model.
    """

    def test_init_values(self):
        """test inilaization values for User model"""

        my_model = User()
        self.assertEqual(my_model.first_name, "")
        self.assertEqual(my_model.last_name, "")
        self.assertEqual(my_model.email, "")
        self.assertEqual(my_model.password, "")
