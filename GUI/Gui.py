from GUI.App.pages.display_pages import TestPage, TrainPage, HomePage
from GUI.App.sidebar import *
from GUI.App.pages.ShowResultsPage import ShowResultsPage

root = Tk()
root.resizable(False, False)
width = 750
height = 510
side_bar_width = 200
root.geometry("%dx%d" % (width, height))
main_frame = Frame(root, bg="grey", width=width*side_bar_width, height=height)
main_frame.place(x=0+side_bar_width, y=0)


# they will be updated after running the model and getting the results
M = None
iteration_size = None
testing_data = None
testing_books_names = None

sidebar = SideBar(root, 200, 1000)
sidebar.add_spacer("Al-Ghazali")
sidebar.add_button("Load Data", lambda: HomePage(main_frame))
sidebar.add_button("Train Model", lambda: TrainPage(main_frame))
sidebar.add_spacer("Other")
sidebar.add_button("Test Model", lambda: TestPage(main_frame))
sidebar.add_button("Results", lambda: ShowResultsPage(main_frame))
sidebar.finish()


root.mainloop()