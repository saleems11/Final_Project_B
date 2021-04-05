from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk

def Sprite(picture, res1, res2):
    im = Image.open(picture).convert("RGBA").resize((res1, res2), Image.BOX)
    pic = ImageTk.PhotoImage(im)
    cor = Image.open(picture)
    print(cor.mode)
    return pic
from ..pages.page import *

"""
defualt widget color:
#201F1E
"""
def_bg = "#201F1E"
def_fg = "lightgrey"

class HomePage(Page):
    def __init__(self, parent):
        print("Showning home page")


        # init page/ delete old page
        Page.__init__(self, parent)

        t = Label(self, text="Home", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)
        t = Button(self, text="Select the data of C1", bg=def_bg, fg=def_fg)

class TrainPage(Page):
    def __init__(self, parent):
        print("Showning settings page")


        # init page/ delete old page
        Page.__init__(self, parent)

        t = Label(self, text="Einstellungen", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)

class TestPage(Page):
    def __init__(self, parent):
        print("Showning test page")


        # init page/ delete old page
        Page.__init__(self, parent)

        t = Button(self, text="Test", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)

class ResultPage(Page):
    def __init__(self, parent):
        print("Showning test page")


        # init page/ delete old page
        Page.__init__(self, parent)

        t = Button(self, text="Result", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)