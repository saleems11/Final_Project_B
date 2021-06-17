from GUI.App.pages.Pages_parameters import Pages_parameters
from GUI.App.pages.page import Page

from Show_results.Heat_map import Heat_map
from Show_results.Error_bar import Error_bar
from Show_results.Book_chunks_labels import Book_chunks_labels
from Show_results.Histograms import Histograms

from Objects.Book import Book

import sys

from tkinter import messagebox, Frame, Button
import tkinter as tk
import tkinter.scrolledtext as st


class ShowResultsPage(Page):
    """ A Class used as GUI and controller for the part of showing the result of the model after training
    and testing the model."""
    def __init__(self, parent_frame, M, testing_data):
        """ initialize the object with M which contains the mean prediction result of each book over many iterations
        testing data, is the object responsible for handeling many kinds of the prediction result"""
        # init page/ delete old page
        Page.__init__(self, parent_frame)

        self.parent_frame = parent_frame
        self.M = M
        self.testing_data = testing_data
        # self.book_names_in_order_of_M = book_names_in_order_of_M

        # split the GUi to three parts vertically
        self.top_frame = Frame(parent_frame)
        self.top_frame.grid(row=0, column=0, sticky="nswe")

        self.mid_frame = Frame(parent_frame)
        self.mid_frame.grid(row=1, column=0, sticky="nswe", columnspan=2)

        self.bottom_frame = Frame(parent_frame)
        self.bottom_frame.grid(row=2, column=0, sticky="nswe")
        self.bottom_frame.grid_rowconfigure(0, weight=2)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_propagate(0)

        # objects contain data for each type of data representations
        self.error_bar = None
        self.heat_map = None
        self.chunk_labels = None
        self.histogram = None

        # variables and lists for GUI
        self.testing_books_names = testing_data.c3_books_names
        self.chunks_labels_selected_book_chunk_staring_idx_value = None
        self.chunks_labels_selected_book_chunk_ending_idx_value = None

        self.histogram_selected_book_chunk_staring_idx_value = None
        self.histogram_selected_book_chunk_ending_idx_value = None

        self.chunks_labels_smooth_frequency_graph_check_box_val = tk.IntVar()
        self.chunks_labels_round_frequency_graph_check_box_val = tk.IntVar()
        self.chunks_labels_over_iterations_check_box_val = tk.IntVar()

        self.histogram_smooth_frequency_graph_check_box_val = tk.IntVar()
        self.histogram_over_iterations_chunks_labels_check_box_val = tk.IntVar()

        self.prev_selected_book_name_chunks_labels = None
        self.prev_selected_book_name_histogram = None

        # books chunks labels sub frames
        self.chunk_labels_frame_top_frame = None
        self.chunk_labels_frame_bottom_frame = None

        # histogram sub frames
        self.histogram_frame_top_frame = None
        self.histogram_frame_bottom_frame = None

        # add GUI parts

        # top frame parameters init
        """ The buttons available in the top frame """
        self.top_frame_prev_pressed_Btn = None
        self.heat_map_show_Btn = None
        self.error_bar_show_Btn = None
        self.chunks_labels_show_Btn = None
        self.histogram_show_Btn = None

        self.return_Btn = None

        self.init_top_frame()
        """ The default page """
        self.clicked_on_heat_map_show_Btn()


    ''' Initializing the Main frame sections'''

    def init_top_frame(self):
        """ create frame parts  and connect the elements to the event handlers and then place them
        The top frame is the one responsible for switching between frames"""
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
        self.return_Btn = \
            Button(self.top_frame, text="Return", bg=Pages_parameters.red,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_finish_Btn)

        self.heat_map_show_Btn.grid(row=0, column=0, padx=10, pady=10)
        self.error_bar_show_Btn.grid(row=0, column=1, padx=10, pady=10)
        self.chunks_labels_show_Btn.grid(row=0, column=2, padx=10, pady=10)
        self.histogram_show_Btn.grid(row=0, column=3, padx=10, pady=10)
        self.return_Btn.grid(row=0, column=4, padx=30, pady=10)

    def init_bottom_frame(self, books_names=None):
        """ set book names to index, the code handel two version of indexing books names
        One of them is according to M, and the other according to the order of inserted books"""
        scrolling_text = ""

        # if books_names is None:
        #     books_names = self.book_names_in_order_of_M

        # get book details as string
        for idx, book_name in enumerate(books_names):
            book_cluster = self.testing_data.get_book_cluster(book_name=book_name)
            txt = Book.get_book_details_as_string(book_name=book_name, index=idx, cluster=book_cluster)
            if idx == 0:
                scrolling_text = scrolling_text + txt
            else:
                scrolling_text = scrolling_text + '\n' + txt

        # each line will book name and the index and the cluster of each book
        self.text_area = st.ScrolledText(self.bottom_frame, height=4)

        self.text_area.insert(tk.INSERT, scrolling_text)
        # Making the text read only
        self.text_area.configure(state='disabled')

        self.text_area.grid(column=0, pady=25, padx=10, rowspan=3, sticky='nsew')

    ''' Click management '''

    def clicked_on_heat_map_show_Btn(self):
        self.switch_top_frame_clicked_button(self.heat_map_show_Btn)
        self.create_heat_map_frame()

    def clicked_on_error_bar_show_Btn(self):
        self.switch_top_frame_clicked_button(self.error_bar_show_Btn)
        self.create_error_bar_frame()

    def clicked_on_chunks_labels_show_Btn(self):
        self.switch_top_frame_clicked_button(self.chunks_labels_show_Btn)
        self.create_chunk_labels_frame()


    def clicked_on_histogram_show_Btn(self):
        self.switch_top_frame_clicked_button(self.histogram_show_Btn)
        self.create_histograms_frame()

    def clicked_on_finish_Btn(self):
        print("Still not Implemented")
        self.reset_variables()
        if messagebox.askokcancel("Warning", "Do you want to go back to the load data page?"):
            from GUI.App.pages.LoadData import HomePage
            HomePage(self.parent_frame, root=None)


    def clicked_on_load_book_chunks_frequency_graph(self):
        """ Handel the click for loading book frequency graph """

        # check is all the inputs are correct
        if self.check_book_and_chunks_selecting_inputs():
            book_name = self.chunk_labels_book_names_opt.get()
            self.chunks_labels_selected_book_chunk_staring_idx_value = int(
                self.select_book_chunk_staring_idx_entry.get())
            self.prev_selected_book_name_chunks_labels = book_name

            # get  check box options
            smoothing_option = self.chunks_labels_smooth_frequency_graph_check_box_val.get()
            rounding_option = self.chunks_labels_round_frequency_graph_check_box_val.get()
            average_over_iter_option = self.chunks_labels_over_iterations_check_box_val.get()

            # get the Book object that contain the  wanted data
            book = self.testing_data.get_book(book_name=book_name)

            # for making better GUI the user doesn't have to enter the last index of the data
            # so when he leave it empty it automatically says that he want all the from staring index to the end
            #  here is the check if the user  left it empty
            if self.select_book_chunk_ending_idx_entry.get() != '':
                data_size = book.embedded_data.shape[0]
                # check if the ending_idx smaller than book size
                self.chunks_labels_selected_book_chunk_ending_idx_value = int(
                    self.select_book_chunk_ending_idx_entry.get())
                if data_size <= self.chunks_labels_selected_book_chunk_ending_idx_value:
                    tk.messagebox.showinfo("Input miss mach", "Please input valid number smaller than data size"
                                                              "(ending index is bigger than data size: %d )" % data_size)
                    return

                """ from starting index to finish index"""
                #  load different data according to the user options
                if average_over_iter_option:
                    """ Take the result of the mean average data over iterations """
                    mean_over_iterations = book.mean_prediction_over_iteration()
                    self.chunk_labels = Book_chunks_labels(
                        mean_over_iterations[
                        self.chunks_labels_selected_book_chunk_staring_idx_value:
                        self.chunks_labels_selected_book_chunk_ending_idx_value],
                        book_name=book.book_name,
                        rounded=rounding_option,
                        smoothed=smoothing_option)
                else:
                    """ Take the result of the average data over iterations """
                    self.chunk_labels = Book_chunks_labels(
                        book.predictions_res_over_iter[-1][
                        self.chunks_labels_selected_book_chunk_staring_idx_value:
                        self.chunks_labels_selected_book_chunk_ending_idx_value],
                        book_name=book.book_name,
                        rounded=rounding_option,
                        smoothed=smoothing_option)
            # The user choose ending index
            else:
                """ from starting index to finish """
                if average_over_iter_option:
                    """ Take the result of the mean average data over iterations """
                    mean_over_iterations = book.mean_prediction_over_iteration()
                    self.chunk_labels = Book_chunks_labels(
                        mean_over_iterations[
                        self.chunks_labels_selected_book_chunk_staring_idx_value:],
                        book_name=book.book_name,
                        rounded=rounding_option,
                        smoothed=smoothing_option)
                else:
                    """ Take the result of the average data over iterations """
                    self.chunk_labels = Book_chunks_labels(
                        book.predictions_res_over_iter[-1][self.chunks_labels_selected_book_chunk_staring_idx_value:],
                        book_name=book.book_name,
                        rounded=rounding_option,
                        smoothed=smoothing_option)
            """ Pre built function that build selecting the option for book frequency graph and Histogram"""
            Book_chunks_labels.create_GUI(result_obj=self.chunk_labels, main_frame=self.chunk_labels_frame_bottom_frame)

    def clicked_on_load_books_histogram_graph(self):
        """ Handel the click for loading book Histogram """

        # check is all the inputs are correct
        if self.check_book_and_chunks_selecting_inputs():
            book_name = self.histogram_book_names_opt.get()
            self.histogram_selected_book_chunk_staring_idx_value = int(
                self.select_book_chunk_staring_idx_entry.get())
            self.prev_selected_book_name_histogram = book_name

            # get  check box options
            smoothing_option = self.histogram_smooth_frequency_graph_check_box_val.get()
            average_over_iter_option = self.histogram_over_iterations_chunks_labels_check_box_val.get()

            # get the Book object that contain the  wanted data
            book = self.testing_data.get_book(book_name=book_name)


            # for making better GUI the user doesn't have to enter the last index of the data
            # so when he leave it empty it automatically says that he want all the from staring index to the end
            #  here is the check if the user  left it empty
            if self.select_book_chunk_ending_idx_entry.get() != '':
                data_size = book.embedded_data.shape[0]
                # check if the ending_idx smaller than book size
                self.histogram_selected_book_chunk_ending_idx_value = int(self.select_book_chunk_ending_idx_entry.get())
                if data_size <= self.histogram_selected_book_chunk_ending_idx_value:
                    tk.messagebox.showinfo("Input miss mach", "Please input valid number smaller than data size"
                                                              "(ending index is bigger than data size: %d )" % data_size)
                    return

                """ from starting index to finish index"""
                #  load different data according to the user options
                if average_over_iter_option:
                    """ Take the result of the mean average data over iterations """
                    mean_over_iterations = book.mean_prediction_over_iteration()
                    self.histogram = Histograms(
                        book_prediction_res=mean_over_iterations[
                                            self.histogram_selected_book_chunk_staring_idx_value:
                                            self.histogram_selected_book_chunk_ending_idx_value],
                        book_name=book.book_name,
                        smoothed=smoothing_option)
                else:
                    """ Take the result of the average data over iterations """
                    self.histogram = Histograms(
                        book_prediction_res=book.predictions_res_over_iter[-1][
                                            self.histogram_selected_book_chunk_staring_idx_value:
                                            self.histogram_selected_book_chunk_ending_idx_value],
                        book_name=book.book_name,
                        smoothed=smoothing_option)

            # The user choose ending index
            else:
                """ starting index to finish index """
                if average_over_iter_option:
                    """ Take the result of the mean average data over iterations """
                    mean_over_iterations = book.mean_prediction_over_iteration()
                    self.histogram = Histograms(
                        book_prediction_res=mean_over_iterations[
                                            self.histogram_selected_book_chunk_staring_idx_value:],
                        book_name=book.book_name,
                        smoothed=smoothing_option)
                else:
                    """ Take the result of the average data over iterations """
                    self.histogram = Histograms(
                        book_prediction_res=book.predictions_res_over_iter[-1][
                                            self.histogram_selected_book_chunk_staring_idx_value:],
                        book_name=book.book_name,
                        smoothed=smoothing_option)

        """ Pre built function that build selecting the option for book frequency graph and Histogram"""
        Histograms.create_GUI(result_obj=self.histogram, main_frame=self.histogram_frame_bottom_frame)

    """ Logic's Handling and input data checking """

    def check_book_and_chunks_selecting_inputs(self):
        """Check  user input for book frequency graph and Histogram"""
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
        """ Update the top frame part according to the clicked button"""
        # reset the prev button

        if self.top_frame_prev_pressed_Btn != None:
            # reset
            self.top_frame_prev_pressed_Btn["state"] = tk.NORMAL

        cur_button["state"] = tk.DISABLED
        self.top_frame_prev_pressed_Btn = cur_button

        # reset mid frame, and delete all the  widgets
        for widgets in self.mid_frame.winfo_children():
            widgets.destroy()
        self.mid_frame = Frame(self.parent_frame)
        self.mid_frame.grid(row=1, column=0, sticky="nswe")

        # reset bottom frame, and delete all the  widgets
        for widgets in self.bottom_frame.winfo_children():
            widgets.destroy()
        self.bottom_frame = Frame(self.parent_frame)
        self.bottom_frame.grid(row=2, column=0, sticky="nswe")
        self.bottom_frame.grid_rowconfigure(0, weight=4)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

    """ creating Sub-frames"""

    def create_heat_map_frame(self):
        """ create Heat map frame using M matrix """
        if self.heat_map is None:
            """ for testing purposes"""
            # self.heat_map = Heat_map(None, None, testing=True)
            """ The final code point to the global parameters """
            self.heat_map = Heat_map(data=self.M, iteration_size=self.testing_data.iteration_size)

        Heat_map.create_GUI(result_obj=self.heat_map, main_frame=self.mid_frame)
        self.init_bottom_frame(self.testing_data.c3_books_names)

        # fit to the size
        self.mid_frame.grid_propagate(1)

    def create_error_bar_frame(self):
        """ create Error Bar frame using testing data object """

        # in the first time
        if self.error_bar is None:
            """ For testing """
            # self.error_bar = Error_bar(x=None,
            #                            y=None,
            #                            y_mean=None,
            #                            y_mean_c1=None,
            #                            y_mean_c2=None,
            #                            label=None,
            #                            asymmetric_y_error=None,
            #                            testing=True)
            # self.error_bar.create_GUI(result_obj=self.error_bar, main_frame=self.mid_frame)
            """ The Finale Code"""
            # get the data using a thread
            # threading.Thread(target=self.get_error_bar_data_and_show, daemon=True)

            # update self.error_bar and show the results
            self.get_error_bar_data_and_show()
        else:
            self.error_bar.create_GUI(result_obj=self.error_bar, main_frame=self.mid_frame)
            # show  for each index in the graph details about the book
            self.init_bottom_frame(self.error_bar.books_names)

        # fit to the size
        self.mid_frame.grid_propagate(1)

    def selecting_book_chunks_frame(self, main_frame, list_option_value, on_click_func, smoothing_check_box_val,
                                    average_check_box_val, rounding_check_box_val=None):
        """ This GUI part is used in Histogram and chunk label graph \n
            There is Three options: round values,  smooth line, average over iterations. """

        """ select the book """
        self.select_book_label = \
            tk.Label(main_frame, text="Select Book", fg=Pages_parameters.black)

        """ list option """
        self.books_selecting_list_option = tk.OptionMenu(main_frame,
                                                         list_option_value,
                                                         *self.testing_books_names)
        self.books_selecting_list_option.config(width=40)

        """ select the starting idx """
        self.select_book_chunk_staring_idx_label = \
            tk.Label(main_frame, text="Starting index", fg=Pages_parameters.black)

        self.select_book_chunk_staring_idx_entry = tk.Entry(main_frame, width=10)

        """ select the end idx """
        self.select_book_chunk_ending_idx_label = \
            tk.Label(main_frame, text="Final index", fg=Pages_parameters.black)

        self.select_book_chunk_ending_idx_entry = tk.Entry(main_frame, width=10)

        """ rounding check box """
        if rounding_check_box_val is not None:
            self.round_frequency_graph_check_box = tk.Checkbutton(main_frame, text="Round Values",
                                                                  variable=rounding_check_box_val)

        """ smoothing check box """
        self.smooth_frequency_graph_check_box = tk.Checkbutton(main_frame, text="Smooth Graph",
                                                               variable=smoothing_check_box_val)
        """ average data check box """
        self.over_iterations_avg_check_box = tk.Checkbutton(main_frame,
                                                            text="Average over iterations",
                                                            variable=average_check_box_val)

        """ load graph button """
        self.load_graph_Btn = tk.Button(main_frame, text="Chunks Labels",
                                        bg=Pages_parameters.def_bg, fg=Pages_parameters.def_fg,
                                        command=on_click_func)

        """ Set the location of the GUI parts """
        x_padding = 5
        y_padding = 5
        self.select_book_label.grid(row=0, column=0, padx=x_padding, pady=y_padding, sticky="W")
        self.books_selecting_list_option.grid(row=0, column=1, padx=x_padding, pady=y_padding, columnspan=3)

        self.select_book_chunk_staring_idx_label.grid(row=1, column=0, padx=x_padding, pady=y_padding/2, sticky="W")
        self.select_book_chunk_staring_idx_entry.grid(row=1, column=1, padx=x_padding, pady=y_padding/2)
        self.select_book_chunk_ending_idx_label.grid(row=1, column=2, padx=x_padding, pady=y_padding/2)
        self.select_book_chunk_ending_idx_entry.grid(row=1, column=3, padx=x_padding, pady=y_padding/2)
        self.load_graph_Btn.grid(row=1, column=4, padx=x_padding * 2, pady=y_padding/2)

        self.smooth_frequency_graph_check_box.grid(row=0, column=4, padx=x_padding, pady=y_padding)
        self.over_iterations_avg_check_box.grid(row=0, column=5, padx=x_padding, pady=y_padding)
        if rounding_check_box_val is not None:
            self.round_frequency_graph_check_box.grid(row=0, column=6, padx=x_padding, pady=y_padding, columnspan=2)

        # fit to the size
        self.mid_frame.grid_propagate(1)


    def create_chunk_labels_frame(self):
        """ creating chunk labels frame GUI elements and arranging them
        It also  load the prev run data (graph data and GUI elements options) if it exist"""

        """  Split  the main frame """
        self.chunk_labels_frame_top_frame = Frame(self.mid_frame)
        self.chunk_labels_frame_top_frame.grid(row=0, column=0, sticky="nswe")

        self.chunk_labels_frame_bottom_frame = Frame(self.mid_frame)
        self.chunk_labels_frame_bottom_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)

        """ Check Prev data stored and load and set the parameters"""
        self.chunk_labels_book_names_opt = tk.StringVar()
        # load the last val of the prev run
        if self.prev_selected_book_name_chunks_labels != None:
            self.chunk_labels_book_names_opt.set(self.prev_selected_book_name_chunks_labels)
        else:
            self.chunk_labels_book_names_opt.set(self.testing_books_names[0])  # default value

        """ add GUI parts to the top frame (Pre-Built) """
        self.selecting_book_chunks_frame(main_frame=self.chunk_labels_frame_top_frame,
                                         list_option_value=self.chunk_labels_book_names_opt,
                                         on_click_func=self.clicked_on_load_book_chunks_frequency_graph,
                                         smoothing_check_box_val=self.chunks_labels_smooth_frequency_graph_check_box_val,
                                         average_check_box_val=self.chunks_labels_over_iterations_check_box_val,
                                         rounding_check_box_val=self.chunks_labels_round_frequency_graph_check_box_val)

        """ Check Prev data stored and load and set the parameters"""

        # load the values of prev run
        if self.chunks_labels_selected_book_chunk_staring_idx_value != None:
            self.select_book_chunk_staring_idx_entry.delete(0, tk.END)
            self.select_book_chunk_staring_idx_entry.insert(0, str(
                self.chunks_labels_selected_book_chunk_staring_idx_value))
        else:
            self.select_book_chunk_staring_idx_entry.insert(0, '0')

        # load the values of prev run
        if self.chunks_labels_selected_book_chunk_ending_idx_value != None:
            self.select_book_chunk_ending_idx_entry.delete(0, tk.END)
            self.select_book_chunk_ending_idx_entry.insert(0, str(
                self.chunks_labels_selected_book_chunk_ending_idx_value))

        """ load the prev graph"""
        if self.chunk_labels is not None:
            Book_chunks_labels.create_GUI(result_obj=self.chunk_labels, main_frame=self.chunk_labels_frame_bottom_frame)

        # fit to the size
        self.mid_frame.grid_propagate(1)

    def create_histograms_frame(self):
        """ creating histogram frame GUI elements and arranging them
        It also  load the prev run data (graph data and GUI elements options) if it exist"""

        """  Split  the main frame """
        self.histogram_frame_top_frame = Frame(self.mid_frame)
        self.histogram_frame_top_frame.grid(row=0, column=0, sticky="nswe")

        self.histogram_frame_bottom_frame = Frame(self.mid_frame)
        self.histogram_frame_bottom_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)

        """ Check Prev data stored and load and set the parameters"""
        self.histogram_book_names_opt = tk.StringVar()
        # load the last val of the prev run
        if self.prev_selected_book_name_histogram != None:
            self.histogram_book_names_opt.set(self.prev_selected_book_name_histogram)
        else:
            self.histogram_book_names_opt.set(self.testing_books_names[0])  # default value

        """ add GUI parts to the top frame """
        self.selecting_book_chunks_frame(main_frame=self.histogram_frame_top_frame,
                                         list_option_value=self.histogram_book_names_opt,
                                         on_click_func=self.clicked_on_load_books_histogram_graph,
                                         smoothing_check_box_val=self.histogram_smooth_frequency_graph_check_box_val,
                                         average_check_box_val=self.histogram_over_iterations_chunks_labels_check_box_val)

        """ Check Prev data stored and load and set the parameters"""

        # load the values of prev run
        if self.histogram_selected_book_chunk_staring_idx_value != None:
            self.select_book_chunk_staring_idx_entry.delete(0, tk.END)
            self.select_book_chunk_staring_idx_entry.insert(0, str(
                self.histogram_selected_book_chunk_staring_idx_value))
        else:
            self.select_book_chunk_staring_idx_entry.insert(0, '0')

        # load the values of prev run
        if self.histogram_selected_book_chunk_ending_idx_value != None:
            self.select_book_chunk_ending_idx_entry.delete(0, tk.END)
            self.select_book_chunk_ending_idx_entry.insert(0, str(
                self.histogram_selected_book_chunk_ending_idx_value))

        """ load the prev graph"""
        if self.histogram is not None:
            Histograms.create_GUI(result_obj=self.histogram, main_frame=self.histogram_frame_bottom_frame)

        # fit to the size
        self.mid_frame.grid_propagate(1)

    """ Get data """

    def get_error_bar_data_and_show(self):
        """ get error bar data and save it to self.error_bar and show the GUI """
        books_names, books_mean_values_over_all_iter, books_error_down_values_over_all_iter, \
        books_error_up_values_over_all_iter, books_mean_values_over_all_iter, c1_mean_val, c2_mean_val, mean_val \
            = self.testing_data.get_error_bar_data()

        books_indexes = [str(i) for i in range(len(books_names))]

        self.error_bar = Error_bar(books_names=books_names,
                                   x=books_indexes,
                                   y=books_mean_values_over_all_iter,
                                   y_mean=mean_val,
                                   y_mean_c1=c1_mean_val,
                                   y_mean_c2=c2_mean_val,
                                   label="Books Error Bar",
                                   asymmetric_y_error=[books_error_down_values_over_all_iter,
                                                       books_error_up_values_over_all_iter])

        Error_bar.create_GUI(result_obj=self.error_bar, main_frame=self.mid_frame)
        self.init_bottom_frame(self.error_bar.books_names)

    """ Reset """

    def reset_variables(self):
        """ delete the saved objects """
        self.heat_map = None
        self.error_bar = None
        self.chunk_labels = None
        self.histogram = None
