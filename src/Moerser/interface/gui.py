import sys
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2 import QtWidgets as QtW
from PySide2.QtCore import QTimer

from Moerser.core.light2morse import Light2Morse
from Moerser.core.morse2text import Morse2Text
from Moerser.core.text2light import Text2Light
from Moerser.interface.blinker import Blinker
from Moerser.utils.periphery import Camera
from Moerser.utils import set_logger


# helping resources for GUI: https://github.com/yushulx/python/blob/master/examples/qt/barcode-reader.py
class Interface(QtW.QWidget):

    def __init__(self):
        QtW.QWidget.__init__(self)

        self.l2m = Light2Morse()
        self.m2t = Morse2Text()
        self.t2l = Text2Light()
        self.Camera = Camera()
        self.log = set_logger("GUI", mode="debug")

        self.total_sequence = None
        self.video_capture = None

        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        # Create a layout.
        layout = QtW.QVBoxLayout()

        toolbar = self._toolbox()
        layout.addLayout(toolbar)

        # setting window title
        self.setWindowTitle("Mörser")

        # Add a label
        self.label = QtW.QLabel()
        self.label.setFixedSize(640, 640)
        layout.addWidget(self.label)

        # Add a text area
        self.results = QtW.QTextEdit()
        layout.addWidget(self.results)

        # Set the layout
        self.setLayout(layout)
        self.setFixedSize(640, 750)
        self.setWindowIcon(QIcon("../assets/logo_simple_small.png"))
        self.setWindowIconText("logo")

        self._start_timer()

    def _toolbox(self):
        # creating a toolbar
        toolbar = QtW.QGridLayout()

        # # adding toolbar to main window
        # self.addToolBar(toolbar)

        # Start
        start = QtW.QPushButton("Start", self)
        start.clicked.connect(self._start_timer)
        start.setToolTip("Start the decoding")
        start.setIcon(QIcon("../assets/play.svg"))
        toolbar.addWidget(start, 0, 0)

        # Stop
        stop = QtW.QPushButton("Pause", self)
        stop.clicked.connect(self._stop_timer)
        stop.setToolTip("stop the decoding")
        stop.setIcon(QIcon("../assets/pause.svg"))
        toolbar.addWidget(stop, 0, 1)

        # Sync
        sync = QtW.QPushButton("Sync", self)
        sync.clicked.connect(self.exec_sync)
        sync.setToolTip("Init brightness values again")
        sync.setIcon(QIcon("../assets/arrow-repeat.svg"))
        toolbar.addWidget(sync, 0, 2)

        # Analyze Sequence
        analyze = QtW.QPushButton("Analyze Sequence", self)
        analyze.clicked.connect(self.exec_analzye)
        analyze.setToolTip("Analyze the Sequence to repair errors")
        analyze.setIcon(QIcon("../assets/search.svg"))
        toolbar.addWidget(analyze, 1, 0)

        # Encode Text
        encode = QtW.QPushButton("Encode Text", self)
        encode.clicked.connect(self.exec_encode)
        encode.setToolTip("Morse text to others via light")
        encode.setIcon(QIcon("../assets/pencil.svg"))
        toolbar.addWidget(encode, 1, 1)

        # setting toolbar stylesheet
        # toolbar.setStyleSheet("background : lightgrey;")

        return toolbar

    # https://stackoverflow.com/questions/1414781/prompt-on-exit-in-pyqt-application
    def closeEvent(self, event):

        msg = "Close the app?"
        reply = QtW.QMessageBox.question(self, 'Mörser - Message',
                                         msg, QtW.QMessageBox.Yes, QtW.QMessageBox.No)

        if reply == QtW.QMessageBox.Yes:
            event.accept()
            self._stop_timer()
        else:
            event.ignore()

    def _start_timer(self):
        self.Camera.openCamera()
        self.timer.start(800)

    def _stop_timer(self):
        self.timer.stop()

    def _dialog(self, text, detail_text=""):
        mbox = QtW.QMessageBox()
        mbox.setWindowTitle("Mörser - Dialog")
        mbox.setText(text)
        mbox.setDetailedText(detail_text)
        mbox.setStandardButtons(QtW.QMessageBox.Ok | QtW.QMessageBox.Cancel)

        mbox.exec_()

    def _input(self):
        text, ok = QtW.QInputDialog.getText(self, " Text to encode", "Enter text:")
        self.log.debug(text)
        self.log.debug(ok)
        return text

    def exec_sync(self):
        self.log.debug("init brightness again")
        _, grey_frame, _ = self.Camera.get_image()
        brightness_threshold = self.l2m.init_brightness(grey_frame)

        self._dialog(text="Sync Done", detail_text=f"The brightness was calibrated again to {brightness_threshold}.")

    def exec_analzye(self):
        self.log.debug("Analyze the Sequence to repair errors")
        # call analyze()
        # TODO do analyze and maybe with custom sequence?
        text = self.m2t.decode(self.total_sequence)
        text = "This is a sample Text"

        self._dialog(text="Analyze successful", detail_text=f"Following text is recognized: \n ----- \n {text}")

    def exec_encode(self):
        self.log.debug("Morse text to others via light")
        # open input field
        text = self._input()
        seq = self.t2l.encode(text)
        Blinker(seq)

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        frame, grey_frame, image = self.Camera.get_image()

        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

        self.total_sequence, bright_counter, darkness_counter = self.l2m.main(grey_frame)   # TODO needs other information

        self.log.debug(f"total_sequence: {self.total_sequence}")
        self.log.debug(f"bright_counter: {bright_counter}")
        self.log.debug(f"darkness_counter: {darkness_counter}")

        text = self.m2t.decode(self.total_sequence)

        self.results.setText(str(bright_counter))


def main():
    app = QtW.QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
