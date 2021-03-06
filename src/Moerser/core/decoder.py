from Moerser.utils import set_logger, get_morse_alphabet


class Decoder:
    def __init__(self):
        self.log = set_logger("M2T", mode="debug")
        self.morse_alphabet = get_morse_alphabet()

    def decode(self, sequence):
        """
        decipher a given morse sequence

        :param sequence:
        :return:
        """
        self.log.debug(sequence)
        text = []
        sequence = sequence.split(" ")

        for subseq in sequence:
            word = []
            characters = subseq.split("/")
            for char in characters:
                if char in self.morse_alphabet:
                    word.append(self.morse_alphabet[char])
                else:
                    if char != "":
                        word.append("_")

            text.append(''.join(word))

        return ' '.join(text)


if __name__ == "__main__":
    decoder = Decoder()
    print(decoder.decode(".../---/... -. --/-."))  # testing
