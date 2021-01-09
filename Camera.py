from picamera import PiCamera
from picamera.array import PiRGBArray
import time

# https://picamera.readthedocs.io/en/release-1.10/api_camera.html

class Camera:
    def __init__(self):
        self.camera = PiCamera()

        self.camera.resolution = (1536, 1088)
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.sharpness = 100
        self.camera.saturation = -100

        # night
        self.camera.framerate = 4.5
        self.camera.shutter_speed = 500000
        self.camera.iso = 800
        self.camera.exposure_mode = "night"

        # day
        # self.camera.framerate = 4.5
        # self.camera.shutter_speed = 10000
        # self.camera.iso = 200
        # self.camera.exposure_mode = "off"

    
    def Capture(self):
        raw = PiRGBArray(self.camera)
        self.camera.capture(raw, format="bgr")
        return raw.array

    def CaptureToFile(self, filename):
        self.camera.start_preview()
        time.sleep(1)

        self.camera.capture(filename)
