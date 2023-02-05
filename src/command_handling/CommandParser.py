import copy
from typing import Optional

from UserMessageResponder import UserMessageResponder
from command_handling.commands.CreateCommand import CreateCommand
from command_handling.commands.CreditBalanceCommand import CreditBalanceCommand
from command_handling.commands.DestroyCommand import DestroyCommand
from command_handling.commands.IpCommand import IpCommand
from command_handling.commands.StartCommand import StartCommand
from command_handling.commands.StopCommand import StopCommand
from credits.CreditColumnDataGateway import CreditColumnDataGateway
from credits.CreditManager import CreditManager
from utils.mongo_gateway import MongoGateway
from utils.instance_manager import InstanceManager


class CommandParser:
    """
    For a given command string, creates the appropriate command objects and gives them the necessary arguments.
    """

    def __init__(self, database_gateway: MongoGateway, responder: UserMessageResponder):
        # List of the commands that this parser can parse
        # TODO move gateway and manager creation to a more appropriate place
        credit_data_gateway = CreditColumnDataGateway(database_gateway)  
        credit_manager = CreditManager(credit_data_gateway)
        server_manager = InstanceManager()
        self.command_list = [StartCommand(responder, database_gateway, server_manager, credit_manager),
                             CreateCommand(responder, database_gateway, server_manager),
                             StopCommand(responder, database_gateway, server_manager, credit_manager),
                             DestroyCommand(responder, database_gateway, server_manager),
                             IpCommand(responder, database_gateway, server_manager),
                             CreditBalanceCommand(responder, credit_data_gateway)
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
