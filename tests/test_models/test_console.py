#!/usr/bin/python3
"""Unittest for HBNBCommand class
file name: test_console.py
"""
import unittest
import inspect  # test function and module doc string
import pep8  # test pep8 conformance
# from json import dumps, loads #to test the de/serialization
import console
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
import re
from models import storage


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for HBNBCommand class
    documentation and pep8 conformaty"""

    """_models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }
    """

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_console conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        mod_doc = console.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self):
        """test class documentation"""
        mod_doc = str(HBNBCommand.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(HBNBCommand, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(HBNBCommand, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestHBNBCommandClassWorking(unittest.TestCase):
    """unittest class for BaseModel class when everything works
    """
    def test_create(self):
        """test create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            re_match = re.compile(r'^([0-9a-fA-F]{8}-' +
                                  r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                  r'-fA-F]{4}-[0-9a-fA-F]{12})$')
            value = f.getvalue().strip()
            res = re_match.match(value).group().strip()
            print("Expected pattern:", re_match.pattern)

            key = "User." + res
            self.assertIn(key, storage.all())

            self.assertEqual(value, res)

# class TestHBNBCommandClassBreaking(unittest.TestCase):
#     """unittest class for BaseModel class when everything breaks"""
#     pass
