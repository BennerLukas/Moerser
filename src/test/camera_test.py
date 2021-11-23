import cv2
from Moerser.utils import set_logger


class Camera:

    def __init__(self, mode="debug"):
        self.debug_level = mode
        self.log = set_logger("Moerser - Camera", mode=mode)

    def image_to_morse(self, image, short=".", long="-", word_space=".......", time_unit=5):
        pass

    def binary_to_light(self, ls_phrase):
        pass
