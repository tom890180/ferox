import telegram
import sys
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler
import time

class FeroxBot(PatternMatchingEventHandler):
    def __init__(self, token, path, db, logger):
        self.bot = telegram.Bot(token)
        self.db = db
        self.logger = logger

        event_handler = LoggingEventHandler()

        event_handler.on_created = self.on_created

        self.observer = Observer()
        self.observer.schedule(event_handler, path, recursive=False)

    def sendMessageToAll(self):
        chats = list(self.db.chats.find({}))

        for chat in chats:
            self.bot.sendMessage(chat["chat_id"], "sup")

    def sendImageToAll(self, path):
        chats = list(self.db.chats.find({}))

        for chat in chats:
            self.bot.send_photo(chat["chat_id"], photo=open(path, 'rb'))

    def start(self):
        self.observer.start()
        try:
            while True:
                # Set the thread sleep time
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()

    def on_created(self,event):
        self.logger("File created")
        self.sendImageToAll(event.src_path)
