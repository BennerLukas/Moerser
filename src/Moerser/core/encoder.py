from Moerser.utils import set_logger, get_morse_alphabet


class Encoder:
    def __init__(self):

        self.log = set_logger("L2M", mode="debug")
        self.morse_alphabet = get_morse_alphabet()

        self.space_waiter = 6
        self.character_waiter = 3
        self.word_waiter = 7

        self.dot = 3
        self.dash = 5

    def encode(self, text):
        morse_seq = self.morse_encode(text)
        light_seq = self.light_encode(morse_seq)
        return light_seq

    def morse_encode(self, text):
        self.log.debug(text)
        text = text.lower()

        morse_symbol = list(get_morse_alphabet().keys())
        character_symbol = list(get_morse_alphabet().values())

        morse_sequence = ""
        for character in text:
            if character == " ":
                if morse_sequence[-1] == "/":   # remove "/ " combinations
                    morse_sequence = morse_sequence[:-1]
                morse_sequence += " "
            else:
                try:
                    position = character_symbol.index(character)
                except ValueError:
                    self.log.error("Value not able to morse")
                    raise

                morse_sequence += morse_symbol[position]
                morse_sequence += "/"

        if morse_sequence[-1] == "/":   # remove last /
            morse_sequence = morse_sequence[:-1]

        self.log.debug(morse_sequence)
        return morse_sequence

    def light_encode(self, morse_sequence):
        sequence = []
        for character in morse_sequence:
            if character == ".":
                [sequence.append("white") for _ in range(2)]
                [sequence.append("black") for _ in range(2)]
            elif character == "-":
                [sequence.append("white") for _ in range(5)]
                [sequence.append("black") for _ in range(2)]
            elif character == "/":
                [sequence.append("black") for _ in range(5)]
            elif character == " ":
                [sequence.append("black") for _ in range(7)]

        self.log.debug(sequence)
        return sequence


if __name__ == "__main__":
    encoder = Encoder()
    texts = "sos n mn"
    # print(encoder.morse_encode(texts))
    encoder.encode(texts)
