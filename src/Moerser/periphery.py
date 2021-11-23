import cv2
from Moerser.utils import set_logger


class Camera:

    def __init__(self, mode="debug"):
        self.debug_level = mode
        self.log = set_logger("Moerser - Camera", mode=mode)

    def image_to_morse(self, image, short=".", long="-", word_space=""):
        pass

    def analyze_stream(self):
        """
        predict what's dot and whats dash based on whole stream.
        :return:
        """


class Microphone:
    def __init__(self, mode="debug"):
        self.debug_level = mode
        self.log = set_logger("Moerser - Microphone", mode=mode)
