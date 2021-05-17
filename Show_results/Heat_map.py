import seaborn as sns
import matplotlib.pylab as plt
import numpy as np

import tkinter
from tkinter import Frame

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Show_results.Matplot_show_fig_tkintner import show_in_tkinter


class Heat_map(show_in_tkinter):

    def __init__(self, data, iteration_size, testing=False):
        if testing:
            self.data = None
            self.iteration_size = None
            self._generate_sample_data()
            self.data = Heat_map.convert_M_to_heat_map(self.data, self.iteration_size)
        else:
            self.data = Heat_map.convert_M_to_heat_map(data, iteration_size)
            self.iteration_size = iteration_size


    def create_heat_map(self, ax=None, block=True):
        """ Recive a 2D array and show the representing heat map"""
        plt.figure()
        ax = sns.heatmap(data=self.data, fmt="", cmap='RdYlGn', linewidths=0.3, ax=ax)
        ax.invert_yaxis()
        ax.set(xlabel='Books index', ylabel='Books values over iterations', title='Heat map for the prediction result'
                                                                                  ' of each book over iterations')

        # plt.show(block=block)

    @staticmethod
    def create_figure(result_obj, dpi) -> Figure:
        # plot the data
        # figure = Figure(dpi=dpi)
        figure = Figure(figsize=Heat_map.tall_fig_size)
        ax = figure.subplots()
        # call creating heat map
        result_obj.create_heat_map(ax=ax)
        return figure

    @staticmethod
    def create_GUI(result_obj, main_frame):
        # create two frames
        top_frame = Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="nswe")
        bottom_frame = Frame(main_frame)
        bottom_frame.grid(row=1, column=0, sticky="nswe")

        dpi = top_frame.winfo_fpixels('1i')*result_obj.main_data_window_size
        init_figure = Heat_map.create_figure(result_obj=result_obj, dpi=dpi)
        canvas = FigureCanvasTkAgg(init_figure, master=top_frame)
        canvas.draw()
        # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        canvas.get_tk_widget().grid(sticky=tkinter.NSEW)
        # add tool bar

        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        canvas._tkcanvas.grid()
        toolbar.update()

    @staticmethod
    def convert_M_to_heat_map(M, iteration_size):
        """ receive an 2D numpy array and slice it according to iteration size and takes the first value"""

        temp = np.copy(M)

        # M = M[:, 0]
        num_of_books = int(len(temp) / iteration_size)
        return np.reshape(temp, (num_of_books, iteration_size))


    def _generate_sample_data(self):
        self.data = np.array([1, 10, 12, 16, 1, 18, 8, 9, 1, 12, 16, 1, 18, 8, 2,
                      2, 1, 5, 9, 2, 1, 2, 4, 9, 2, 7, 9, 3, 4, 1])
        self.iteration_size = 10


if __name__ == "__main__":
    M, iteration_size = Heat_map._generate_sample_data()
    # Heat_map.create_heat_map([[1,2],[2,3],[4,3]])
    Heat_map.create_heat_map(Heat_map.convert_M_to_heat_map(M, iteration_size))
