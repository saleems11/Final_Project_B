import matplotlib.pyplot as plt
from scipy import interpolate
from numpy import linspace
from numpy.random import random
import numpy as np


class Book_chunks_labels:

    @staticmethod
    def create_book_chunks_labels(y_data, book_name):
        """" create a graph containing a function that represent each book slice and her label\n
        :parameter\n
        y_data: is an array of 1d that contain the prediction of each chunk,
        book_name: is the book_name"""
        plt.plot(y_data)
        plt.title('labels of each chunk in %s book' % book_name)
        plt.ylabel("label")
        plt.xlabel("Chunks")
        plt.show(block=False)

    @staticmethod
    def create_book_over_iterations_chunks_labels(y_data, book_name, interval_percent=0.7):
        """" create a graph of containing two functions:\n
        First one: the y_data which containing the avg result of book labels over iterations,
        Second one: a smother graph(in default the the interval_percent is 0.7)\n
        :parameter\n
        y_data: is an array of 1d that contain the mean prediction of each chunk,
        book_name: is the book_name"""
        interval = int(len(y_data) * interval_percent)

        plt.plot(y_data, label='Avg values', color='blue', alpha=0.5)
        plt.title('labels of each chunk in %s book' % book_name)

        a_BSpline = interpolate.make_interp_spline([i for i in range(len(y_data))], y_data)
        x_new = linspace(1, interval, len(y_data))
        y_smooth = a_BSpline(x_new)
        plt.plot(y_smooth, label='Smoothed Avg values', color='red', alpha=0.3)

        plt.legend()
        plt.show()

    @staticmethod
    def round_to_three_values(array, min_val, mid_val, max_val):
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




if __name__ == "__main__":
    # values = [0.749, 0.9, 0.3, 0.4, 0.1, 0.749, 0.9, 0.3, 0.4, 0.1, 0.3, 0.4, 0.1]
    values = [random() for i in range(40)]
    # print(values)
    Book_chunks_labels.round_to_three_values(values, 0, 0.5, 1)
    # print(values)
    # Book_chunks_labels.create_book_chunks_labels(values, "It's me")
    Book_chunks_labels.create_book_over_iterations_chunks_labels(values, "hello")
