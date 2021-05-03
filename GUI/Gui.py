from threading import Thread
from time import sleep
from tkinter import messagebox

from GUI.App.pages.LoadData import HomePage
from GUI.App.pages.Parameters import Parameter
from GUI.App.pages.Result import ResultPage
from GUI.App.pages.Train import TrainPage
from GUI.App.sidebar import *
thread_list: List[Thread] = []

def join_threats(list_of_threads: List[Thread]):
    for thread in list_of_threads:
        if not thread.is_alive():
            thread.join()
    sleep(1)
root = Tk()
root.resizable(False, False)
root.geometry('1200x600')
main_frame = Frame(root, bg="grey", width=1200, height=600)
main_frame.place(x=0, y=0)
home_page = HomePage(main_frame, root)
# sidebar = SideBar(root)
# sidebar.add_spacer("Al-Ghazali")
# sidebar.add_button("Load Data", lambda: HomePage(main_frame))
# sidebar.add_button("Parameters", lambda: Parameter(main_frame))
#
# sidebar.add_button("Train Model", lambda: TrainPage(main_frame))
# sidebar.add_spacer("Other")
# sidebar.add_button("Results", lambda:  ResultPage(main_frame))
# sidebar.finish()
def doSomething():
    if messagebox.askokcancel("myapp", "Do you want to quit?"):
        root.destroy()

    sys.exit()
root.protocol('WM_DELETE_WINDOW', doSomething)  # root is your root window


root.update()
root.mainloop()
