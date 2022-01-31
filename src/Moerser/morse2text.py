import cv2
from matplotlib import pyplot as plt
from Moerser.utils import set_logger, get_morse_alphabet


class Morse2Text:
    def __init__(self):
        self.log = set_logger("M2T", mode="debug")
        self.morse_alphabet = get_morse_alphabet()

    def decode(self, sequence):
        self.log.debug(sequence)
        text = ""
        return text
