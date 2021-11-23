# import unittest
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()

from Moerser.decipher import Decipher

morse = Decipher()
s_input_value = ".... .. ....... .-.. ..- -.- .- ..."   # HI LUKAS
result = morse.execute(s_input_value)

print(result)
