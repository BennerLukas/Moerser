from Moerser.utils import set_logger, get_morse_alphabet


class Encoder:
    def __init__(self):

        self.log = set_logger("L2M", mode="debug")
        self.morse_alphabet = get_morse_alphabet()

    def encode(self, text):
        self.log.debug(text)    # TODO missing logic
        sequence = ["white", "white", "black", "white", "white", "black"]
        return sequence
