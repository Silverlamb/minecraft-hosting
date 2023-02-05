import os
import pymongo

"""
This class is a gate way to the MongoDB database where the instance and credit collections will exist.
"""
class MongoGateway:
    def __init__(self) -> None:
        #starts the mongodb service (follow instructions on installation)
        os.system("sudo service mongod start")

        # Connects to mongodb and uses the database 'Minecraft-Hosting'
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db_minecraft_hosting = self.db_client["Minecraft-Hosting"]
        
        # Sets variables to collections that store information in a database
        self.db_instances = self.db_minecraft_hosting["instances"]

        # Template dictionary to initiate
        self.instance_doc = lambda guild_id: {
            "guild_id": guild_id,
            "credits": 2000.0, # TODO DEMO ONLY: Reset to 0.
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
    Used for inserting one new guilds to the instance collection
    """
    def insert_instance_one(self, guild_id: int) -> bool:
        if not self.exist_instance_guild(guild_id):
            self.db_instances.insert_one(self.instance_doc(guild_id))
            return True
        return False
    
    """
    Deletes one of the instance documents based on guild id
    True if the document is deleted and False if the document isn't deleted (possibly because it doesn't exist)
    """
    def delete_instance_one(self, guild_id: int) -> bool:
        deleted = self.db_instances.delete_one({"guild_id": guild_id})
        if deleted.deleted_count == 0:
            return False
        return True

    """
    Checks if an instance doc exists in the database based on the guild id
    True if the document does exist and False if document doesn't
    """
    def exist_instance_guild(self, guild_id: int) -> bool:
        if self.db_instances.count_documents({"guild_id": guild_id}) == 0:
            return False
        return True

    """
    Returns one instance doc which is searched by the given guild id else returns an empty dict
    """
    def find_instance_one(self, guild_id: int) -> dict:
        find = self.db_instances.find_one({"guild_id": guild_id})
        if isinstance(find, type(None)):
            return {}
        return find

    """
    Updates one document with update_query in the instance collection which is search for with the guild_id
    True if the document is updated and False if the document failed to update
    """
    def update_instance_one(self, guild_id: int, update_query: dict) -> bool:
        server_instances_query = {"guild_id": guild_id}
        update_instance_query = {"$set": update_query}
        updated = self.db_instances.update_one(server_instances_query, update_instance_query)
        if updated.modified_count == 0:
            return False
        return True