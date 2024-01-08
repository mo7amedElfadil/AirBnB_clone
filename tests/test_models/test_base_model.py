#!/usr/bin/python3
"""Unittest for base_model class
file name: test_base_model.py
"""
import unittest
import inspect  # test function and module doc string
import pep8  # test pep8 conformance
# from json import dumps, loads #to test the de/serialization
from models.base_model import BaseModel


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_base_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        import models.base_model as base_model
        mod_doc = base_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self):
        """test class documentation"""
        mod_doc = str(BaseModel.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(BaseModel, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)

# class TestBaseModelClassWorking(unittest.TestCase):
#     """unittest class for BaseModel class when everything works"""
#     pass

# class TestBaseModelClassBreaking(unittest.TestCase):
#     """unittest class for BaseModel class when everything breaks"""
#     pass
