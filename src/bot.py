# bot.py
import os
import discord
import dotenv

from command_handling.CommandParser import CommandParser
from UserMessageResponder import UserMessageResponder
from utils.mongo_gateway import MongoGateway

"""
Discord class for discord client
"""


class DiscordClient(discord.Client):
    BOT_TRIGGER = "!"
    MSG_CMD_RECEIVED = "Command {} received"
    MSG_CMD_NOT_PARSABLE = "Command '{}' not parsable"
    MSG_CMD_SUCCESS = "Command successfully executed"

    """
    Sets and loads env variables in local os environment into token
    
    Also, set the necessary intents for the bot and calls the Discord API's super constructor.
    """
    def __init__(self, intents=discord.Intents.default(), *args, **kwargs):
        intents.message_content = True
        super().__init__(intents=intents, *args, **kwargs)
        self.dotenv_file = dotenv.find_dotenv()  # sets the env file
        dotenv.load_dotenv(self.dotenv_file)  # loads env variables in local os environment
        self.token = os.environ["DISCORD_TOKEN"]  # specific to discord client
        self.message_content = True

        self.database_gateway = MongoGateway()
        self.command_parser = CommandParser(self.database_gateway, UserMessageResponder(self, None))

    """
    Handles Messages sent to the Bot
    """

    async def on_message(self, message):
        # if the message is the bot or does not have the '!' at the beginning then it is ignored
        if message.author == self.user or message.content[0] != self.BOT_TRIGGER:
            return

        command_string = (message.content[1:]) # removes the bot trigger
        command = self.command_parser.parse_command(command_string, message)

        if command is None:
            await self.send_response_message(message, self.MSG_CMD_NOT_PARSABLE.format(message.content[1:]))
            return

        await self.send_response_message(message, self.MSG_CMD_RECEIVED.format(command.get_name().upper()))

        try:
            command.execute()
        except Exception as e:
            await message.channel.send("ERROR: " + str(e) + " in " + e.__traceback__.tb_frame.f_code.co_filename
                                       + " at line " + str(e.__traceback__.tb_lineno))
            # TODO Remove explicit debug print out

        await self.send_response_message(message, self.MSG_CMD_SUCCESS) # TODO remove (debug)


    @staticmethod
    async def send_response_message(message_to_respond_to: discord.Message, response_str: str):
        await message_to_respond_to.channel.send(response_str)



