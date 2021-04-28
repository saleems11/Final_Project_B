
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np

class Heat_map:

    @staticmethod
    def create_heat_map(data):
        """ Recive a 2D array and show the representing heat map"""
        plt.figure()
        ax = sns.heatmap(data=data, fmt="", cmap='RdYlGn', linewidths=0.3)
        ax.invert_yaxis()
        ax.set(xlabel='Books index', ylabel='Books values over iterations', title='Heat map for the prediction result'
                                                                                  'of each book over iterations')

        plt.show(block=False)


    @staticmethod
    def convert_M_to_heat_map(M, iteration_size):
        """ receive an 2D numpy array and slice it according to iteration size and takes the first value"""
        # M = M[:, 0]
        num_of_books = int(len(M)/ iteration_size)
        return np.reshape(M, (num_of_books, iteration_size))

if __name__ == "__main__":
    M = np.array([[1,10],[2,8],[3,2]])
    iteration_size = 1
    # Heat_map.create_heat_map([[1,2],[2,3],[4,3]])
    Heat_map.create_heat_map(Heat_map.convert_M_to_heat_map(M, iteration_size))