
import matplotlib.pylab as plt

class Error_bar:

    @staticmethod
    def create_error_bar(x, y, y_mean, y_mean_c1, y_mean_c2, label: str, asymmetric_y_error: [[float,], [float,]]):
        """ Receive :\n
        X: for book index or books names,
        y: is the y value for the specific book,
        label: is string for the name of the plot,
        asymmetric_y_error: [+y, -y] the error for the y value,
        from the top and the bottom, input structure [[y+,..], [y-,..]]"""
        # ax = plt.subplots()

        plt.scatter(x, y, label=label)
        plt.errorbar(x, y, yerr=asymmetric_y_error)

        # the mean line
        mean_line = plt.axhline(y=y_mean, color='r', linestyle='-', alpha=0.3, label='mean value')

        # the mean lines for the two clusters
        mean_line_c1 = plt.axhline(y=y_mean_c1, color='g', linestyle='--', alpha=0.3, label='mean value c1')
        mean_line_c2 = plt.axhline(y=y_mean_c2, color='b', linestyle='--', alpha=0.3, label='mean value c2')

        legend = plt.legend(loc='upper right')
        plt.show()



if __name__ == "__main__":
    Error_bar.create_error_bar(["hello", "how", "hi"], [10, 12, 13], 11, 12, 10, "Testing", [[1, 2, 3], [3, 1, 1]])