#!/usr/bin/python3
"""
Entry point into the AirBnB console app
"""
import shlex
import cmd
import re
from json import loads
from json.decoder import JSONDecodeError
from typing import Union
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """AirBnB CLI
    Commands:
    quit, EOF, help
    """
    prompt = "(hbnb) "

    _models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
        }
    str_attr = ["name", "amenity_id", "place_id", "state_id",
                "user_id", "city_id", "description", "text",
                "email", "password", "first_name", "last_name"]
    int_attr = ["number_rooms", "number_bathrooms",
                "max_guest", "price_by_night"]
    float_attr = ["latitude", "longitude"]

    patterns = {"all": re.compile(r'(.*)\.(.*)\((.*)\)'),

                # id, attribute, value
                "update": [re.compile(r'^(.+)\,(.+)\,(.+)$'),
                           re.compile(r'^[\'\"]?([^"]+)[\'\"]?\,\s*(\{.+\})$'),
                           re.compile(r"[\'\"](.*?)[\'\"]")]}

    # pylint: disable-next=unused-argument
    def do_quit(self, arg) -> bool:
        """quit command to exit the program
        """
        return True

    # pylint: disable-next=unused-argument
    def do_EOF(self, arg) -> bool:
        """EOF or Ctrl-D command to exit the program
        """
        return True

    def emptyline(self) -> bool:
        """Empty line should do nothing"""
        return False

    def precmd(self, line) -> str:
        """parse command line and determine if reformatting is needed.
        Helps handle call to commands using Class.command("values"),
        By splitting it to match the format of the do_cmd
        Ex:
        $ update User <ID> <attribute> <value>
        $ User.update(<ID>, <attribute>, <value>)
        $ User.update(<ID>, {<attribute1>: <value1>, <attribute2>: <value2>})
        """
        # class.command(data)
        pattern = self.patterns
        args = pattern["all"].match(line)
        if args:
            arg_list = []
            arg_list.append(args.group(2))  # command
            arg_list.append(args.group(1))  # class
            arg_list.append(args.group(3))  # rest
            if arg_list[0] == "count":
                self.count(args.group(1))
                return ""
            if arg_list[0] == "update":
                # id, attribute, value
                uvp = pattern["update"][0]
                # id, {dict}
                udict = pattern["update"][1]
                clean = args.group(3).replace("'", '"')
                # id, {dict}
                uvp_match = udict.match(clean)
                res = arg_list[:2]
                if uvp_match and len(uvp_match.groups()) == 2:
                    try:
                        my_dict = loads(uvp_match.group(2))
                        for k, v in my_dict.items():
                            # command class id attribute value
                            self.onecmd(" ".join(res +
                                                 [uvp_match.group(1),
                                                  '"' + str(k) + '"',
                                                  '"' + str(v) + '"']))
                        return ""
                    except JSONDecodeError:
                        pass
                else:
                    # id, attribute, value
                    uvp_match = uvp.match(clean)
                    if uvp_match and len(uvp_match.groups()) == 3:
                        res.extend(uvp_match.group().split(','))
                    else:
                        res.append(clean)
                    return " ".join(res)
            else:
                return " ".join(arg_list)
        return line

    def do_create(self, arg) -> None:
        """Create a new instance of a class, save it, print its id
        Ex:
        $ create BaseModel
        $ <class name>.create()
        $ User.create()
        """
        args = shlex.split(arg)
        if not self.validate_cls(args):
            return
        instance = self._models[args[0]]()
        storage.save()
        print(instance.id)

    def do_show(self, arg) -> None:
        """Prints the string representation of an instance
        based on the class name and id
        Ex:
        $ show BaseModel 1234-1234-1234
        $ <class name>.show(id)
        $ BaseModel.show(1234-1234-1234)
        """
        args = shlex.split(arg)
        if not (self.validate_cls(args) and self.validate_id(args)):
            return
        print(storage.all()[args[0] + "." + args[1]])

    def do_destroy(self, arg) -> None:
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)
        Ex:
        $ destroy BaseModel 1234-1234-1234
        $ <class name>.destroy(id)
        $ BaseModel.destroy(1234-1234-1234)
        """
        args = shlex.split(arg)
        if not (self.validate_cls(args) and self.validate_id(args)):
            return
        del storage.all()[args[0] + "." + args[1]]
        storage.save()

    def count(self, arg) -> None:
        """Count all occurences of class instances
        Ex:
        $ count BaseModel
        $ BaseModel.count()
        """
        args = shlex.split(arg)

        if not self.validate_cls(args):
            return
        res = 0
        if len(args) > 0:
            for k in storage.all():
                if args[0] == k.split(".")[0]:
                    res += 1
        print(res)

    def do_all(self, arg) -> None:
        """Prints all string representation of all instances
        based or not on the class name
        Ex:
        $ all
        $ all BaseModel
        $ <class name>.all()
        $ BaseModel.all()
        """
        args = shlex.split(arg)
        res = []
        if len(args) > 0:
            if not self.validate_cls(args):
                return
            for k, v in storage.all().items():
                if args[0] == k.split(".")[0]:
                    res.append(str(v))
        else:
            for k, v in storage.all().items():
                res.append(str(v))
        print(res)

    def do_update(self, arg) -> None:
        """Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        update <class name> <id> <attribute name> "<attribute value>"
        Ex:
        $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        $ update User <ID> <attribute> <value>
        $ User.update(<ID>, <attribute>, <value>)
        $ User.update(<ID>, {<attribute1>: <value1>, <attribute2>: <value2>})
        """

        args = shlex.split(arg)

        if not (self.validate_cls(args) and self.validate_id(args)):
            return
        key = args[0] + "." + args[1]
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        # if args[3].startswith(("'", '"')) and args[3].endswith(("'", '"')):
            # match = self.patterns["update"][2].match(args[3]).group(1)
        # else:
        match = args[3]

        instance = storage.all()[key]

        if args[2] in self.int_attr:
            setattr(instance,
                    args[2], int(match))
        elif args[2] in self.str_attr:
            setattr(instance, args[2], str(match))
        elif args[2] in self.float_attr:
            setattr(instance, args[2], float(match))
        else:
            setattr(instance, args[2], self.type_cast(match))
        storage.save()

    def type_cast(self, arg) -> Union[float, int, str]:
        """determine type of arg and cast it to the correct type
        """
        try:
            if "." in arg:
                return float(arg)
            return int(arg)
        except ValueError:
            return arg

    def validate_cls(self, args) -> bool:
        """validate class creation
        Checks if class name is provide and it exists
        """
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in self._models:
            print("** class doesn't exist **")
            return False
        return True

    def validate_id(self, args) -> bool:
        """validate id of class instance
        Checks if id is provide and it exists
        """
        if len(args) < 2:
            print("** instance id missing **")
            return False
        instance_id = args[0] + "." + args[1]
        if instance_id not in storage.all():
            print("** no instance found **")
            return False
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
