import pymongo

class DB:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)

        if "ferox" not in self.client.list_database_names():
            raise Exception("database ferox not found")

        self.ferox = self.client["ferox"]

        if "chats" not in self.ferox.list_collection_names():
            raise Exception("database ferox not found")

        self.chats = self.ferox["chats"]
