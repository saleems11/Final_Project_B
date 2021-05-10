from tkinter import *

active_page = []

def_fg = "lightgrey"
def_bg = "#201F1E"


class Page(Frame):
    def __init__(self, parent, title: str = 'None'):
        self.width = 1200
        self.height = 600
        # remove old page
        try:
            active_page[0].delete()
        except:
            pass

        # create new tab
        Frame.__init__(self, parent, bg="#201F1E", height=self.height, width=self.width)

        # place page
        self.place(x=0, y=0)
        self.title = Label(self, text=title, bg='white', fg='black')
        self.title.config(font=("Courier", 30))
        self.title.place(x=100, y=20)
        active_page.append(self)

    def delete(self):
        print("destroying previous tab")
        global active_page
        active_page.remove(self)
        self.destroy()