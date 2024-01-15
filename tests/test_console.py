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
    documentation and pep8 conformaty
    """

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8.
        """
        style = pep8.StyleGuide()
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_console conforms to PEP8.
        """
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation
        """
        mod_doc = console.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self):
        """test class documentation
        """
        mod_doc = str(HBNBCommand.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions
        """
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
        self.commands = ['all', 'quit', 'create', 'update', 'show',
                         'destroy', 'count', 'EOF']

    def tearDown(self) -> None:
        """Tear down instances and variables
        """
        for instance in self.instances:
            del storage.all()[instance.__class__.__name__ +
                              "." + instance.id]
        storage.save()

    def test_methods(self):
        """test methods
        """
        for k in self.commands:
            if k != 'count':
                self.assertIn(f"do_{k}", HBNBCommand.__dict__.keys())
            else:
                self.assertIn(f"{k}", HBNBCommand.__dict__.keys())

    def test_help(self):
        """test help command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            f_value = f.getvalue().strip()
            self.assertIn('''Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update''', f_value)

    def test_help_command(self):
        """test help <topic> command.
        """
        for k in self.commands:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"help {k}")
                f_value = f.getvalue().strip()
                self.assertIn(k, f_value)
                self.assertTrue(len(f_value) > 0)

    def test_do_quit(self):
        """test quit command. Exits the execution and outputs nothing
        onecmd returns true when it terminates the interactive mode
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd('quit'))
            self.assertEqual(f.getvalue(), '')

    def test_do_EOF(self):
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

    def test_count(self):
        """test count
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().precmd("User.count()")
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "User":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_do_all(self):
        """test all
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"all")
            # convert str list to list
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_do_all_class(self):
        """test all <class>
        """
        for k, _ in self.classes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {k}")
                if f.getvalue().strip() != "[]":
                    self.assertRegex(f.getvalue().strip(), self.show_pattern)
                res = []
                for i, j in storage.all().items():
                    if k == i.split(".")[0]:
                        res.append(str(j))

                self.assertEqual(str(res), f.getvalue().strip())

    def test_do_create(self):
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

    def test_do_show(self):
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

    def test_do_destroy(self):
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

    def test_do_update(self):
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
    """unittest class for HBNBCommand class when everything breaks
    """
    def test_wrong_command(self):
        """test a wrong command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("reate")
            f_output = f.getvalue().strip()
            cmd_output = "*** Unknown syntax: reate"
            self.assertEqual(f_output, cmd_output)

    def test_all_wrong_class(self):
        """test all with wrong
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all ds")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_create_no_class(self):
        """test create with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_create_wrong_class(self):
        """test create with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create urs")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_show_no_class(self):
        """test show with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_show_wrong_class(self):
        """test show with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show ds")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_show_no_id(self):
        """test show with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_show_wrong_id(self):
        """test show with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 0")
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_no_class(self):
        """test destroy with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_wrong_class(self):
        """test destroy with wrong
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy ds")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_no_id(self):
        """test destroy with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_wrong_id(self):
        """test destroy with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 0")
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_update_no_class(self):
        """test update with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_update_wrong_class(self):
        """test update with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update cls")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_update_no_id(self):
        """test update with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User")
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_update_wrong_id(self):
        """test update with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User 0")
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_update_no_attribute(self):
        """test update with no attribute
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            usr_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update User {usr_id}")
            f_output = f.getvalue().strip()
            cmd_output = "** attribute name missing **"
            self.assertEqual(f_output, cmd_output)
            HBNBCommand().onecmd(f"destroy User {usr_id}")

    def test_update_no_value(self):
        """test update with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            usr_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update User {usr_id} "attribute"')
            f_output = f.getvalue().strip()
            cmd_output = "** value missing **"
            self.assertEqual(f_output, cmd_output)
            HBNBCommand().onecmd(f"destroy User {usr_id}")
