from Moerser.utils import set_logger, get_morse_alphabet


class Text2Light:
    def __init__(self):

        self.log = set_logger("L2M", mode="debug")
        self.morse_alphabet = get_morse_alphabet()

    def encode(self, text):
        self.log.debug(text)    # TODO missing logic
        sequence = ["white", "white", "black", "white", "white", "black"]
        return sequence

    def get_time_sequence(self, sequence):
        self.log.debug(sequence)
        brightness = []
        return brightness
