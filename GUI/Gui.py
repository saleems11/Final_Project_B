from GUI.App.pages.display_pages import TestPage, TrainPage, HomePage, Parameter
from GUI.App.sidebar import *

root = Tk()
root.resizable(False, False)
root.geometry('1200x600')
main_frame = Frame(root, bg="grey", width=1200, height=600)
main_frame.place(x=200, y=0)





sidebar = SideBar(root)
sidebar.add_spacer("Al-Ghazali")
sidebar.add_button("Load Data", lambda: HomePage(main_frame))
sidebar.add_button("Parameters", lambda: Parameter(main_frame))

sidebar.add_button("Train Model", lambda: TrainPage(main_frame))
sidebar.add_spacer("Other")
sidebar.add_button("Test Model", lambda: TestPage(main_frame))
sidebar.add_button("Results", lambda: print("KundVWebsite"))
sidebar.finish()


root.mainloop()