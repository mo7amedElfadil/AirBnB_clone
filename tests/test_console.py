#!/usr/bin/python3
"""Unittest for HBNBCommand class
file name: test_console.py
"""
import unittest
import inspect  # test function and module doc string
# from json import dumps, loads #to test the de/serialization
from unittest.mock import patch
from io import StringIO
import re
import pycodestyle as pep8
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import console
from console import HBNBCommand


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for HBNBCommand class
    documentation and pep8 conformaty"""

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
    """unittest class for HBNBCommand class when everything works
    """
    def setUp(self):
        """ instanciate widely used variables
        """
        self.cmd = HBNBCommand()
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.show_pattern = re.compile(r'(\[([^]]+)\] \(([^)]+)\) (\{.+\}))')
        self.classes = {"BaseModel": BaseModel, "User": User,
                        "State": State, "City": City,
                        "Amenity": Amenity, "Place": Place,
                        "Review": Review}
        self.instances = []

    def tearDown(self) -> None:
        """Tear down instances and variables"""
        for instance in self.instances:
            del storage.all()[instance.__class__.__name__ +
                              "." + instance.id]
        storage.save()

    def test_quit(self):
        """test quit command. Exits the execution and outputs nothing
        onecmd returns true when it terminates the interactive mode
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd('quit'))
            self.assertEqual(f.getvalue(), '')

    def test_EOF(self):
        """test EOF command. Exits the execution and outputs nothing
        onecmd returns true when it terminates the interactive mode
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd('EOF'))
            self.assertEqual(f.getvalue(), '')

    def test_emptyline(self):
        """test EOF command. Doesn't execute anything
        onecmd returns false when execution continues
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(''))
            self.assertEqual(f.getvalue(), '')

    def test_create_class(self):
        """test create <class>
        """
        for k in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                self.assertRegex(f.getvalue().strip(), self.id_pattern)
                res = f.getvalue().strip()
                key = f"{k}." + res
                self.instances.append(storage.all()[key])
                self.assertIn(key, storage.all())

    def test_show_class(self):
        """test show <class>
        """
        for k, v in self.classes.items():
            model = v()
            self.instances.append(model)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {k} {model.id}")
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
                key = f"{k}.{model.id}"
                self.assertIn(key, storage.all())

    def test_destroy_class(self):
        """test destroy <class>
        """
        for k, _ in self.classes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                f_value = f.getvalue().strip()
                key = f"{k}.{f_value}"
                self.assertIn(key, storage.all())
                HBNBCommand().onecmd(f"destroy {k} {f_value}")
                self.assertNotIn(key, storage.all())

    def test_update_class(self):
        """test update <class>
        """
        for k, _ in self.classes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                f_value = f.getvalue().strip()
                key = f"{k}.{f_value}"
                self.assertIn(key, storage.all())
                HBNBCommand().onecmd(f'update {k}\
                                     {f_value} "attribute" "value"')
                self.assertTrue(hasattr(storage.all()[key], "attribute"))
                self.assertEqual(storage.all()[key]
                                 .to_dict()["attribute"], "value")
                HBNBCommand().onecmd(f"destroy {k} {f_value}")
                self.assertNotIn(key, storage.all())


class TestHBNBCommandClassBreaking(unittest.TestCase):
    """unittest class for HBNBCommand class when everything breaks"""
    def test_wrong_command(self):
        """test a wrong command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("reate")
            f_output = f.getvalue().strip()
            cmd_output = "*** Unknown syntax: reate"
            self.assertEqual(f_output, cmd_output)

    def test_create_no_arguments(self):
        """test create with no arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_create_wrong_arguments(self):
        """test create with wrong arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create urs")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
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
