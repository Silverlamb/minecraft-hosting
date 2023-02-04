import discord
from discord.command_handling.Command import Command

"""
For a given command string, creates the appropriate command objects and gives them the necessary arguments.
"""
class CommandParser:
    def __init__(self):
        # List of the commands that this parser can parse
        self.command_list = []
        pass

    """
    Takes a command string and creates the appropriate command object for it.
    """
    def parse_command(self, command_string: str, discord_msg) -> Command:
        string_elements = command_string.split(" ")
        for command in self.command_list:
            if command_string.startswith(command.get_name()):
                return command.parse_arguments(string_elements[1:], discord_msg)


