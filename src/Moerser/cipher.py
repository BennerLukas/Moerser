from Moerser.utils import get_morse_alphabet
from Moerser.utils import set_logger
import tkinter as tk
from itertools import cycle


class Cipher:
    def __init__(self, mode="debug"):
        self.morse_alphabet = get_morse_alphabet()
        self.debug_level = mode
        self.log = set_logger("Moerser - Cipher", mode=mode)

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

    def flatten(self, liste):
        """Flatten a list using generators comprehensions.
            Returns a flattened version of list lst.

            by https://miguendes.me/python-flatten-list#how-to-flatten-list-of-strings-tuples-or-mixed-types
        """

        for sublist in liste:
            if isinstance(sublist, list):
                for item in sublist:
                    yield item
            else:
                yield sublist

    def translate_binary2color_sequence(self, ls_binary=None):
        if ls_binary is None:
            ls_binary = ['110', '001', '1', '0', '10', '0000000', '1', '01', '110']

        sequence = list()
        character_space = ["white" for _ in range(3)]   # 3 units white between individual letters
        word_space = ["white" for _ in range(7)]        # 7 units white between words
        for character in ls_binary:
            sequence.append(word_space)

            if character == "0000000":
                sequence.append(word_space)

            for part in character:
                if part == "0":
                    sequence.append("black")
                elif part == "1":
                    sequence.append(["black" for _ in range(3)])
                else:
                    raise
                sequence.append("white")    # one unit between parts of same character
            sequence.append(character_space)
        # flatten sequence
        flattend_sequence = list(self.flatten(sequence))
        self.log.debug(sequence)
        return flattend_sequence

    def display_morse(self, color_sequence=None, frequency=1000):
        if color_sequence is None:
            color_sequence = ["White", "White", "Black", "Black"]

        # append stop symbol
        color_sequence.append("red")

        root = tk.Tk()
        root.title("Moerser")
        frame = tk.Frame(root, width=260, height=200, background="green")
        frame.pack()
        color_gen = cycle(color_sequence)

        def __change_color():
            frame.config(background=next(color_gen))
            root.after(frequency, __change_color)

        __change_color()
        root.mainloop()

    def execute(self, s_text):
        binary_morse = self.text_to_morse(s_text)
        sequence = self.translate_binary2color_sequence(binary_morse)
        self.display_morse(sequence)
        return sequence
