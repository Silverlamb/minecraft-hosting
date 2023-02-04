import os
import pymongo

"""
This class is a gate way to the MongoDB database where the instance and credit collections will exist.
"""
class MongoGateWay:
    def __init__(self) -> None:
        #starts the mongodb service (follow instructions on installation)
        os.system("sudo service mongod start")

        # Connects to mongodb and uses the database 'Minecraft-Hosting'
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db_minecraft_hosting = self.db_client["Minecraft-Hosting"]
        
        # Sets variables to collections that store information in a database
        self.db_credits = self.db_minecraft_hosting["credits"] 
        self.db_betaKeys = self.db_minecraft_hosting["beta_keys"]
        self.db_access = self.db_minecraft_hosting["access"]
        self.db_instances_discord = self.db_minecraft_hosting["instances_discord"]
        self.db_credit_tokens = self.db_minecraft_hosting["credit_tokens"]

        # Template dictionary to initiate
        self.instance_doc = lambda guild_id: {
            "guild_id": guild_id,
            "credits": 0.0,
            "server_state": False,
            "server_present": False,
            "is_process": False,
            "start_time": 0,
            "server_status": "Not Created Yet",
            "restrict": False,
            "instance_id": "",
            "ip": "",
            "world_name": "world",
            "minecraft_version": "1.0",
            "total_space": 0,
            "paper_build": 0,
            "jre_version": ""
        }

    """
    Used for inserting new guilds to the instance collection
    """
    def insert_instance_one(self, guild_id: int) -> bool:
        if self.db_instances_discord.count_documents({"guild_id": guild_id}) == 0:
            self.db_instances_discord.insert_one(self.instance_doc(guild_id))
            return True
        return False
    
    """
    Deletes one of the instance documents based on guild id
    """
    def delete_instance_one(self, guild_id: int) -> bool:
        self.db_instances_discord.delete_one({"guild_id": guild_id})

    """
    Checks if an instance doc exists in the database based on the guild id
    """
    def exist_instance_guild(self, guild_id: int) -> bool:
        if self.db_instances_discord.count_documents({"guild_id": guild_id}) == 0:
            return False
        return True

    """
    Returns an instance doc which is searched by the given guild id else returns an empty dict.
    """
    def find_instance_one(self, guild_id: int) -> dict:
        find = self.db_instances_discord.find_one({"guild_id": guild_id})
        if isinstance(find, type(None)):
            return {}
        return find