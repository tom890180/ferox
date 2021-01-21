# from MotionDetector import MotionDetector
# from FeroxListener import FeroxListener
# from core.Logger import Logger
# import threading
# from MotionDetectorThreadHandler import MotionDetectorThreadHandler

# Logger().logger.info("Started Ferox")

# def listen():
#     FeroxListener().start_polling()

# threading.Thread(target=listen, args=()).start()
import vcgencmd
CPUc=vcgencmd.measure_temp()

print(CPUc)