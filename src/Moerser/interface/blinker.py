from tkinter import *
from itertools import cycle


class Blinker:
    def __init__(self, sequence, timing=0.5):
        self.sequence = ["grey" for _ in range(3)] + sequence + ["red" for _ in range(1)]       # to visualize start and stop
        self.timing = int(timing * 1000)

        self.root = Tk()
        self.root.title("Mörser: Blinker")

        logo = PhotoImage(file="../assets/logo_simple_small.png")
        self.root.iconphoto(False, logo)

        self.frame = Frame(self.root, width=800, height=800,)
        self.frame.pack()
        self.color_gen = cycle(self.sequence)

        self.ChangeColor()
        self.root.mainloop()

    def ChangeColor(self):
        """
        Changes the blinking color.
        
        :return:
        """
        self.frame.config(bg=next(self.color_gen))
        self.root.after(self.timing, self.ChangeColor)


if __name__ == "__main__":
    seq = ["white", "white", "black", "white", "white", "black"]
    Blinker(seq)
