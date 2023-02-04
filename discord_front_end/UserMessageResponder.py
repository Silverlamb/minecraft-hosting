import asyncio

import discord


class UserMessageResponder:
    """ An inverse dependency to the discord client. Allows the backend to trigger certain message events.

    This class manages what precise messages are sent upon the respective events.
    """

    def __init__(self, client: discord.Client):
        self.client = client

    def send_remote_message(self, event_name: str, channel_id, args=None):
        """
        Creates a new (background) task of a remote message (ie. one sent from outside the class)
        """
        self.client.loop.create_task(self._remote_message(event_name, channel_id, args))

    def send_direct_message(self, id, msg):
        """ Sends a direct message via discord id using the client
        """

        self.client.loop.create_task(self._direct_message(id, msg))

    async def _remote_message(self, arg, channel_id, args):
        """
        Different possible types of remote messages that can be sent to the user
        """

        if arg == 'server_created':
            await self.client.get_channel(channel_id).send("{} {} {}".format(
                "Server created successfully!",
                "Please do !server start to begin your journey.",
                "Note that it will take some time at first to generate the world."
            ))
        elif arg == 'server_started':
            await self.client.get_channel(channel_id).send(
                "Server started successfully! Server address: ``{}``".format(args[0]))
        elif arg == 'server_stopped':
            await self.client.get_channel(channel_id).send("Server stopped successfully!")
        elif arg == 'server_destroyed':
            await self.client.get_channel(channel_id).send("Server destroyed successfully!")
        elif arg == 'server_state_err':
            await self.client.get_channel(channel_id).send("{} {}\n {}".format(
                "Server state cannot be changed!",
                "This might be because it is in a state that is not changeable from the command provided.",
                "Try doing !server state to see which state it is"
            ))
        elif arg == 'insufficient_funds':
            await self.client.get_channel(channel_id).send("Insufficent amount of credits! Do !credit to see balance.")
        elif arg == 'credits_charge':
            await self.client.get_channel(channel_id).send(
                "You were charged {}! Your credit balance is {}".format(round(args[0], 4),
                                                                        round(args[1], 3)))  # TODO: str() needed?
        elif arg == 'credits_pre_warning':
            await self.client.get_channel(channel_id).send("{}! {}. {}.".format(
                "Your credits will run out in the next hour",
                "Either refill your credits or stop to server",
                "The server will be shutdown once you can't pay credits anymore"
            ))
        elif arg == 'credits_warning':
            await self.client.get_channel(channel_id).send("{}! {}. {}.".format(
                "Your credits will run out in the next hour",
                "Either refill your credits or stop to server",
                "The server will be shutdown once you can't pay credits anymore"
            ))
        elif arg == 'credits_out':
            await self.client.get_channel(channel_id).send("Your credits ran out!")
        elif arg == 'server_stopped_forced':
            await self.client.get_channel(channel_id).send("Server stopped forcefully. Credits have run out.")
        elif arg == 'first_server_started':
            await self.client.get_channel(channel_id).send("{} {} {}{}".format(
                "Server started successfully!",
                "Since this is your first time starting the server, I advise you to wait a couple of minutes (5 max) for the world to properly generate everything.",
                "Also, the server may crash, but don't be alarmed. It will quickly reset itself and you can play peacefully again.\n",
                "Do !server ip for the ip. Have fun!"
            ))
        elif arg == 'fetch_success':
            await self.client.get_channel(channel_id).send("You world has succesfully backed up!")
        elif arg == 'fetch_err':
            await self.client.get_channel(channel_id).send(
                "The back-up didn't save properly or doesn't exist. Please try again.")
        elif arg == 'fetch_missing_directory':
            await self.client.get_channel(channel_id).send(
                "Whoops something went wrong! I've attempted to fix it. Please try again.")
        elif arg == 'restore_success':
            await self.client.get_channel(channel_id).send("You world has succesfully been restored with your back up!")
        elif arg == 'restore_no_back_ups':
            await self.client.get_channel(channel_id).send(
                "You can't restore anything because you don't have any back ups to restore with.")
        elif arg == 'version_update_complete':
            await self.client.get_channel(channel_id).send("Your minecraft server was updated succesfully!")
        elif arg == 'version_update_none':
            await self.client.get_channel(channel_id).send("There are no available updates for this server.")
        elif arg == 'fetch_created_err':
            await self.client.get_channel(channel_id).send(
                "You cannot back up a server that has just been created! Please start it once so I can back it up.")
        else:
            print("ERR: Arg '{}' does not exist!".format(arg))

    async def _direct_message(self, id, msg):
        """ Sends discord direct message via user's discord id
        """

        user = await self.client.fetch_user(id)
        await user.send(msg)