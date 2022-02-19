import cv2 as cv
from Moerser.utils import set_logger
import time


class Camera:

    def __init__(self, camera_id, mode="debug"):

        self.debug_level = mode
        self.log = set_logger("Moerser - Camera", mode=mode)

        #self.video_capture = cv.VideoCapture(camera_id)
        self.video_capture = cv.VideoCapture(camera_id)
        self.log.debug("Camera starting")
        time.sleep(1)
        self.returned, self.frame = self.video_capture.read()
        time.sleep(1)

    # Frame generation for Browser streaming
    def get_frame(self):
        returned, image = self.video_capture.read()
        if not returned:
            self.log.error("Can't receive frame (stream end?). Exiting ...")
            raise
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        return gray_image

    @staticmethod
    def calc_mean_brightness(img):
        return img.mean(axis=0).mean(axis=0)

    def record_sequence(self, iterations=10):
        recorded_morse = list()
        image = self.get_frame()
        prev_brightness = self.calc_mean_brightness(image)

        # initial guess
        if prev_brightness > 200:       # big number -> bright -> 1
            recorded_morse.append("H")
        else:
            recorded_morse.append("L")
        self.log.info(f"Intial Guess {recorded_morse[-1]}")

        tolerance = 0.25       # change must be at least 25% compared to before
        frequency_delay = 1
        while True:
            image = self.get_frame()
            brightness = self.calc_mean_brightness(image)
            if brightness > prev_brightness * (1 + tolerance):      # significantly brighter than before
                # change from dark to bright
                recorded_morse.append("H")
            elif prev_brightness > brightness * (1 + tolerance):    # significantly darker than before
                # change from bright to dark
                recorded_morse.append("L")
            else:
                last_item = len(recorded_morse) - 1
                recorded_morse.append(recorded_morse[last_item])    # no change append last status again
            time.sleep(frequency_delay)
            self.log.info(recorded_morse[-1])   # log last entry

    def __del__(self):
        self.video_capture.release()
        cv.destroyAllWindows()
        self.log.info("Camera stopped")
        return ()

