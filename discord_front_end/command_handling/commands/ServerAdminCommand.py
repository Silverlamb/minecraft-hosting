from abc import ABC

import discord

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.command_handling.Command import Command
from discord_front_end.command_handling.commands.ServerCommand import ServerCommand
from discord_front_end.utils.db import MongoGateWay


class ServerAdminCommand(ServerCommand, ABC):
    """
    Abstract command class for commands that control a game server and require administrator permissions.
    """

    HARDCODED_ROOT_USERS = [518217896896495616, 665749352891023392, 568174168370053152]  # Headrush, Silverlamb, funcrek
    MSG_NO_PERMISSION = "You do not have permission to use this command."
    MSG_SERVER_NOT_REGISTERED = "The server is not registered with the system yet. Please register first."

    def __init__(self, name: str, responder: UserMessageResponder, database_gateway: MongoGateWay):
        """
        Creates a new server command. The concrete command name specified by the name parameter is used as a sub-name.

        Before this command can be executed, its arguments must be parsed into it.
        """

        super().__init__(name, responder, database_gateway)
        self.database_gateway = database_gateway
        self.discord_msg = None

    """
    (See parent class)
    """

    def __copy__(self):
        return ServerAdminCommand(self.name, self.responder, self.database_gateway)

    """
    (See parent class)
    """

    def execute(self):
        super().execute()
        #self.assert_admin(self.discord_msg)
        # Further logic is executed in the subclass

    @staticmethod
    def is_admin(discord_msg: discord.Message) -> bool:
        """
        Returns whether the user who sent the message has admin permissions.
        """
        has_admin_role = discord.utils.get(discord_msg.guild.roles, name="Admin")
        has_admin_permission = discord_msg.author.guild_permissions.administrator
        is_root_user = discord_msg.author.id in ServerAdminCommand.HARDCODED_ROOT_USERS

        return has_admin_role or has_admin_permission or is_root_user

    @staticmethod
    def assert_admin(discord_msg: discord.Message) -> None:
        """
        Raises an exception if the user who sent the message does not have admin permissions.
        Otherwise, returns without doing anything.
        """
        if not ServerAdminCommand.is_admin(discord_msg):
            raise PermissionError(ServerAdminCommand.MSG_NO_PERMISSION)
