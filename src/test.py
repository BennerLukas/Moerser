global morse_alphabet
morse_alphabet = {'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0', 'F': '0010', 'G': '110', 'H': '0000',
              'I': '00', 'J': '0111', 'K': '101', 'L': '0100', 'M': '11', 'N': '10', 'O': '111', 'P': '0110',
              'Q': '1101', 'R': '010', 'S': '000', 'T': '1', 'U': '001', 'V': '0001', 'W': '011', 'X': '1001',
              'Y': '1011', 'Z': '1100', '0': '11111', '1': '01111', '2': '00111', '3': '00011', '4': '00001',
              '5': '00000', '6': '10000', '7': '11000', '8': '11100', '9': '11110'}

# input
s_input_value = ".... .. ....... .-.. ..- -.- .- ..."


def get_camera_input():
    pass


def detect_relevant_image_part():
    pass


def debug_sync():
    pass


def morse_to_binary(s_input):
    # split into character (spaces)
    replaces = {46: 48, 45: 49}
    s_input_binary = s_input.translate(replaces)
    ls_input_character = s_input_binary.split(" ")
    return ls_input_character


def match_binary_to_alphabet(s_input="01"):
    for character, code in morse_alphabet.items():
        if s_input == code:
            return character

def error_correction(s_raw_input, s_binary_input, s_alphabetic_input):
    pass

print(match_binary_to_alphabet())
# print(morse_to_binary(s_input_value))
