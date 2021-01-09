import cv2
import datetime
from Camera import Camera
from DetectMotion import DetectMotion

cam = Camera()

folder = "images/"
extension = ".jpg"

while True:
    time_string = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    print(time_string)

    name = '%s' % time_string
    img1 = cam.Capture()
    img2 = cam.Capture()

    dm = DetectMotion(img1, img2)

    (motion_found, img1_1, img2_1, contourCount, img2_processed, nonZero) = dm.detect_motion()

    print(contourCount)

    if not motion_found:
        continue

    cv2.imwrite('%s%s_c%s_01%s' % (folder, name, nonZero, extension), img1_1)
    cv2.imwrite('%s%s_c%s_02%s' % (folder, name, nonZero, extension), img2_1)
