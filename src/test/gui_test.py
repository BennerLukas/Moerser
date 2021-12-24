from tkinter import *
from tkinter import ttk
from itertools import cycle

root = Tk()
root.title("Title")

frame = Frame(root, width=260, height=200)
frame.pack()
ls_morse_sequence = ["L", "L", "H", "H", "L", "H",]
ls_morse_sequence = ls_morse_sequence.replace("L", "white")
ls_morse_sequence = ls_morse_sequence.replace("L", "white")
colors = ['red', 'green', 'orange', 'blue']
color_gen = cycle(colors)


def ChangeColor():
    frame.config(bg=next(color_gen))
    root.after(1000, ChangeColor)

# btn = ttk.Button(frame, text='Change color', command=ChangeColor)
# btn.place(x=80, y=100)
ChangeColor()
root.mainloop()

# import time
# from tkinter import *
#
#
# def change_color():
#     current_color = box.cget("background")
#     next_color = "green" if current_color == "red" else "red"
#     box.config(background=next_color)
#     root.after(1000, change_color)
#
#
# def display_morse(ls_morse_sequence=["L", "L", "H", "H", "L", "H",], frequency_delay=10):
#     for state in ls_morse_sequence:
#         time.sleep(3)
#         if state == "L":
#             print("White")
#             next_color = "white"
#         else:                       # if state == "H":
#             print("Black")
#             next_color = "black"
#         box.config(background=next_color)
#         # root.after(1000, change_color)
#
#
# root = Tk()
# box = Text(root, background="green")
# box.pack()
# change_color()
# root.mainloop()
