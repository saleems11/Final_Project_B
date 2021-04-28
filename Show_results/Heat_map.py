
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np

import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Heat_map:

    @staticmethod
    def create_heat_map(data, ax=None, block=True):
        """ Recive a 2D array and show the representing heat map"""
        plt.figure()
        ax = sns.heatmap(data=data, fmt="", cmap='RdYlGn', linewidths=0.3, ax=ax)
        ax.invert_yaxis()
        ax.set(xlabel='Books index', ylabel='Books values over iterations', title='Heat map for the prediction result'
                                                                                  'of each book over iterations')

        # plt.show(block=block)


    @staticmethod
    def create_figure(data) -> Figure:
        # plot the data
        figure = Figure(figsize=(8, 10))
        ax = figure.subplots()
        # call creating heat map
        Heat_map.create_heat_map(data=data, ax=ax)
        return figure

    @staticmethod
    def create_GUI(root, data):
        sns.set()
        init_figure = Heat_map.create_figure(data=data)
        canvas = FigureCanvasTkAgg(init_figure, master=root)
        canvas.figure = init_figure
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        return canvas


    @staticmethod
    def convert_M_to_heat_map(M, iteration_size):
        """ receive an 2D numpy array and slice it according to iteration size and takes the first value"""

        temp = np.copy(M)

        # M = M[:, 0]
        num_of_books = int(len(temp)/ iteration_size)
        return np.reshape(temp, (num_of_books, iteration_size))

    @staticmethod
    def _generate_sample_data():
        M = np.array([1, 10, 12, 16, 1, 18, 8, 9, 1, 12, 16, 1, 18, 8, 2])
        iteration_size = 3
        return M, iteration_size

if __name__ == "__main__":
    M, iteration_size = Heat_map._generate_sample_data()
    # Heat_map.create_heat_map([[1,2],[2,3],[4,3]])
    Heat_map.create_heat_map(Heat_map.convert_M_to_heat_map(M, iteration_size))