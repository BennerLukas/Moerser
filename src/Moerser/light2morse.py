import cv2
from matplotlib import pyplot as plt
from Moerser.utils import set_logger
from Moerser.periphery import Camera


class Light2Morse:
    def __init__(self, tolerance=0.05):

        self.log = set_logger("L2M", mode="debug")

        # self.camera_p = Camera()
        self.frame_count = 0
        self.frames = 1  # Frame per second
        self.brightness_threshold = 0
        self.tolerance = tolerance
        self.bright_counter = 0
        self.darkness_counter = 0
        self.sequence = ""
        self.total_sequence = " "
        self.frame_brightness = None

    def init_brightness(self, current_frame):
        # current_frame = self.camera_p.get_frame()
        self.frame_brightness = Camera.calc_mean_brightness(current_frame)
        self.log.info(f"Threshold initiated  at {self.frame_brightness}")
        self.brightness_threshold = self.frame_brightness

    def main(self, current_frame):
        self.log.debug(current_frame)
        # current_frame = self.camera_p.get_frame()
        self.frame_brightness = Camera.calc_mean_brightness(current_frame)

        # If first frame -> set avg brightness 2 threshold
        if self.frame_count == 0:
            self.init_brightness()

        # Track brightness
        if self.frame_brightness > self.brightness_threshold * (1 + self.tolerance):
            self.bright_counter += 1
            darkness_counter = 0
            self.log.info(f"Current Brightness Counter: {self.bright_counter}")
            self.log.info(f"Current Darkness Counter: {self.darkness_counter}")

        else:
            # Decoding light to morse code
            self.darkness_counter += 1
            self.log.info(f"Current Brightness Counter: {self.bright_counter}")
            self.log.info(f"Current Darkness Counter: {self.darkness_counter}")

            # Brightness
            if self.bright_counter in range(1, (5 * self.frames)):
                self.sequence = "."
                # self.log.info(".")
                # bright_counter = 0
            elif self.bright_counter >= (5 * self.frames):
                self.sequence = "-"
                # self.log.info("-")
                # bright_counter = 0

            # Darkness
            if self.darkness_counter in range(1, (7 * self.frames)):
                # next character in word
                self.total_sequence += self.sequence
                self.sequence = ""
                self.bright_counter = 0

            elif self.darkness_counter > (7 * self.frames):
                # next word
                # total_sequence += sequence # not needed because a darkness_counter of 1 will push sequence already
                # sequence = ""
                if self.total_sequence[-1] != " ":
                    self.total_sequence += " "

                self.bright_counter = 0

            self.log.info(f"Current sequence: {self.total_sequence}")

        self.frame_count += 1

        return current_frame, self.total_sequence, self.bright_counter, self.darkness_counter,

        # cv2.putText(current_frame, f"Morse_Code: {self.total_sequence}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
        #             (0, 0, 255), 2)
        #
        # # TODO: After space, translate current morse code
        # # TODO: show current sequence in frame
        # # TODO: Button to initiate avg baseline
        #
        # cv2.imshow("webcam", current_frame)
        #
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # cv2.waitKey(500)  # one frame per second