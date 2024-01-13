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


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for HBNBCommand class
    documentation and pep8 conformaty"""
    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_console conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_console.py'])
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

# class TestHBNBCommandClassWorking(unittest.TestCase):
#     """unittest class for BaseModel class when everything works"""
#     pass

# class TestHBNBCommandClassBreaking(unittest.TestCase):
#     """unittest class for BaseModel class when everything breaks"""
#     pass
