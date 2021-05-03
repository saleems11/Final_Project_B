from GUI.App.pages.display_pages import TestPage, TrainPage, HomePage
from GUI.App.sidebar import *
from GUI.App.pages.ShowResultsPage import ShowResultsPage

root = Tk()
root.resizable(False, False)
root.geometry("750x510")
main_frame = Frame(root, bg="grey", width=1000, height=1000)
main_frame.place(x=200, y=0)





sidebar = SideBar(root, 200, 1000)
sidebar.add_spacer("Al-Ghazali")
sidebar.add_button("Load Data", lambda: HomePage(main_frame))
sidebar.add_button("Train Model", lambda: TrainPage(main_frame))
sidebar.add_spacer("Other")
sidebar.add_button("Test Model", lambda: TestPage(main_frame))
sidebar.add_button("Results", lambda: ShowResultsPage(main_frame))
sidebar.finish()


root.mainloop()