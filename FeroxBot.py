import telegram
from core.Singleton import Singleton
import time
from core.Config import Config
from core.MongoDB import DB
from core.Logger import Logger
import os


class FeroxBot(Singleton):

    def __init__(self):
        self.bot = telegram.Bot(Config().get()["Telegram"]["Token"])

    def sendMessageToAll(self):
        chats = list(DB().chats.find({}))

        for chat in chats:
            self.bot.sendMessage(chat["chat_id"], "sup")

        Logger().logger.info("sendMessageToAll()")

    def sendImageToAll(self, path):
        chats = list(DB().chats.find({}))

        for chat in chats:
            self.bot.send_photo(chat["chat_id"], open(path, 'rb'))
            
        Logger().logger.info("sendImageToAll()")

        os.remove(path)