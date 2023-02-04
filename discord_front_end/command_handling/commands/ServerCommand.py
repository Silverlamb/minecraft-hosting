from abc import ABC

import discord

from discord_front_end.command_handling.Command import Command
from discord_front_end.utils.db import MongoGateWay

"""
Abstract command class for commands that control a game server.
"""


class ServerCommand(Command, ABC):
    HARDCODED_ROOT_USERS = [518217896896495616, 665749352891023392]  # Headrush, Silverlamb
    MSG_NO_PERMISSION = "You do not have permission to use this command."


    """
    Creates a new server command. The concrete command name specified by the name parameter is used as a sub-name.

    Before this command can be executed, its arguments must be parsed into it.
    """

    def __init__(self, name: str, database_gateway: MongoGateWay):
        super().__init__("server " + name)
        self.database_gateway = database_gateway


    """
    Returns a shallow copy of this command object.
    """
    def __copy__(self):
        return ServerCommand(self.name, self.database_gateway)

    """
    (See parent class)
    """
    def execute(self):
        super().execute()
        self.assert_admin(self.discord_msg)
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