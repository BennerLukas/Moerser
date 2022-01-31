import sys

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QGridLayout

from Moerser.light2morse import Light2Morse
from Moerser.periphery import Camera
from Moerser.utils import set_logger


class Logic:
    def __init__(self, view):
        self.model = None
        self.view = view


class Interface(QMainWindow):

    def __init__(self, parent=None):
        self.log = set_logger("GUI", mode="debug")

        self.light_converter = Light2Morse()


        super().__init__(parent)
        self.setWindowTitle('Mörser')
        self.setFixedSize(900, 600)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._buttons()

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        self.cam = Camera()
        self.timer.start(1000. / 24)

    def _buttons(self):
        buttonsLayout = QGridLayout()

        # Sync
        sync = QPushButton("Sync")
        sync.setToolTip("Init brightness values again")
        sync.clicked.connect(self.exec_sync)
        buttonsLayout.addWidget(sync, 0, 0)

        # Analyze Sequence
        analyze = QPushButton("Analyze Sequence")
        analyze.clicked.connect(self.exec_analzye)
        analyze.setToolTip("Analyze the Sequence to repair errors")

        buttonsLayout.addWidget(analyze, 0, 1)

        # Encode Text
        encode = QPushButton("Encode Text")
        encode.clicked.connect(self.exec_encode)
        encode.setToolTip("Morse text to others via light")
        buttonsLayout.addWidget(encode, 0, 2)

        self.generalLayout.addLayout(buttonsLayout)

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

    def _image(self, frame):
        image = QImage(frame.tostring(), frame.width, frame.height, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)

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
        self._input()

    def next_frame(self):
        # current_frame, total_sequence, bright_counter, darkness_counter, = self.light_converter.main()
        current_frame = self.cam.get_frame()
        image = QImage(current_frame, current_frame.shape[1], current_frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)




def main():
    moerser = QApplication(sys.argv)
    view = Interface()
    view.show()

    # Execute main loop
    sys.exit(moerser.exec_())


if __name__ == "__main__":
    main()
