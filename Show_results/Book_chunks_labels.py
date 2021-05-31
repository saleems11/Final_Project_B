import matplotlib.pyplot as plt
from scipy import interpolate
from numpy import linspace
from numpy.random import random
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter

from tkinter import Frame

from Show_results.Matplot_show_fig_tkintner import show_in_tkinter

class Book_chunks_labels(show_in_tkinter):
    """ A Class that store and handle showing the data in Book chunks labels or prediction values.
    The Class extend show_in_tkinter Class to implement showing the graph in tkniter."""
    def __init__(self, y_data, book_name, rounded, smoothed, testing=False):
        """ There is two ways to init, the default is receiving the data, and the other is generating random samples
        when testing is True (for testing purposes).
        y_data:[float] array of y values for each tweet
        book_name:string book name
        rounded:bool round the values to (0, 0.5, 1)"""
        if testing:
            self.y_data = None
            self.book_name = None
            self.rounded = rounded
            self.smoothed = smoothed
            self._generate_sample_data()
        else:
            self.y_data = y_data
            self.book_name = book_name
            self.rounded = rounded
            self.smoothed = smoothed


    def create_book_chunks_labels(self, ax):
        """ create the graph according to the options """
        rounded_data = None
        if self.rounded:
            rounded_data = Book_chunks_labels.round_to_three_values(self.y_data, 0, 0.5, 1)

        self.create_regulare_book_chunks_labels(ax, rounded_data)

        if self.smoothed:
            self.create_smooth_line(ax, rounded_data)




    def create_regulare_book_chunks_labels(self, ax, rounded_data=None):
        """" create a graph containing a function that represent each book slice and her label
        :parameter
        y_data: is an array of 1d that contain the prediction of each chunk,
        book_name: is the book_name"""
        y_label = None
        if rounded_data is None:
            y_label = 'Value'
            ax.plot(self.y_data, label=y_label)
        else:
            y_label = 'Label'
            ax.plot(rounded_data, label=y_label)

        ax.set_title('%s of each chunk in %s book' % (y_label, self.book_name))
        ax.set_ylabel(y_label)
        ax.set_xlabel("Chunks")


    def create_smooth_line(self, ax, data=None, interval_percent=0.7):
        """ create smooth graph for rounded data when data isn't None, and for regular data when data is None
        It create a smoothed line using a_BSpline"""
        if data is None:
            interval = int(len(self.y_data) * interval_percent)
            a_BSpline = interpolate.make_interp_spline([i for i in range(len(self.y_data))], self.y_data)
            x_new = linspace(1, interval, len(self.y_data))
        else:
            interval = int(len(data) * interval_percent)
            a_BSpline = interpolate.make_interp_spline([i for i in range(len(data))], data)
            x_new = linspace(1, interval, len(data))

        y_smooth = a_BSpline(x_new)
        ax.plot(y_smooth, label='Smoothed Avg values', color='red', alpha=0.3)

        ax.legend()


    @staticmethod
    def create_figure(result_obj, dpi) -> Figure:
        """ create a figure according to result_obj """
        # plot the data
        # set the figure size to normal_fig_size
        figure = Figure(figsize=Book_chunks_labels.normal_fig_size)
        ax = figure.subplots()
        # call creating heat map
        result_obj.create_book_chunks_labels(ax=ax)
        return figure

    @staticmethod
    def create_GUI(result_obj, main_frame):
        """ create the GUI that  contain the figure and connect to tkinter"""
        # create two frames
        top_frame = Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="nswe")
        bottom_frame = Frame(main_frame)
        bottom_frame.grid(row=1, column=0, sticky="nswe")

        # create the graph frame, and reduce his size according to main_data_window_size parameter
        window_size_reduction = None
        if result_obj.main_data_window_size > 0.3:
            window_size_reduction = result_obj.main_data_window_size - 0.25
        dpi = top_frame.winfo_fpixels('1i') * window_size_reduction
        init_figure = Book_chunks_labels.create_figure(result_obj=result_obj, dpi=dpi)
        canvas = FigureCanvasTkAgg(init_figure, master=top_frame)
        canvas.draw()

        canvas.get_tk_widget().grid(sticky=tkinter.NSEW)

        # add tool bar
        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        canvas._tkcanvas.grid()
        toolbar.update()



    @staticmethod
    def round_to_three_values(array, min_val, mid_val, max_val):
        """ round values to three values(min_val, mid_val, max_val) """
        first_mid_val = (min_val + mid_val) / 2.0
        second_mid_val = (max_val + mid_val) / 2.0

        res_array = np.zeros((len(array)))
        for i in range(len(array)):
            if array[i] < first_mid_val:
                res_array[i] = min_val
            elif array[i] < second_mid_val:
                res_array[i] = mid_val
            else:
                res_array[i] = max_val

        return res_array


    def _generate_sample_data(self):
        """ generate random samples """
        self.y_data = [random() for i in range(40)]
        self.book_name = "Testing"
