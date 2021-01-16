import pymongo
from core.Singleton import Singleton
from core.Config import Config

class DB(Singleton):
    def __init__(self):
        self.client = pymongo.MongoClient(Config().get()['MongoDB']['URL'])

        if "ferox" not in self.client.list_database_names():
            raise Exception("database ferox not found")

        self.ferox = self.client["ferox"]

        if "chats" not in self.ferox.list_collection_names():
            raise Exception("database ferox not found")

        self.chats = self.ferox["chats"]
