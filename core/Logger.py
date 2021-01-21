import logging
from core.Singleton import Singleton

class Logger(metaclass=Singleton):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: %(levelname)s - %(message)s')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)