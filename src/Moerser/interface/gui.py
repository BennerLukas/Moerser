import time
import webbrowser
import sys
from PySide2 import QtCore
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2 import QtWidgets as QtW
from PySide2.QtCore import QTimer

from Moerser.core.decoder import Decoder
from Moerser.core.encoder import Encoder
from Moerser.interface.blinker import Blinker
from Moerser.utils.periphery import Camera
from Moerser.core.interpreter import Interpreter
from Moerser.utils import set_logger


# helping resources for GUI: https://github.com/yushulx/python/blob/master/examples/qt/barcode-reader.py
class Interface(QtW.QWidget):

    def __init__(self):
        QtW.QWidget.__init__(self)

        self.m2t = Decoder()
        self.t2l = Encoder()
        self.Camera = Camera()
        self.Interpreter = Interpreter()

        self.log = set_logger("GUI", mode="debug")

        self.total_sequence = None
        self.frame_throttle = 1   # throttle limit
        self.startTime = time.time()
        self.nowTime = None

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
        # self.label.setFixedWidth(800)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Add a text area
        self.results = QtW.QTextEdit()
        layout.addWidget(self.results)

        # Set the layout
        self.setLayout(layout)
        self.setFixedSize(800, 800)
        self.setWindowIcon(QIcon("../assets/logo_simple_small.png"))
        self.setWindowIconText("logo")

        self._start_timer()

    def _toolbox(self):
        """

        :return:
        """
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

        # Clear Sequence Sequence
        analyze = QtW.QPushButton("Clear", self)
        analyze.clicked.connect(self.exec_clear)
        analyze.setToolTip("Clear the current output")
        analyze.setIcon(QIcon("../assets/trash3.svg"))
        toolbar.addWidget(analyze, 1, 0)

        # Encode Text
        encode = QtW.QPushButton("Encode Text", self)
        encode.clicked.connect(self.exec_encode)
        encode.setToolTip("Morse text to others via light")
        encode.setIcon(QIcon("../assets/pencil.svg"))
        toolbar.addWidget(encode, 1, 1)

        # Help
        encode = QtW.QPushButton("Help", self)
        encode.clicked.connect(self.exec_help)
        encode.setToolTip("Link to the documentation")
        encode.setIcon(QIcon("../assets/question-circle.svg"))
        toolbar.addWidget(encode, 1, 2)

        # setting toolbar stylesheet
        # toolbar.setStyleSheet("background : lightgrey;")

        return toolbar

    # https://stackoverflow.com/questions/1414781/prompt-on-exit-in-pyqt-application
    def closeEvent(self, event):
        """

        :param event:
        :return:
        """

        msg = "Close the app?"
        reply = QtW.QMessageBox.question(self, 'Mörser - Message',
                                         msg, QtW.QMessageBox.Yes, QtW.QMessageBox.No)

        if reply == QtW.QMessageBox.Yes:
            event.accept()
            self._stop_timer()
        else:
            event.ignore()

    def _start_timer(self):
        """

        :return:
        """
        self.Camera.openCamera()
        self.timer.start(1)

    def _stop_timer(self):
        """

        :return:
        """
        self.timer.stop()

    def _dialog(self, text, detail_text=""):
        """

        :param text:
        :param detail_text:
        :return:
        """
        mbox = QtW.QMessageBox()
        mbox.setWindowTitle("Mörser - Dialog")
        mbox.setText(text)
        mbox.setDetailedText(detail_text)
        mbox.setStandardButtons(QtW.QMessageBox.Ok | QtW.QMessageBox.Cancel)

        mbox.exec_()

    def _input(self):
        """

        :return:
        """
        text, ok = QtW.QInputDialog.getText(self, " Text to encode", "Enter text:")
        self.log.debug(text)
        self.log.debug(ok)
        return text

    def exec_sync(self):
        """

        :return:
        """
        self.log.debug("init brightness again")
        _, grey_frame, bw_frame, _ = self.Camera.get_image()
        brightness_threshold = self.Interpreter.set_baseline(bw_frame)

        self._dialog(text="Sync Done", detail_text=f"The brightness was calibrated again to {brightness_threshold}.")

    def exec_clear(self):
        """

        :return:
        """
        self.log.debug("Clear the current sequence")
        self.total_sequence = ""
        self.Interpreter = Interpreter()
        self.results.setText("")

        self._dialog(text="Clear successful", detail_text=f"Following sequence is deleted: \n ----- \n {self.total_sequence}")

    def exec_encode(self):
        """

        :return:
        """
        self.log.debug("Morse text to others via light")
        # open input field
        text = self._input()
        seq = self.t2l.encode(text)
        Blinker(seq, self.frame_throttle)

    def exec_help(self):
        """

        :return:
        """
        self.log.debug("Open help")
        url = "https://github.com/BennerLukas/Moerser/"
        webbrowser.open(url)

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        """
        Periodically (depending on frame_throttle)
        interprets a frame. 

        :return:
        """
        self.nowTime = time.time()

        frame, grey_frame, bw_frame, image = self.Camera.get_image()

        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

        if (self.nowTime - self.startTime) > self.frame_throttle:
            self.log.debug(self.nowTime - self.startTime)

            self.total_sequence, bright_counter, darkness_counter, translation, sequence = self.Interpreter.main(bw_frame)

            self.log.debug(f"total_sequence: {self.total_sequence}")
            self.log.debug(f"bright_counter: {bright_counter}")
            self.log.debug(f"darkness_counter: {darkness_counter}")

            # translation = self.m2t.decode(self.total_sequence)

            text = f"Total Input: {self.total_sequence}\nCurrent Input: {sequence}\nTranslation: {translation}\nbright_counter: {bright_counter}    |    darkness_counter: {darkness_counter}"
            self.results.setText(text)
            self.startTime = time.time()  # reset time
        return True


def main():
    app = QtW.QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
