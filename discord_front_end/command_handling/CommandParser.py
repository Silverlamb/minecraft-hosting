import copy
from typing import Optional

from discord_front_end.command_handling.commands.CreateCommand import CreateCommand
from discord_front_end.command_handling.commands.StartCommand import StartCommand
from discord_front_end.utils.db import MongoGateWay

"""
For a given command string, creates the appropriate command objects and gives them the necessary arguments.
"""
class CommandParser:
    def __init__(self, database_gateway: MongoGateWay):
        # List of the commands that this parser can parse
        self.command_list = [StartCommand(database_gateway), CreateCommand(database_gateway)]
        pass

    """
    Takes a command string and creates the appropriate command object for it.
    """
    def parse_command(self, command_string: str, discord_msg) -> Optional[StartCommand]:
        for command_template in self.command_list:
            if command_string.startswith(command_template.get_name()):
                argument_string = command_string.replace(command_template.get_name(), '')
                argument_elements = argument_string.split(" ")

                # Create a new command object of the same type as the command in the list
                new_command = copy.copy(command_template)
                new_command.parse_arguments(argument_elements, discord_msg)
                return new_command

        return None
