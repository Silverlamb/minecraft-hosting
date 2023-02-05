import threading

import discord

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.command_handling.commands.ServerAdminCommand import ServerAdminCommand
from discord_front_end.utils.db import MongoGateWay

"""
Command to create a game server.
"""


class CreateCommand(ServerAdminCommand):
    """
    Creates a new create command instance.

    Before this command can be executed, its arguments must be parsed into it.
    """

    def __init__(self, responder: UserMessageResponder, database_gateway: MongoGateWay):
        super().__init__("create", responder, database_gateway)
        self.discord_msg = None

    """
    (See parent class)
    """

    def __copy__(self):
        return CreateCommand(self.responder, self.database_gateway)

    """
    Parses the arguments for this command from the provided argument string list and extracts relevant information form
    the discord message object.

    Expected arguments in the string arguments list: none.
    """

    def parse_arguments(self, arguments: list, discord_msg) -> None:
        self.discord_msg = discord_msg

    """
    (See parent class)
    """

    def execute(self) -> None:
        super().execute()

        # TODO Check whether user has sufficient credits

        #threading.Thread(target=self._create_server,
        #                 args=(self.discord_msg.guild.id, self.discord_msg.channel.id)).start()

    """
    Starts a server based on guild id
    """

    def _create_server(self, guild_id, channel_id, bot_for_messages: discord.Client) -> None:
        # TODO Old code. Will be replaced by using the interface to Ishaan
        instance_data = self.database_gateway.find_instance_one(guild_id)

        if instance_data["server_state"] or instance_data["server_present"] or instance_data["is_process"]:
            raise Exception("Server is already running or is being created.")
