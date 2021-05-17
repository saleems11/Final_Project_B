import matplotlib.pyplot as plt
from numpy.random import random
from scipy import interpolate
from numpy import linspace

from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import Frame
import tkinter

from Show_results.Matplot_show_fig_tkintner import show_in_tkinter

class Histograms(show_in_tkinter):

    def __init__(self, book_prediction_res, book_name, smoothed, testing=False):
        if testing:
            self.book_prediction_res = None
            self.book_name = None
            self.smoothed = smoothed
            self._generate_sample_data()
        else:
            self.book_prediction_res = book_prediction_res
            self.book_name = book_name
            self.smoothed = smoothed

    def create_Histograms(self, ax):
        self.create_regulare_Histograms(ax)
        if self.smoothed:
            self.create_smoothed_histogram(ax)

    def create_regulare_Histograms(self, ax, bins=10):
        ax.hist(self.book_prediction_res, bins=bins, color='b', alpha=0.6, label='predictions', edgecolor='black', linewidth=1.2)

        ax.set_title("%s frequency histogram" % self.book_name)
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        ax.grid(alpha=0.3)


    def create_smoothed_histogram(self, ax, bins=10, interval_percent=0.5):
        interval = int(len(self.book_prediction_res) * interval_percent)

        a_BSpline = interpolate.make_interp_spline([i for i in range(len(self.book_prediction_res))], self.book_prediction_res)
        x_new = linspace(1, interval, len(self.book_prediction_res))
        book_prediction_smooth = a_BSpline(x_new)

        ax.hist(book_prediction_smooth, bins=bins, color='r', alpha=0.5, label='Smoothed Value', edgecolor='black', linewidth=1.2)
        ax.legend()

    @staticmethod
    def create_figure(result_obj, dpi) -> Figure:
        # plot the data
        # figure = Figure(dpi=dpi)
        figure = Figure(figsize=Histograms.normal_fig_size)
        ax = figure.subplots()
        # call creating heat map
        result_obj.create_Histograms(ax=ax)
        return figure

    @staticmethod
    def create_GUI(result_obj, main_frame):
        # create two frames
        top_frame = Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="nswe")
        bottom_frame = Frame(main_frame)
        bottom_frame.grid(row=1, column=0, sticky="nswe")

        window_size_reduction = None
        if result_obj.main_data_window_size > 0.3:
            window_size_reduction = result_obj.main_data_window_size - 0.25

        dpi = top_frame.winfo_fpixels('1i') * window_size_reduction
        init_figure = Histograms.create_figure(result_obj=result_obj, dpi=dpi)
        canvas = FigureCanvasTkAgg(init_figure, master=top_frame)
        canvas.draw()

        canvas.get_tk_widget().grid(sticky=tkinter.NSEW)

        # add tool bar
        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        canvas._tkcanvas.grid()
        toolbar.update()



    def _generate_sample_data(self):
        self.book_prediction_res = [random() for i in range(400)]
        self.book_name = "Testing"


if __name__ == "__main__":
    # values = [0.749, 0.9, 0.3, 0.4, 0.1, 0.749, 0.9, 0.3, 0.4, 0.1, 0.3, 0.4, 0.1]
    values = [random() for i in range(400)]
    Histograms.create_Histograms(values, "hello")