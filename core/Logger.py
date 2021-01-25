import logging
from core.Singleton import Singleton
import sys
from core.Config import Config

class Logger(metaclass=Singleton):
    def __init__(self):
        filename = Config().get()['Logger']['Path']

        if(filename == "None"):
            filename = None

        logging.basicConfig(level=logging.CRITICAL,filename=filename,
                    format='[%(asctime)s]: %(levelname)s - %(message)s')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)


def my_handler(type, value, tb):
    Logger().logger.exception("Uncaught exception: {0}".format(str(value)))

# Install exception handler
sys.excepthook = my_handler
