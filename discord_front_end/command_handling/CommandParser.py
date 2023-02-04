import copy
from typing import Optional

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.command_handling.commands.CreateCommand import CreateCommand
from discord_front_end.command_handling.commands.DestroyCommand import DestroyCommand
from discord_front_end.command_handling.commands.IpCommand import IpCommand
from discord_front_end.command_handling.commands.StartCommand import StartCommand
from discord_front_end.command_handling.commands.StopCommand import StopCommand
from discord_front_end.credits.CreditManager import CreditManager
from discord_front_end.utils.db import MongoGateWay


class CommandParser:
    """
    For a given command string, creates the appropriate command objects and gives them the necessary arguments.
    """

    def __init__(self, database_gateway: MongoGateWay, responder: UserMessageResponder):
        # List of the commands that this parser can parse
        credit_manager = CreditManager(database_gateway)  # TODO move to a more appropriate place
        self.command_list = [StartCommand(responder, database_gateway, credit_manager),
                             CreateCommand(responder, database_gateway),
                             StopCommand(responder, database_gateway, credit_manager),
                             DestroyCommand(responder, database_gateway),
                             IpCommand(responder, database_gateway),
                             ]
        pass

    def parse_command(self, command_string: str, discord_msg) -> Optional[StartCommand]:
        """
        Takes a command string and creates the appropriate command object for it.
        """

        for command_template in self.command_list:
            if command_string.startswith(command_template.get_name()):
                argument_string = command_string.replace(command_template.get_name(), '')
                argument_elements = argument_string.split(" ")

                # Create a new command object of the same type as the command in the list
                new_command = copy.copy(command_template)
                new_command.parse_arguments(argument_elements, discord_msg)
                return new_command

        return None
