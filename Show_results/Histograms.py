import matplotlib.pyplot as plt
from numpy.random import random
from scipy import interpolate
from numpy import linspace

class Histograms:

    @staticmethod
    def create_Histograms(book_prediction_res, book_name, bins=10,interval_percent=0.5):
        interval = int(len(book_prediction_res) * interval_percent)

        plt.hist(book_prediction_res, bins=bins, color='b', alpha=0.6, label='predictions', edgecolor='black', linewidth=1.2)

        a_BSpline = interpolate.make_interp_spline([i for i in range(len(book_prediction_res))], book_prediction_res)
        x_new = linspace(1, interval, len(book_prediction_res))
        book_prediction_smooth = a_BSpline(x_new)

        plt.hist(book_prediction_smooth, bins=bins, color='r', alpha=0.5, label='Uniform', edgecolor='black', linewidth=1.2)

        plt.title("%s frequency histogram"%book_name)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.grid(alpha=0.3)
        plt.show()


if __name__ == "__main__":
    # values = [0.749, 0.9, 0.3, 0.4, 0.1, 0.749, 0.9, 0.3, 0.4, 0.1, 0.3, 0.4, 0.1]
    values = [random() for i in range(400)]
    Histograms.create_Histograms(values, "hello")