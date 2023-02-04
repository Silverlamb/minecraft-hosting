from abc import ABC

import discord

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.command_handling.Command import Command
from discord_front_end.utils.db import MongoGateWay


class ServerCommand(Command, ABC):
    """
    Abstract command class for commands that control a game server.
    """

    HARDCODED_ROOT_USERS = [518217896896495616, 665749352891023392, 568174168370053152]  # Headrush, Silverlamb, funcrek
    MSG_NO_PERMISSION = "You do not have permission to use this command."
    MSG_SERVER_NOT_REGISTERED = "The server is not registered with the system yet. Please register first."

    def __init__(self, name: str, responder: UserMessageResponder, database_gateway: MongoGateWay):
        """
        Creates a new server command. The concrete command name specified by the name parameter is used as a sub-name.

        Before this command can be executed, its arguments must be parsed into it.
        """

        super().__init__("server " + name, responder)
        self.database_gateway = database_gateway
        self.discord_msg = None

    """
    (See parent class)
    """

    def __copy__(self):
        return ServerCommand(self.name, self.responder, self.database_gateway)

    """
    (See parent class)
    """

    def execute(self):
        super().execute()
        self.assert_discord_server_is_registered(self.discord_msg.guild.id)
        # Further logic is executed in the subclass


    def assert_discord_server_is_registered(self, guild_id: int) -> None:
        """
        Raises an exception if the server is not registered with the system yet.
        """
        if not self.database_gateway.exist_instance_guild(guild_id):
            raise PermissionError(self.MSG_SERVER_NOT_REGISTERED)
