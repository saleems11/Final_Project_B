import sys
from tkinter import messagebox, Tk, Frame

from GUI.App.pages.LoadData import HomePage



# init the window
root = Tk()
root.resizable(False, False)
root.geometry('1200x600')
main_frame = Frame(root, bg="white", width=1200, height=600)
main_frame.place(x=0, y=0)
HomePage(main_frame, root=root, testing=False)

def new_exit():
    if messagebox.askokcancel("Warning", "Do you want to quit?"):
        sys.exit()


root.protocol('WM_DELETE_WINDOW', new_exit)  # root is your root window


root.update()
root.mainloop()
