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
        self.assert_admin(self.discord_msg)
        self.assert_discord_server_is_registered(self.discord_msg.guild.id)
        # Further logic is executed in the subclass

    """
    Returns whether the user who sent the message has admin permissions.
    """

    @staticmethod
    def is_admin(discord_msg: discord.Message) -> bool:
        has_admin_role = discord.utils.get(discord_msg.guild.roles, name="Admin")
        has_admin_permission = discord_msg.author.guild_permissions.administrator
        is_root_user = discord_msg.author.id in ServerCommand.HARDCODED_ROOT_USERS

        return has_admin_role or has_admin_permission or is_root_user

    """
    Raises an exception if the user who sent the message does not have admin permissions.
    Otherwise, returns without doing anything.
    """

    def assert_admin(self, discord_msg: discord.Message) -> None:
        if not self.is_admin(discord_msg):
            raise PermissionError(self.MSG_NO_PERMISSION)

    def assert_discord_server_is_registered(self, guild_id: int) -> None:
        if not self.database_gateway.exist_instance_guild(guild_id):
            raise PermissionError(self.MSG_SERVER_NOT_REGISTERED)
