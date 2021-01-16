from MotionDetector import MotionDetector
from FeroxListener import FeroxListener
from core.Logger import Logger
import threading

Logger().logger.info("Started Ferox")

def listen():
    FeroxListener().start_polling()


def motiondetector():
    MotionDetector().start()

threading.Thread(target=listen, args=()).start()
threading.Thread(target=motiondetector, args=()).start()

