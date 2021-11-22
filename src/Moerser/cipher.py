from Moerser.utils import get_morse_alphabet


class Cipher:
    def __init__(self):
        self.morse_alphabet = get_morse_alphabet()

    def text_to_morse(self, s_input_text="Guten Tag"):
        s_input_text = s_input_text.upper()
        ls_morse_phrase = list()
        for input_char in s_input_text:
            for character, code in self.morse_alphabet.items():
                if input_char == character:
                    ls_morse_phrase.append(code)
                    break
        return ls_morse_phrase

    def morse_to_light(self, ls_morse):
        pass