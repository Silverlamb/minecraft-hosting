from discord_front_end.utils.db import MongoGateWay


class GameServerInstanceProxy:
    """Proxies a game server instance in the database that a user can control through the front end.

    Can be created solely from a guild id and database access.
    In this case, the proxy will try to find the corresponding game server instance in the database.
    """

    """
    Created status variable (used in more than one place)
    """
    CREATED_STATUS = "Created (Stopped)"

    def __init__(self,  guild_id: int, database_gateway: MongoGateWay):
        """Creates a new game server instance proxy from a guild id using the provided database.
        """

        self.database_gateway = database_gateway
        self.guild_id = guild_id

    def setup(self) -> None:
        """ Sets up a new game server instance in the database and on the hosting platform.

        This creates an instance which this proxy will represent from there on. The instance does not exist beforehand.
        """
        if self._is_locked():
            raise Exception("Server instance is currently being used by a different user. Please retry later")

        instance_data = self._get_instance_data()

        if instance_data["server_state"] or instance_data["server_present"]:
            raise Exception("Server exists already.")

        # TODO Check whether instance is in a state that allows setup
        self._local_setup(self.guild_id)
        self._remote_setup(self.guild_id)

        instance_id = None
        with open("{}/{}/instanceID.txt".format(globals.guild_instances_path, self.guild_id), "r") as f:
            instance_id = f.read()
        if instance_id is None:
            raise Exception("Could not retrieve instance_id from instanceID.txt.")

        set_instance_id_query = {"instance_id": instance_id}
        self.database_gateway.update_instance_one(self.guild_id, set_instance_id_query)

        set_server_state_query = {
                    "server_state": True,
                    "server_present": False,
                    "server_status": self.CREATED_STATUS,
                }
        self.database_gateway.update_instance_one(self.guild_id, set_server_state_query)


    def _local_setup(self, guild_id) -> None:
        """ Creates the necessary local file system for a new game server instance.
        """
        create_file("{}/{}/ip.txt".format(globals.guild_instances_path, guild_id), "")

        create_file("{}/{}/instanceID.txt".format(globals.guild_instances_path, guild_id), "")

        create_folder("{}/{}/back_up".format(globals.guild_instances_path, guild_id))

        copy_file("terraform", "{}/{}/terraform".format(globals.guild_instances_path, guild_id))

    def _remote_setup(self, guild_id) -> None:
        """ Uses terraform and ansible to create a new game server instance on the hosting platform.
        """
        pass

    def _set_lock(self, set_lock_state: bool) -> None:
        """ Locks the game server instance to prevent concurrent access.
        """

        set_is_process_query = {"is_process": set_lock_state}
        self.database_gateway.update_instance_one(self.guild_id, set_is_process_query)

    def _is_locked(self) -> bool:
        """ Returns whether the game server instance is locked.
        """

        instance_data = self.database_gateway.find_instance_one(self.guild_id)
        return instance_data["is_process"]

    def _get_instance_data(self) -> dict:
        """ Returns the most up-to-date entry for this instance in the database.
        """

        return self.database_gateway.find_instance_one(self.guild_id)