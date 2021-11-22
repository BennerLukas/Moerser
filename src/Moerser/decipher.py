from Moerser.utils import get_morse_alphabet


class Decipher:

    def __init__(self):
        self.morse_alphabet = get_morse_alphabet()

    def morse_to_binary(self, s_input):
        # split into character (spaces)
        replaces = {46: 48, 45: 49}
        s_input_binary = s_input.translate(replaces)
        ls_input_character = s_input_binary.split(" ")
        return ls_input_character

    def match_binary_to_alphabet(self, s_input="01"):
        for character, code in self.morse_alphabet.items():
            if s_input == code:
                return character
        print("nothing found")

    def error_correction(self, s_raw_input, s_binary_input, s_alphabetic_input):
        pass

    def grammar_correction(self, s_input_phrase):
        # groß/ kleinschreibung
        pass

    def main(self, s_morse):
        ls_binary = self.morse_to_binary(s_morse)
        ls_phrase = list()
        for item in ls_binary:
            ls_phrase.append(self.match_binary_to_alphabet(item))
        s_phrase = "".join(ls_phrase)
        return s_phrase, ls_phrase
