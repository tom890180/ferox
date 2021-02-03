import cv2
import datetime
from Camera import Camera
from DetectMotion import DetectMotion
from core.Logger import Logger
from core.Config import Config
from FeroxBot import FeroxBot
import time

class MotionDetector:
    def __init__(self, handler):
        self.folder = Config().get()["MotionDetector"]["Folder"]
        self.extension = Config().get()["MotionDetector"]["Extension"]
        self.handler = handler

        self.cam = Camera()
        
    def start(self):
        Logger().logger.info("MotionDetector started")

        while True:
            if self.handler.stop: break

            time_string = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            name = '%s' % time_string
            img1 = self.cam.Capture()
            img2 = self.cam.Capture()

            if(self.handler.sendLatest):
                self.handler.sendLatest = False

                path = '%s%s_c%s_02%s' % (self.folder, name, nonZero, self.extension)
                cv2.imwrite(path, img1)
                FeroxBot().sendImageToAll(path)

            dm = DetectMotion(img1, img2)

            (motion_found, img1_1, img2_1, contourCount, img2_processed, nonZero) = dm.detect_motion()

            if not motion_found:
                continue

            Logger().logger.info("Motion detected: %s", contourCount)
            
            path = '%s%s_c%s_02%s' % (self.folder, name, nonZero, self.extension)

            #cv2.imwrite('%s%s_c%s_01%s' % (self.folder, name, nonZero, self.extension), img1_1)
            cv2.imwrite(path, img2_1)

            FeroxBot().sendImageToAll(path)

