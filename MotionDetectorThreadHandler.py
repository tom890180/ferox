import threading
from core.Singleton import Singleton
import time
import MotionDetector
import datetime
from Camera import Camera



class MotionDetectorThreadHandler(metaclass=Singleton):
    def __init__(self):
        self.thread = threading.Thread(target=self.motiondetector, args=())
        self.stop = False
        self.sendLatest = False
        self.ThreadHasBeenRun = False

    def startThread(self):
        if self.ThreadHasBeenRun:
            self.thread = threading.Thread(target=self.motiondetector, args=())
            self.stop = False

        if not self.thread.is_alive():
            self.ThreadHasBeenRun = True
            self.thread.start()

    def is_alive(self):
        return self.thread.is_alive()

    def doSendLatest(self, chat_id):
        if self.is_alive():
            self.sendLatest = True
        else: 
            Camera().sendLatest(chat_id)
    
    def killThread(self):
        self.stop = True
        if self.thread.is_alive():
            self.thread.join()

    def motiondetector(self):
        MotionDetector.MotionDetector(self).start()
