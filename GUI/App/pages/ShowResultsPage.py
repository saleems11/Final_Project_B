from tkinter import Frame
from GUI.App.pages.Pages_parameters import Pages_parameters
from GUI.App.pages.page import Page
from tkinter import Button

from Show_results.Heat_map import Heat_map
from Show_results.Error_bar import Error_bar

# import GUI.Gui as Gui

import threading
import tkinter as tk


class ShowResultsPage(Page):
    def __init__(self, parent_frame):
        # init page/ delete old page
        Page.__init__(self, parent_frame)

        self.pages_types = ['heat_map', 'error_bar', 'chunks_labels', 'histogram']
        self.current_page = 'heat_map'

        # split the GUi to three parts vertically
        self.top_frame = Frame(parent_frame)
        self.top_frame.grid(row=0, column=0, sticky="nswe")

        self.mid_frame = Frame(parent_frame)
        self.mid_frame.grid(row=1, column=0, sticky="nswe")

        self.bottom_frame = Frame(parent_frame)
        self.bottom_frame.grid(row=2, column=0, sticky="nswe")

        # objects contain data
        self.error_bar = None
        self.heat_map = None
        self.chunk_labels = None

        # variables and lists for GUI
        """ The final code replace the next line bellow the bellow line"""
        # Gui.testing_books_names
        self.testing_books_names = ["Jan", "Feb", "Mar", "Very long name and Very long  bame"]  # etc


        # add GUI parts

        # top frame parameters init
        self.top_frame_prev_pressed_Btn = None
        self.heat_map_show_Btn = None
        self.error_bar_show_Btn = None
        self.chunks_labels_show_Btn = None
        self.histogram_show_Btn = None

        self.init_top_frame()
        self.clicked_on_heat_map_show_Btn()

        # bottom frame parameters init
        self.finish_Btn = None
        self.init_bottom_frame()

    ''' Initializing the Main frame sections'''

    def init_top_frame(self):
        self.heat_map_show_Btn = \
            Button(self.top_frame, text="Heat Map", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_heat_map_show_Btn)
        self.error_bar_show_Btn = \
            Button(self.top_frame, text="Error Bar", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_error_bar_show_Btn)
        self.chunks_labels_show_Btn = \
            Button(self.top_frame, text="Chunks Labels", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_chunks_labels_show_Btn)
        self.histogram_show_Btn = \
            Button(self.top_frame, text="Histogram", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_histogram_show_Btn)

        self.heat_map_show_Btn.grid(row=0, column=0, padx=10, pady=10)
        self.error_bar_show_Btn.grid(row=0, column=1, padx=10, pady=10)
        self.chunks_labels_show_Btn.grid(row=0, column=2, padx=10, pady=10)
        self.histogram_show_Btn.grid(row=0, column=3, padx=10, pady=10)

    def init_bottom_frame(self):
        self.finish_Btn = \
            Button(self.bottom_frame, text="Finish", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_finish_Btn)
        self.finish_Btn.pack(padx=10, pady=10, side=tk.RIGHT)

    ''' Click management '''

    def clicked_on_heat_map_show_Btn(self):
        self.switch_top_frame_clicked_button(self.heat_map_show_Btn)
        self.create_heat_map_frame()

    def clicked_on_error_bar_show_Btn(self):
        self.switch_top_frame_clicked_button(self.error_bar_show_Btn)
        self.create_error_bar_frame()
        pass

    def clicked_on_chunks_labels_show_Btn(self):
        self.switch_top_frame_clicked_button(self.chunks_labels_show_Btn)
        self.create_chunk_labels_frame()
        pass

    def clicked_on_histogram_show_Btn(self):
        self.switch_top_frame_clicked_button(self.histogram_show_Btn)
        pass

    def clicked_on_finish_Btn(self):
        print("Still not Implemented")
        self.reset_variables()
        pass

    """ Logic's Handling and input data checking """

    def check_chunks_labels_inputs(self):
        print("Un-implemented")
        pass

    def switch_top_frame_clicked_button(self, cur_button):
        # reset the prev button

        if self.top_frame_prev_pressed_Btn != None:
            # reset
            self.top_frame_prev_pressed_Btn["state"] = tk.NORMAL

        cur_button["state"] = tk.DISABLED
        self.top_frame_prev_pressed_Btn = cur_button

    """ creating Sub-frames"""

    def create_heat_map_frame(self):
        if self.heat_map is None:
            """ for testing purposes"""
            self.heat_map = Heat_map(None, None, testing=True)
            """ The final code point to the global parameters """
            # self.heat_map = Heat_map(data=Gui.M, iteration_size=Gui.iteration_size)

        Heat_map.create_GUI(result_obj=self.heat_map, main_frame=self.mid_frame)

    def create_error_bar_frame(self):

        if self.error_bar is None:
            """ For testing """
            self.error_bar = Error_bar(x=None,
                                       y=None,
                                       y_mean=None,
                                       y_mean_c1=None,
                                       y_mean_c2=None,
                                       label=None,
                                       asymmetric_y_error=None,
                                       testing=True)
            """ The Finale Code"""
            # get the data using a thread
            # threading.Thread(target=ShowResultsPage.get_error_bar_data_and_show, args=self.error_bar)

        self.error_bar.create_GUI(result_obj=self.error_bar, main_frame=self.mid_frame)


    def create_chunk_labels_frame(self):
        self.chunk_labels_frame_top_frame = Frame(self.mid_frame)
        self.chunk_labels_frame_top_frame.grid(row=0, column=0, sticky="nswe")

        self.bottom_frame = Frame(self.mid_frame)
        self.bottom_frame.grid(row=1, column=0, sticky="nswe")

        # add GUI parts to the top frame
        # select the book
        self.select_book_chunk_labels_label = \
            tk.Label(self.chunk_labels_frame_top_frame, text="Select Book", fg=Pages_parameters.black)

        variable = tk.StringVar()
        variable.set(self.testing_books_names[0])  # default value
        self.books_selecting_list_option = tk.OptionMenu(self.chunk_labels_frame_top_frame, variable,
                                                         *self.testing_books_names)
        self.books_selecting_list_option.config(width=20)

        # select the starting idx
        self.select_book_chunk_staring_idx_label = \
            tk.Label(self.chunk_labels_frame_top_frame, text="Starting index", fg=Pages_parameters.black)

        self.select_book_chunk_staring_idx_entry = tk.Entry(self.chunk_labels_frame_top_frame, width=10)

        # select the end idx
        self.select_book_chunk_ending_idx_label = \
            tk.Label(self.chunk_labels_frame_top_frame, text="Final index", fg=Pages_parameters.black)

        self.select_book_chunk_ending_idx_entry = tk.Entry(self.chunk_labels_frame_top_frame, width=10)

        self.load_book_chunks_frequency_graph = tk.Button(self.chunk_labels_frame_top_frame, text="Chunks Labels",
                                                          bg=Pages_parameters.def_bg, fg=Pages_parameters.def_fg,
                                                          command=self.check_chunks_labels_inputs)


        # set the GUI parts
        x_padding = 5
        self.select_book_chunk_labels_label.grid(row=0, column=0, padx=x_padding, pady=10, sticky="W")
        self.books_selecting_list_option.grid(row=0, column=1, padx=x_padding, pady=10, columnspan=2)
        self.select_book_chunk_staring_idx_label.grid(row=1, column=0, padx=x_padding, pady=10, sticky="W")
        self.select_book_chunk_staring_idx_entry.grid(row=1, column=1, padx=x_padding, pady=10)
        self.select_book_chunk_ending_idx_label.grid(row=1, column=2, padx=x_padding, pady=10)
        self.select_book_chunk_ending_idx_entry.grid(row=1, column=3, padx=x_padding, pady=10)
        self.load_book_chunks_frequency_graph.grid(row=1, column=4, padx=x_padding*2, pady=10)


    """ Threads Functions """

    @staticmethod
    def get_error_bar_data_and_show(error_bar):
        books_names, books_mean_values_over_all_iter, books_error_down_values_over_all_iter, \
        books_error_up_values_over_all_iter, books_mean_values_over_all_iter, c1_mean_val, c2_mean_val, mean_val \
            = Gui.testing_data.get_error_bar_data()

        error_bar = Error_bar(x=books_names,
                              y=books_mean_values_over_all_iter,
                              y_mean=mean_val,
                              y_mean_c1=c1_mean_val,
                              y_mean_c2=c2_mean_val,
                              label="Books Error Bar",
                              asymmetric_y_error=[books_error_down_values_over_all_iter,
                                                  books_error_up_values_over_all_iter])

    """ Resest """

    def reset_variables(self):
        self.heat_map = None
        self.error_bar = None

        pass
