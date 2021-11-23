from Moerser.utils import get_morse_alphabet
from Moerser.utils import set_logger


class Cipher:
    def __init__(self, mode="debug"):
        self.morse_alphabet = get_morse_alphabet()
        self.debug_level = mode
        self.log = set_logger("Moerser - Decipher", mode=mode)

    def text_to_morse(self, s_input_text="Guten Tag"):
        self.log.debug("Translate text to morse-code.")
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