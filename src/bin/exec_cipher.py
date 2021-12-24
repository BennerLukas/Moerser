from Moerser.cipher import Cipher

if __name__ == '__main__':

    morse = Cipher("debug")
    result = morse.text_to_morse()
    seq = morse.translate_binary2color_sequence(result)
    morse.display_morse(seq)
    print(result)
