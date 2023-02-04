from typing import Optional

from discord_front_end.command_handling.commands.CreateCommand import CreateCommand
from discord_front_end.command_handling.commands.StartCommand import StartCommand

"""
For a given command string, creates the appropriate command objects and gives them the necessary arguments.
"""
class CommandParser:
    def __init__(self):
        # List of the commands that this parser can parse
        self.command_list = [StartCommand(), CreateCommand()]
        pass

    """
    Takes a command string and creates the appropriate command object for it.
    """
    def parse_command(self, command_string: str, discord_msg) -> Optional[StartCommand]:
        for command in self.command_list:
            if command_string.startswith(command.get_name()):
                argument_string = command_string.replace(command.get_name(), '')
                argument_elements = argument_string.split(" ")

                # Create a new command object of the same type as the command in the list
                command_type = type(command)
                new_command = command_type()
                new_command.parse_arguments(argument_elements, discord_msg)
                return new_command

        return None
