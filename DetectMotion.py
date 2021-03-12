import cv2
from datetime import datetime

class DetectMotion:
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2

    def detect_motion(self):
        img1_processed = self.preliminary_image_process(self.img1)
        img2_processed = self.preliminary_image_process(self.img2)

        delta = cv2.absdiff(img1_processed, img2_processed)

        threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]

        (contours, _) = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contourCount = 0
        
        dilate_image = cv2.dilate(threshold, None, iterations=2)
        nonZero = cv2.countNonZero(dilate_image)

        for contour in contours:
            if cv2.contourArea(contour) < 15: continue

            contourCount = contourCount + 1

            (x, y, w, h)=cv2.boundingRect(contour)
            cv2.rectangle(self.img2, (x, y), (x+w, y+h), (120,30,120), 1)

        motion_found = False
        if(contourCount >= 1):
            motion_found = True

        self.img2 = self.add_timestamp(self.img2)

        return motion_found, self.img1, self.img2, contourCount, img2_processed, nonZero

    def preliminary_image_process(self, image):
        #image = cv2.rectangle(image, (420, 100), (570, 220), (0,0,0), -1)
        #image = cv2.rectangle(image, (10, 280), (100, 400), (0,0,0), -1)

        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gaussian_frame = cv2.GaussianBlur(grey, (21, 21), 0)
        blur_frame = cv2.blur(gaussian_frame, (5, 5))

        return blur_frame

    def add_timestamp(self, img):
        return cv2.putText(img, '%s' % datetime.now().strftime("%d.%m.%Y %H:%M:%S"), (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,0,255), 1)
