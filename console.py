#!/usr/bin/python3
"""
Entry point into the AirBnB console app
"""
import cmd


class HBNBCommand(cmd.Cmd):
    """AirBnB CLI
    Commands:
    quit, EOF, help
    """
    prompt = "(hbnb) "

    # pylint: disable-next=unused-argument
    def do_quit(self, arg) -> bool:
        """Quit command to exit the program
        """
        return True

    do_EOF = do_quit


if __name__ == "__main__":
    HBNBCommand().cmdloop()
