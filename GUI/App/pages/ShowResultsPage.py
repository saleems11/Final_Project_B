from tkinter import Frame
from GUI.App.pages.Pages_parameters import Pages_parameters
from GUI.App.pages.page import Page
from tkinter import Button

from Show_results.Heat_map import Heat_map
from Show_results.Error_bar import Error_bar
from Show_results.Book_chunks_labels import Book_chunks_labels
from Show_results.Histograms import Histograms

# import GUI.Gui as Gui

import threading
import tkinter as tk


class ShowResultsPage(Page):
    def __init__(self, parent_frame):
        # init page/ delete old page
        Page.__init__(self, parent_frame)

        self.parent_frame = parent_frame

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
        self.histogram = None
        self.chunk_labels = None

        # variables and lists for GUI
        """ The final code replace the next line bellow the bellow line"""
        # Gui.testing_books_names
        self.testing_books_names = ["Jan", "Feb", "Mar", "Very long name and Very long  bame"]  # etc
        self.select_book_chunk_staring_idx_value = None
        self.select_book_chunk_ending_idx_value = None
        self.smooth_frequency_graph_check_box_val = tk.IntVar()
        self.over_iterations_chunks_labels_check_box_val = tk.IntVar()
        self.prev_selected_book_name_chunks_labels = None
        self.prev_selected_book_name_histogram = None

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

    def clicked_on_load_book_chunks_frequency_graph(self):
        if self.check_chunks_labels_inputs():
            book_name = self.chunk_labels_book_names_opt.get()
            self.select_book_chunk_staring_idx_value = int(self.select_book_chunk_staring_idx_entry.get())
            self.prev_selected_book_name_chunks_labels = book_name

            smoothing_option = self.smooth_frequency_graph_check_box_val.get()
            average_over_iter_option = self.over_iterations_chunks_labels_check_box_val.get()

            """ Just for testing """
            self.chunk_labels = Book_chunks_labels(
                None,
                book_name=None,
                rounded=smoothing_option,
                average_over_iter=average_over_iter_option,
                testing=True)

            if self.select_book_chunk_ending_idx_entry.get() != '':
                self.select_book_chunk_ending_idx_value = int(self.select_book_chunk_ending_idx_entry.get())

                # check if the ending_idx smaller than book size
                data_size = len(self.chunk_labels.y_data)
                if data_size <= self.select_book_chunk_ending_idx_value:
                    tk.messagebox.showinfo("Input miss mach", "Please input valid number smaller than data size"
                                                              "(ending index is bigger than data size: %d )" % data_size)
                    return

                self.chunk_labels.y_data = self.chunk_labels.y_data[self.select_book_chunk_staring_idx_value:
                                                                    self.select_book_chunk_ending_idx_value]
            else:
                self.chunk_labels.y_data = self.chunk_labels.y_data[self.select_book_chunk_staring_idx_value:]

            # the finale code
            # book = Gui.testing_data.get_book(book_name=book_name)

            # check if the ending_idx smaller than book size
            # if self.select_book_chunk_ending_idx_entry.get() != '':
            #     data_size = len(book.predictions_res_over_iter[-1])
            #     if data_size <= select_book_chunk_ending_idx_value:
            #         tk.messagebox.showinfo("Input miss mach", "Please input valid number smaller than data size"
            #                                                   "(ending index is bigger than data size: %d )" % data_size)
            #         return

                # here must know if average_over_iter_option is used
                # to know witch data to give to the GUI creator

                # self.chunk_labels = Book_chunks_labels(
                #     book.predictions_res_over_iter[-1][self.select_book_chunk_staring_idx_value:
                #     select_book_chunk_ending_idx_value],
                #     book_name=book.book_name,
                #     rounded= smoothing_option,
                #     average_over_iter= average_over_iter_option)
                # look at the hint above
            # else:
            # self.chunk_labels = Book_chunks_labels(
            #     book.predictions_res_over_iter[-1][self.select_book_chunk_staring_idx_value:],
            #     book_name=book.book_name,
            #     rounded= smoothing_option,
            #     average_over_iter= average_over_iter_option)

            Book_chunks_labels.create_GUI(result_obj=self.chunk_labels, main_frame=self.chunk_labels_frame_bottom_frame)

    """ Logic's Handling and input data checking """

    def check_chunks_labels_inputs(self):
        all_rest_of_data_index = True

        if self.select_book_chunk_staring_idx_entry.get() == '':
            tk.messagebox.showinfo("Input miss mach", "Please fill starting index")
            return False

        try:
            staring_idx = int(self.select_book_chunk_staring_idx_entry.get())
            if self.select_book_chunk_ending_idx_entry.get() != '':
                ending_idx = int(self.select_book_chunk_ending_idx_entry.get()) + 1
                all_rest_of_data_index = False
        except Exception:
            tk.messagebox.showinfo("Input miss mach", "Please input valid number(Integer)")
            return False



        if staring_idx < 0:
            tk.messagebox.showinfo("Input miss mach", "Please input valid number(Positive or Zero) for starting index")
            return False

        if not all_rest_of_data_index:
            if ending_idx < 0:
                tk.messagebox.showinfo("Input miss mach", "Please input valid number(Positive) for Final index")
                return False
            if staring_idx > ending_idx - 10 + 1:
                tk.messagebox.showinfo("Input miss mach",
                                       "Please set the Starting index smaller that Final by 10 at least")
                return False

        return True

    def switch_top_frame_clicked_button(self, cur_button):
        # reset the prev button

        if self.top_frame_prev_pressed_Btn != None:
            # reset
            self.top_frame_prev_pressed_Btn["state"] = tk.NORMAL

        cur_button["state"] = tk.DISABLED
        self.top_frame_prev_pressed_Btn = cur_button

        # reset mid frame
        self.mid_frame = Frame(self.parent_frame)
        self.mid_frame.grid(row=1, column=0, sticky="nswe")

    """ creating Sub-frames"""

    def create_chunk_labels_graph_frame(self):
        pass

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
            self.error_bar.create_GUI(result_obj=self.error_bar, main_frame=self.mid_frame)
            """ The Finale Code"""
            # get the data using a thread
            # threading.Thread(target=self.get_error_bar_data_and_show)
        else:
            self.error_bar.create_GUI(result_obj=self.error_bar, main_frame=self.mid_frame)


    def create_chunk_labels_frame(self):
        self.chunk_labels_frame_top_frame = Frame(self.mid_frame)
        self.chunk_labels_frame_top_frame.grid(row=0, column=0, sticky="nswe")

        self.chunk_labels_frame_bottom_frame = Frame(self.mid_frame)
        self.chunk_labels_frame_bottom_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)

        # add GUI parts to the top frame
        # select the book
        self.select_book_chunk_labels_label = \
            tk.Label(self.chunk_labels_frame_top_frame, text="Select Book", fg=Pages_parameters.black)

        self.chunk_labels_book_names_opt = tk.StringVar()
        # load the last val of the prev run
        if self.prev_selected_book_name_chunks_labels != None:
            self.chunk_labels_book_names_opt.set(self.prev_selected_book_name_chunks_labels)
        else:
            self.chunk_labels_book_names_opt.set(self.testing_books_names[0])  # default value
        self.chunk_labels_books_selecting_list_option = tk.OptionMenu(self.chunk_labels_frame_top_frame,
                                                         self.chunk_labels_book_names_opt,
                                                         *self.testing_books_names)
        self.chunk_labels_books_selecting_list_option.config(width=40)

        # select the starting idx
        self.chunk_labels_select_book_chunk_staring_idx_label = \
            tk.Label(self.chunk_labels_frame_top_frame, text="Starting index", fg=Pages_parameters.black)

        self.select_book_chunk_staring_idx_entry = tk.Entry(self.chunk_labels_frame_top_frame, width=10)
        # load the values of prev run
        if self.select_book_chunk_staring_idx_value != None:
            self.select_book_chunk_staring_idx_entry.delete(0, tk.END)
            self.select_book_chunk_staring_idx_entry.insert(0, str(self.select_book_chunk_staring_idx_value))
        else:
            self.select_book_chunk_staring_idx_entry.insert(0, '0')

        # select the end idx
        self.select_book_chunk_ending_idx_label = \
            tk.Label(self.chunk_labels_frame_top_frame, text="Final index", fg=Pages_parameters.black)

        self.select_book_chunk_ending_idx_entry = tk.Entry(self.chunk_labels_frame_top_frame, width=10)
        # load the values of prev run
        if self.select_book_chunk_ending_idx_value != None:
            self.select_book_chunk_ending_idx_entry.delete(0, tk.END)
            self.select_book_chunk_ending_idx_entry.insert(0, str(self.select_book_chunk_ending_idx_value))

        # smoothing check box
        self.smooth_frequency_graph_check_box = tk.Checkbutton(self.chunk_labels_frame_top_frame, text="Smooth Graph",
                                                               variable=self.smooth_frequency_graph_check_box_val)
        # average data check box
        self.over_iterations_chunks_labels_check_box = tk.Checkbutton(self.chunk_labels_frame_top_frame,
                                                                      text="Average over iterations",
                                                                      variable=self.over_iterations_chunks_labels_check_box_val)

        self.load_book_chunks_frequency_graph_Btn = tk.Button(self.chunk_labels_frame_top_frame, text="Chunks Labels",
                                                              bg=Pages_parameters.def_bg, fg=Pages_parameters.def_fg,
                                                              command=self.clicked_on_load_book_chunks_frequency_graph)

        # set the GUI parts
        x_padding = 5
        self.select_book_chunk_labels_label.grid(row=0, column=0, padx=x_padding, pady=10, sticky="W")
        self.chunk_labels_books_selecting_list_option.grid(row=0, column=1, padx=x_padding, pady=10, columnspan=3)

        self.chunk_labels_select_book_chunk_staring_idx_label.grid(row=1, column=0, padx=x_padding, pady=10, sticky="W")
        self.select_book_chunk_staring_idx_entry.grid(row=1, column=1, padx=x_padding, pady=10)
        self.select_book_chunk_ending_idx_label.grid(row=1, column=2, padx=x_padding, pady=10)
        self.select_book_chunk_ending_idx_entry.grid(row=1, column=3, padx=x_padding, pady=10)
        self.load_book_chunks_frequency_graph_Btn.grid(row=1, column=4, padx=x_padding * 2, pady=10)

        self.smooth_frequency_graph_check_box.grid(row=2, column=0, padx=x_padding, pady=10)
        self.over_iterations_chunks_labels_check_box.grid(row=2, column=1, padx=x_padding, pady=10)


    def create_histograms_frame(self):
        self.histogram_frame_top_frame = Frame(self.mid_frame)
        self.histogram_frame_top_frame.grid(row=0, column=0, sticky="nswe")

        self.histogram_frame_bottom_frame = Frame(self.mid_frame)
        self.histogram_frame_bottom_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)

        # add GUI parts to the top frame
        """ Select the book """
        self.select_book_histogram_label = \
            tk.Label(self.histogram_frame_top_frame, text="Select Book", fg=Pages_parameters.black)

        self.histogram_book_names_opt = tk.StringVar()
        # load the last val of the prev run
        if self.prev_selected_book_name_histogram != None:
            self.histogram_book_names_opt.set(self.prev_selected_book_name_histogram)
        else:
            self.histogram_book_names_opt.set(self.testing_books_names[0])  # default value
        self.histogram_books_selecting_list_option = tk.OptionMenu(self.histogram_frame_top_frame,
                                                         self.histogram_book_names_opt,
                                                         *self.testing_books_names)
        self.histogram_books_selecting_list_option.config(width=40)


        """  Select the starting idx"""
        self.histogram_select_book_chunk_staring_idx_label = \
            tk.Label(self.histogram_frame_top_frame, text="Starting index", fg=Pages_parameters.black)

        self.select_book_chunk_staring_idx_entry = tk.Entry(self.histogram_frame_top_frame, width=10)
        # load the values of prev run
        if self.select_book_chunk_staring_idx_value != None:
            self.select_book_chunk_staring_idx_entry.delete(0, tk.END)
            self.select_book_chunk_staring_idx_entry.insert(0, str(self.select_book_chunk_staring_idx_value))
        else:
            self.select_book_chunk_staring_idx_entry.insert(0, '0')

        """ Select the end idx """
        self.select_book_chunk_ending_idx_label = \
            tk.Label(self.histogram_frame_top_frame, text="Final index", fg=Pages_parameters.black)

        self.select_book_chunk_ending_idx_entry = tk.Entry(self.histogram_frame_top_frame, width=10)
        # load the values of prev run
        if self.select_book_chunk_ending_idx_value != None:
            self.select_book_chunk_ending_idx_entry.delete(0, tk.END)
            self.select_book_chunk_ending_idx_entry.insert(0, str(self.select_book_chunk_ending_idx_value))

        # smoothing check box
        self.smooth_frequency_graph_check_box = tk.Checkbutton(self.histogram_frame_top_frame, text="Smooth Graph",
                                                               variable=self.smooth_frequency_graph_check_box_val)
        # average data check box
        self.over_iterations_chunks_labels_check_box = tk.Checkbutton(self.histogram_frame_top_frame,
                                                                      text="Average over iterations",
                                                                      variable=self.over_iterations_chunks_labels_check_box_val)

        self.load_book_chunks_frequency_graph_Btn = tk.Button(self.histogram_frame_top_frame, text="Chunks Labels",
                                                              bg=Pages_parameters.def_bg, fg=Pages_parameters.def_fg,
                                                              command=self.clicked_on_load_book_chunks_frequency_graph)

        # set the GUI parts
        x_padding = 5
        self.select_book_chunk_labels_label.grid(row=0, column=0, padx=x_padding, pady=10, sticky="W")
        self.histogram_books_selecting_list_option.grid(row=0, column=1, padx=x_padding, pady=10, columnspan=3)

        self.histogram_select_book_chunk_staring_idx_label.grid(row=1, column=0, padx=x_padding, pady=10, sticky="W")
        self.select_book_chunk_staring_idx_entry.grid(row=1, column=1, padx=x_padding, pady=10)
        self.select_book_chunk_ending_idx_label.grid(row=1, column=2, padx=x_padding, pady=10)
        self.select_book_chunk_ending_idx_entry.grid(row=1, column=3, padx=x_padding, pady=10)
        self.load_book_chunks_frequency_graph_Btn.grid(row=1, column=4, padx=x_padding * 2, pady=10)

        self.smooth_frequency_graph_check_box.grid(row=2, column=0, padx=x_padding, pady=10)
        self.over_iterations_chunks_labels_check_box.grid(row=2, column=1, padx=x_padding, pady=10)






    """ Threads Functions """

    def get_error_bar_data_and_show(self, error_bar):
        books_names, books_mean_values_over_all_iter, books_error_down_values_over_all_iter, \
        books_error_up_values_over_all_iter, books_mean_values_over_all_iter, c1_mean_val, c2_mean_val, mean_val \
            = Gui.testing_data.get_error_bar_data()

        self.error_bar = Error_bar(x=books_names,
                                   y=books_mean_values_over_all_iter,
                                   y_mean=mean_val,
                                   y_mean_c1=c1_mean_val,
                                   y_mean_c2=c2_mean_val,
                                   label="Books Error Bar",
                                   asymmetric_y_error=[books_error_down_values_over_all_iter,
                                                       books_error_up_values_over_all_iter])

        Error_bar.create_GUI(result_obj=self.error_bar, main_frame=self.mid_frame)

    """ Resest """

    def reset_variables(self):
        self.heat_map = None
        self.error_bar = None
        self.chunk_labels = None
        self.histogram = None

        pass
