from GUI.App.pages.display_pages import TestPage, TrainPage, HomePage
from GUI.App.sidebar import *
from Show_results.Heat_map import Heat_map
# test for pyplot

root = Tk()
root.resizable(False, False)
width = 1920
height = 1080
side_bar_width = 200
root.geometry("%dx%d" % (width, height))
main_frame = Frame(root, bg="grey", width=width-side_bar_width, height=height)
main_frame.place(x=side_bar_width, y=0)



M, iteration_size = Heat_map._generate_sample_data()
Heat_map.create_GUI(root=main_frame, data=Heat_map.convert_M_to_heat_map(M, iteration_size))

sidebar = SideBar(root, side_bar_width, height)



sidebar.add_spacer("Al-Ghazali")
sidebar.add_button("Load Data", lambda: HomePage(main_frame))
sidebar.add_button("Train Model", lambda: TrainPage(main_frame))
sidebar.add_spacer("Other")
sidebar.add_button("Test Model", lambda: TestPage(main_frame))
sidebar.add_button("Results", lambda: print("KundVWebsite"))
# sidebar.finish()


root.mainloop()