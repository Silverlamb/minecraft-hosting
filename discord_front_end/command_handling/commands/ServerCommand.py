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

    def execute(self):
        """
        (See parent class)
        """
        super().execute()
        self.register_guild_if_needed()
        # Further logic is executed in the subclass

    def register_guild_if_needed(self) -> None:
        """
        Registers the guild that the message came from if the guild is not registered yet.
        """
        if not self.database_gateway.exist_instance_guild(self.discord_msg.guild.id):
            self.database_gateway.insert_instance_one(self.discord_msg.guild.id)
            self.responder.send_remote_message('guild_not_registered', self.discord_msg.channel.id)
