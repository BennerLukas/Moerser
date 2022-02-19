from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys
import time

from Moerser.light2morse import Light2Morse
from Moerser.utils import set_logger


class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.camera = None

        self.l2m = Light2Morse()
        self.log = set_logger("GUI", mode="debug")

        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.decode_morse)

        # setting geometry
        self.setGeometry(100, 100,
                         800, 600)

        # setting style sheet
        self.setStyleSheet("background : white;")

        # getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()

        # if no camera found
        if not self.available_cameras:
            # exit the code
            self.log.error("No Camera found.")
            sys.exit()

        # creating a status bar
        self.status = QStatusBar()

        # setting style sheet to the status bar
        self.status.setStyleSheet("background : white;")

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # creating a QCameraViewfinder object
        self.viewfinder = QCameraViewfinder()

        # showing this viewfinder
        self.viewfinder.show()

        # making it central widget of main window
        self.setCentralWidget(self.viewfinder)

        # Set the default camera.
        self.select_camera(0)

        # creating a tool bar
        toolbar = QToolBar("Mörser Tool Bar")

        # adding tool bar to main window
        self.addToolBar(toolbar)

        # Start
        start = QAction("Start", self)
        start.triggered.connect(self.start_timer)
        start.setStatusTip("Start the decoding")
        start.setToolTip("Start the decoding")
        toolbar.addAction(start)

        # Stop
        stop = QAction("Pause", self)
        stop.triggered.connect(self.stop_timer)
        stop.setStatusTip("Stop the decoding")
        stop.setToolTip("stop the decoding")
        toolbar.addAction(stop)

        # Sync
        sync = QAction("Sync", self)
        sync.triggered.connect(self.exec_sync)
        sync.setStatusTip("Init brightness values again")
        sync.setToolTip("Init brightness values again")
        toolbar.addAction(sync)

        # Analyze Sequence
        analyze = QAction("Analyze Sequence")
        analyze.triggered.connect(self.exec_analzye)
        analyze.setStatusTip("Analyze the Sequence to repair errors")
        analyze.setToolTip("Analyze the Sequence to repair errors")
        toolbar.addAction(analyze)

        # Encode Text
        encode = QAction("Encode Text", self)
        encode.triggered.connect(self.exec_encode)
        encode.setStatusTip("Morse text to others via light")
        encode.setToolTip("Morse text to others via light")
        toolbar.addAction(encode)

        # creating a combo box for selecting camera
        camera_selector = QComboBox()
        camera_selector.setStatusTip("Choose camera to take pictures")
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)
        camera_selector.addItems([camera.description() for camera in self.available_cameras])
        # adding action to the combo box
        # calling the select camera method
        camera_selector.currentIndexChanged.connect(self.select_camera)
        # adding this to toolbar
        toolbar.addWidget(camera_selector)

        # setting toolbar stylesheet
        toolbar.setStyleSheet("background : lightgrey;")

        # setting window title
        self.setWindowTitle("Mörser")

        # showing the main window
        self.show()

    def _dialog(self, text, detail_text=""):
        mbox = QMessageBox()
        mbox.setWindowTitle("Mörser - Dialog")
        mbox.setText(text)
        mbox.setDetailedText(detail_text)
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        mbox.exec_()

    def _input(self, text):
        text, ok = QInputDialog.getText(QWidget, " Text to encode", "Enter text:")
        self.log.debug(text)
        self.log.debug(ok)
        return text

    def exec_sync(self):
        self.log.debug("init brightness again")
        # call to init_brightness()

        self._dialog(text="Sync Done", detail_text="The brightness was calibrated again.")

    def exec_analzye(self):
        self.log.debug("Analyze the Sequence to repair errors")
        # call analyze()
        text = "This is a sample Text"

        self._dialog(text="Analyze successful", detail_text=f"Following text is recognized: \n ----- \n {text}")

    def exec_encode(self):
        self.log.debug("Morse text to others via light")
        # open input field
        text = self._input()

    def start_timer(self):
        self.timer.start(800)

    def stop_timer(self):
        self.timer.stop()

    def select_camera(self, i):
        # getting the selected camera
        self.camera = QCamera(self.available_cameras[i])

        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)

        # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureStillImage)

        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))

        # start the camera
        self.camera.start()

        # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)

        # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error,
                                          msg: self.alert(msg))

        # when image captured showing message
        self.capture.imageCaptured.connect(lambda d,
                                                  i: self.status.showMessage("Image captured : "
                                                                             + str(self.save_seq)))

        # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()

        # initial save sequence
        self.save_seq = 0

        # self.timer.start(1000. / 24)

    def alert(self, msg):
        # error message
        error = QErrorMessage(self)

        # setting text to the error message
        error.showMessage(msg)

    def decode_morse(self):
        self.log.debug(self.capture)
        self.log.debug(self.capture.capture())

        self.l2m.main(self.capture)


if __name__ == "__main__":
    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = Interface()

    # start the app
    sys.exit(App.exec())
