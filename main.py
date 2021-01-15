import logging
from MotionDetector import MotionDetector
from FeroxListener import FeroxListener
from FeroxBot import FeroxBot
from Config import Config
from MongoDB import DB
import threading


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cfg = Config()

db = DB(cfg.get()["MongoDB"]["URL"])

logger.info("Started Ferox")

def listen(token, db, logger):
    FeroxListener(token, db, logger).start_polling()

def bot(token, path, db, logger):
    FeroxBot(token, path, db, logger).start()

def motiondetector(folder, extension, logger):
    MotionDetector(folder, extension, logger).start()

token = cfg.get()["Telegram"]["Token"]

threading.Thread(target=bot, args=(token, cfg.get()["FeroxBot"]["Path"], db, logger)).start()
threading.Thread(target=motiondetector, args=(cfg.get()["MotionDetector"]["Folder"], cfg.get()["MotionDetector"]["Extension"], logger)).start()

