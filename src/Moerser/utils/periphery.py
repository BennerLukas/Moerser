from PySide2.QtGui import QImage
from PySide2 import QtWidgets as QtW
import cv2
from Moerser.utils import set_logger
from scipy.signal import convolve2d

class Camera:

    def __init__(self, mode="debug"):

        self.debug_level = mode
        self.log = set_logger("Moerser - Camera", mode=mode)

        self.video_capture = None

    @staticmethod
    def calc_mean_brightness(img):  # TODO sync on dark --> easier?
        return img.mean(axis=0).mean(axis=0)

    def openCamera(self, camera_number=0):
        self.video_capture = cv2.VideoCapture(camera_number)
        # vc.set(5, 30)  #set FPS
        self.video_capture.set(3, 640)  # set width
        self.video_capture.set(4, 480)  # set height

        if not self.video_capture.isOpened():
            self.log.error("Failed to open camera.")
            msgBox = QtW.QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return False

    def get_image(self):
        rval, frame = self.video_capture.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh, bw_frame = cv2.threshold(grey_frame, 220, 255, cv2.THRESH_BINARY)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        return frame, grey_frame, bw_frame, image
