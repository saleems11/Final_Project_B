
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import Frame
import tkinter

from Show_results.Matplot_show_fig_tkintner import show_in_tkinter

class Error_bar(show_in_tkinter):
    """ A Class that store and handle showing the data in Error bar graph of all the books .
    The Class extend show_in_tkinter Class to implement showing the graph in tkniter."""
    def __init__(self, books_names, x, y, y_mean, y_mean_c1, y_mean_c2, label: str, asymmetric_y_error: [[float,], [float,]], testing=False):
        """There is two ways to init, the default is receiving the data, and the other is generating random samples
        when testing is True (for testing purposes).
        Receive :
        books_names:[string] array of books names
        x: for book index or books names
        y: is the y value for the specific book
        y_mean: float the mean value of all the clusters
        y_mean_c1: float the mean of cluster c1
        y_mean_c2: float the mean of cluster c2
        label: is string for the name of the plot
        asymmetric_y_error: [-y, +y] the error for the y value
        from the top and the bottom, input structure [[y-,..], [y+,..]]"""

        if testing:
            self.books_names =None
            self.x = None
            self.y = None
            self.y_mean = None
            self.y_mean_c1 = None
            self.y_mean_c2 = None
            self.label = None
            self.asymmetric_y_error = None
            self._generate_sample_data()
        else:
            self.books_names = books_names
            self.x = x
            self.y = y
            self.y_mean = y_mean
            self.y_mean_c1 = y_mean_c1
            self.y_mean_c2 = y_mean_c2
            self.label = label
            self.asymmetric_y_error = asymmetric_y_error


    def create_error_bar(self, ax):
        """ create the graph, and all his parts """
        ax.scatter(self.x, self.y, label=self.label)
        ax.errorbar(self.x, self.y, yerr=self.asymmetric_y_error)

        ax.set_title('Error bar of all the book mean values over each iteration')

        # the mean line
        mean_line = ax.axhline(y=self.y_mean, color='r', linestyle='-', alpha=0.3, label='mean value')

        # the mean lines for the two clusters
        mean_line_c1 = ax.axhline(y=self.y_mean_c1, color='g', linestyle='--', alpha=0.3, label='mean value c1')
        mean_line_c2 = ax.axhline(y=self.y_mean_c2, color='b', linestyle='--', alpha=0.3, label='mean value c2')

        legend = ax.legend(loc='upper right')

    @staticmethod
    def create_figure(result_obj, dpi) -> Figure:
        """ create a figure according to result_obj """
        # plot the data
        # set the figure size to tall_fig_size
        figure = Figure(figsize=Error_bar.tall_fig_size)
        ax = figure.subplots()
        # call creating heat map
        result_obj.create_error_bar(ax=ax)
        return figure

    @staticmethod
    def create_GUI(result_obj, main_frame):
        """ create the GUI that  contain the figure and connect to tkinter"""
        # create two frames
        top_frame = Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="nswe")
        bottom_frame = Frame(main_frame)
        bottom_frame.grid(row=1, column=0, sticky="nswe")

        # create the graph frame
        dpi = top_frame.winfo_fpixels('1i')*result_obj.main_data_window_size
        init_figure = Error_bar.create_figure(result_obj=result_obj, dpi=dpi)
        canvas = FigureCanvasTkAgg(init_figure, master=top_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky=tkinter.NSEW)

        # add tool bar
        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        canvas._tkcanvas.grid()
        toolbar.update()

    def _generate_sample_data(self):
        """ generate random samples """
        c1_test_names = ["Al_Mustasfa_min_ilm_al_Usul", "Fada_ih_al_Batiniyya_wa_Fada_il_al_Mustazhiriyy",
                         "Faysal_at_Tafriqa_Bayna_al_Islam_wa_al_Zandaqa", "al_iqtisad_fi_al_itiqad",
                         "Iljam_Al_Awamm_an_Ilm_Al_Kalam"]
        self.x = c1_test_names
        self.y = [10, 12, 13, 15, 16]
        self.y_mean = 11
        self.y_mean_c1 = 12
        self.y_mean_c2 = 10
        self.label = "Testing"
        self.asymmetric_y_error = [[1, 2, 3, 4, 5], [3, 1, 1, 2, 1]]