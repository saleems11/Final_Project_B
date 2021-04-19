from tkinter import Button

from GUI.App.pages.page import Page, def_fg, def_bg


class ResultPage(Page):
    def __init__(self, parent):
        print("Showning test page")

        # init page/ delete old page
        Page.__init__(self, parent, title='Result')

        t = Button(self, text="Result", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)