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
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


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


class TestHBNBCommandClassWorking(unittest.TestCase):
    """unittest class for BaseModel class when everything works
    """
    def setUp(self):
        """ instanciate widely used variables
        """
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.show_pattern = re.compile(r'(\[([^]]+)\] \(([^)]+)\) (\{.+\}))')
        
        self.cls = BaseModel()
        self.usr = User()
        self.stt = State()
        self.ct = City()
        self.amnty = Amenity()
        self.plc = Place()
        self.rvw = Review()


    def test_create_User(self):
        """test create() on User class
        """
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        
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

    
    def test_create_BaseModel(self):
        """test create() on BaseModel class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            re_match = re.compile(r'^([0-9a-fA-F]{8}-' +
                                  r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                  r'-fA-F]{4}-[0-9a-fA-F]{12})$')
            value = f.getvalue().strip()
            res = re_match.match(value).group().strip()
            # print("Expected pattern:", re_match.pattern)

            key = "BaseModel." + res
            self.assertIn(key, storage.all())

            self.assertEqual(value, res)

    def test_create_State(self):
        """test create() on  State class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            re_match = re.compile(r'^([0-9a-fA-F]{8}-' +
                                  r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                  r'-fA-F]{4}-[0-9a-fA-F]{12})$')
            value = f.getvalue().strip()
            res = re_match.match(value).group().strip()
            # print("Expected pattern:", re_match.pattern)

            key = "State." + res
            self.assertIn(key, storage.all())

            self.assertEqual(value, res)
    
    def test_create_City(self):
        """test create() on City class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            re_match = re.compile(r'^([0-9a-fA-F]{8}-' +
                                  r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                  r'-fA-F]{4}-[0-9a-fA-F]{12})$')
            value = f.getvalue().strip()
            res = re_match.match(value).group().strip()
            # print("Expected pattern:", re_match.pattern)

            key = "City." + res
            self.assertIn(key, storage.all())

            self.assertEqual(value, res)

    def test_create_Amenity(self):
        """test create() on BaseModel class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            re_match = re.compile(r'^([0-9a-fA-F]{8}-' +
                                  r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                  r'-fA-F]{4}-[0-9a-fA-F]{12})$')
            value = f.getvalue().strip()
            res = re_match.match(value).group().strip()
            # print("Expected pattern:", re_match.pattern)

            key = "Amenity." + res
            self.assertIn(key, storage.all())

            self.assertEqual(value, res)

    def test_create_Place(self):
        """test create() on BaseModel class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            re_match = re.compile(r'^([0-9a-fA-F]{8}-' +
                                  r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                  r'-fA-F]{4}-[0-9a-fA-F]{12})$')
            value = f.getvalue().strip()
            res = re_match.match(value).group().strip()
            # print("Expected pattern:", re_match.pattern)

            key = "Place." + res
            self.assertIn(key, storage.all())

            self.assertEqual(value, res)

    def test_create_Review(self):
        """test create() on BaseModel class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            re_match = re.compile(r'^([0-9a-fA-F]{8}-' +
                                  r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                  r'-fA-F]{4}-[0-9a-fA-F]{12})$')
            value = f.getvalue().strip()
            res = re_match.match(value).group().strip()
            # print("Expected pattern:", re_match.pattern)

            key = "Review." + res
            self.assertIn(key, storage.all())

            self.assertEqual(value, res)

    # Test show command
    def test_show_BaseModel(self):
        """test show() on BaseModel
        """
        base_model = self.cls
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel " + base_model.id )
            f_value = f.getvalue().strip()
            patt = self.show_pattern
            s_patt = patt.match(f_value).group().strip()

            key = "BaseModel." + base_model.id
            # value = storage.all()[key]

            self.assertIn(key, storage.all())
            self.assertEqual(f_value, s_patt)

    def test_show_User(self):
        """test show() on User
        """
        user = self.usr
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show User " + user.id )
            f_value = f.getvalue().strip()
            patt = self.show_pattern
            s_patt = patt.match(f_value).group().strip()

            key = "User." + user.id
            # value = storage.all()[key]

            self.assertIn(key, storage.all())
            self.assertEqual(f_value, s_patt)

    def test_show_State(self):
        """test show() on State
        """
        state = self.stt
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show State " + state.id )
            f_value = f.getvalue().strip()
            patt = self.show_pattern
            s_patt = patt.match(f_value).group().strip()

            key = "State." + state.id
            # value = storage.all()[key]

            self.assertIn(key, storage.all())
            self.assertEqual(f_value, s_patt)

    def test_show_City(self):
        """test show() on City
        """
        city = self.ct
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show City " + city.id )
            f_value = f.getvalue().strip()
            patt = self.show_pattern
            s_patt = patt.match(f_value).group().strip()

            key = "City." + city.id
            # value = storage.all()[key]

            self.assertIn(key, storage.all())
            self.assertEqual(f_value, s_patt)

    def test_show_Amenity(self):
        """test show() on Amenity
        """
        amenity = self.amnty
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Amenity " + amenity.id )
            f_value = f.getvalue().strip()
            patt = self.show_pattern
            s_patt = patt.match(f_value).group().strip()

            key = "Amenity." + amenity.id
            # value = storage.all()[key]

            self.assertIn(key, storage.all())
            self.assertEqual(f_value, s_patt)

    def test_show_Place(self):
        """test show() on Place
        """
        place = self.plc
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Place " + place.id )
            f_value = f.getvalue().strip()
            patt = self.show_pattern
            s_patt = patt.match(f_value).group().strip()

            key = "Place." + place.id
            # value = storage.all()[key]

            self.assertIn(key, storage.all())
            self.assertEqual(f_value, s_patt)

    def test_show_Review(self):
        """test show() on Review
        """
        review = self.rvw
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Review " + review.id )
            f_value = f.getvalue().strip()
            patt = self.show_pattern
            s_patt = patt.match(f_value).group().strip()

            key = "Review." + review.id
            # value = storage.all()[key]

            self.assertIn(key, storage.all())
            self.assertEqual(f_value, s_patt)

    def test_all(self):
        """test all() on BaseModel
        """ 
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            f_value = f.getvalue().strip()
            for v in storage.all().values():
                self.assertIn(str(v), f_value)

    def test_User_all(self):
        """test User.all()
        """ 
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.all()")
            f_value = f.getvalue().strip()
            for v in storage.all().values():
                self.assertIn(f_value, str(v))
        
class TestHBNBCommandClassBreaking(unittest.TestCase):
    """unittest class for BaseModel class when everything breaks"""
    def test_create_no_arguments(self):
        """test create with no arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_show_no_arguments(self):
        """test show with no arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_show_no_id(self):
        """test show with no id"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("Show BaseModel")
            f_output = f.getvalue().strip()
            cmd_output = "*** Unknown syntax: Show BaseModel"
            self.assertEqual(f_output, cmd_output)

    def test_update_no_arguments(self):
        """test update with no arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)
