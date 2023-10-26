#!/usr/bin/python3
"""Unittest for State model
"""
import unittest
from models.state import State


class Test_State_model(unittest.TestCase):
    """
    test class for the State modle.
    """
    def test_init_values(self):
        """test inilaization values for State model"""

        my_model = State()
        self.assertEqual(my_model.name, "")
