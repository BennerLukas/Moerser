from tkinter import *
from tkinter import ttk
from itertools import cycle


class Blinker:
    def __init__(self, sequence, timing=1000):
        self.sequence = ["grey" for _ in range(3)] + sequence + ["red" for _ in range(3)]       # to visualize start and stop
        self.timing = timing

        self.root = Tk()
        self.root.title("Mörser: Blinker")

        logo = PhotoImage(file="../assets/logo_simple_small.png")
        self.root.iconphoto(False, logo)

        self.frame = Frame(self.root, width=260, height=200)
        self.frame.pack()
        self.color_gen = cycle(self.sequence)

        self.ChangeColor()
        self.root.mainloop()

    def ChangeColor(self):
        self.frame.config(bg=next(self.color_gen))
        self.root.after(1000, self.ChangeColor)


if __name__ == "__main__":
    seq = ["white", "white", "black", "white", "white", "black"]
    Blinker(seq)
