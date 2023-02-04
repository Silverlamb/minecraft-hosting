# bot.py
import os
import discord
import dotenv

"""
Discord class for discord client
"""

class DiscordClient(discord.Client):
    def __init__(self, intents = discord.Intents.default(), *args, **kwargs):
        super().__init__(intents = intents, *args, **kwargs)
        self.dotenv_file = dotenv.find_dotenv() #sets the env file
        dotenv.load_dotenv(self.dotenv_file) #loads env variables in local os environment
        self.token = os.environ["DISCORD_TOKEN"] #specific to discord client
        self.message_content = True

    """
    Handels Messages sent to the Bot
    """
    async def on_message(self, message):  
        if message.author == client.user or message.content[0] != '!': #if the message is the bot or does not have the '!' at the beginning then it is ignored
            return

        args = (message.content[1:]).lower().split() #splits all arguments into a list lowercased. (!helLo woRld => ['hello', 'world'])
        
        if args[0] == 'bot':
            await message.channel.send("Just a bot that will help you host your Minecraft servers!")

intents = discord.Intents.default()
intents.message_content = True

client = DiscordClient(intents = intents)
client.run(client.token)