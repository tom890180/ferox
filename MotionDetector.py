import cv2
import datetime
from Camera import Camera
from DetectMotion import DetectMotion

class MotionDetector:
    def __init__(self, folder, extension, logger):
        self.folder = folder
        self.extension = extension
        self.logger = logger

        self.cam = Camera()
        
    def start(self):
        self.logger.info("MotionDetector started")

        while True:
            time_string = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            self.logger.info("Image taken")

            name = '%s' % time_string
            img1 = self.cam.Capture()
            img2 = self.cam.Capture()

            dm = DetectMotion(img1, img2)

            (motion_found, img1_1, img2_1, contourCount, img2_processed, nonZero) = dm.detect_motion()

            if not motion_found:
                continue

            self.logger.info("Motion detected: %s", contourCount)

            #cv2.imwrite('%s%s_c%s_01%s' % (self.folder, name, nonZero, self.extension), img1_1)
            cv2.imwrite('%s%s_c%s_02%s' % (self.folder, name, nonZero, self.extension), img2_1)
