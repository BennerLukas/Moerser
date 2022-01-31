from Moerser2.utils import get_morse_alphabet, set_logger

class Decode:
    def __init__(self, mode="debug"):
        self.morse_alphabet = get_morse_alphabet()
        self.debug_level = mode
        self.log = set_logger("Moerser - Decipher", mode=mode)

    def calc_mean_brightness(self, img):
        return img.mean(axis=0).mean(axis=0)

    def set_inital_brightness(self):
        # Set inital brighness to "train" the default/ ambiente brightness
        img = camera.get_frame()
        brightness = self.calc_mean_brightness(image)
        return brightness

    def execute(self):
        tolerance = 0.25
        default_brightness = self.set_inital_brightness()

        bright_counter = 0
        dark_counter = 0
        sequence = list()

        # "." --> 1 Unit (bright)
        # "-" --> 3 Units (bright)
        # "" --> 3 Units (next Character in word) (dark)
        # " " --> 7 Units (next word) (dark)
        while True:
            img = camera.get_frame()
            frame_brightness = self.calc_mean_brightness(img)

            if frame_brightness >= brightness_threshold * (1 - tolerance):
                # frame is bright
                bright_counter+=1

            # frame is dark
            # how high is the counter
            elif bright_counter == 0:
                dark_counter += 1


            # if frame_brightness == dark
            else:
                # fallunterscheidung
                if bright_counter == 1:
                    sequence.append(".")
                    bright_counter == 0

                elif bright_counter == 3:
                    sequence.append("-")
                    bright_counter == 0