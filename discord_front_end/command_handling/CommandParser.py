from typing import Optional

import discord
from discord_front_end.command_handling.Command import Command
from discord_front_end.command_handling.commands.StartCommand import StartCommand

"""
For a given command string, creates the appropriate command objects and gives them the necessary arguments.
"""
class CommandParser:
    def __init__(self):
        # List of the commands that this parser can parse
        self.command_list = [StartCommand()]
        pass

    """
    Takes a command string and creates the appropriate command object for it.
    """
    def parse_command(self, command_string: str, discord_msg) -> Optional[StartCommand]:
        string_elements = command_string.split(" ")
        for command in self.command_list:
            if command_string.startswith(command.get_name()):
                # Create a new command object of the same type as the command in the list
                command_type = type(command)
                new_command = command_type()
                new_command.parse_arguments(string_elements[1:], discord_msg) # TODO Pass only arguments that do not belong to name
                return new_command

        return None

