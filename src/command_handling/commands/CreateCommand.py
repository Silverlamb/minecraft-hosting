import threading

import discord

from UserMessageResponder import UserMessageResponder
from command_handling.commands.ServerAdminCommand import ServerAdminCommand
from utils.mongo_gateway import MongoGateway
from utils.instance_manager import InstanceManager

"""
Command to create a game server.
"""


class CreateCommand(ServerAdminCommand):
    """
    Creates a new create command instance.

    Before this command can be executed, its arguments must be parsed into it.
    """

    def __init__(self, responder: UserMessageResponder, database_gateway: MongoGateway, server_manager: InstanceManager):
        super().__init__("create", responder, database_gateway, server_manager)
        self.discord_msg = None

    """
    (See parent class)
    """

    def __copy__(self):
        return CreateCommand(self.responder, self.database_gateway, self.server_manager)

    """
    Parses the arguments for this command from the provided argument string list and extracts relevant information form
    the discord message object.

    Expected arguments in the string arguments list: none.
    """

    def parse_arguments(self, arguments: list, discord_msg) -> None:
        self.discord_msg = discord_msg


    def execute(self) -> None:
        """
        (See parent class)
        """

        super().execute()
        threading.Thread(target=self.server_manager.server_create, args=(self.discord_msg.guild.id, 
                                                                         self.discord_msg.channel.id, 
                                                                         self.responder
                                                                         )).start()