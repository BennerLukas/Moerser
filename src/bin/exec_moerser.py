from Moerser.decipher import Decipher

if __name__ == '__main__':

    morse = Decipher("info")
    s_input_value = ".... .. ....... .-.. ..- -.- .- ..."   # HI LUKAS
    result = morse.execute(s_input_value)

    print(result)
