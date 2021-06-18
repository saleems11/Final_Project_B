import abc


class show_in_tkinter(metaclass=abc.ABCMeta):
    """ abstract Class for showing the graph and connecting them into tkintner"""
    # in percent
    def __init__(self):
        self.main_data_window_size = 0.8
        self.tall_fig_size = [12, 4]
        self.normal_fig_size = [11.5, 3.5]

    @staticmethod
    @abc.abstractmethod
    def create_GUI(result_obj, main_frame, data):
        """ a function template for creating the GUI that contain the figure and connect to tkinter"""
        pass

    @staticmethod
    @abc.abstractmethod
    def create_figure(result_obj, data, dpi):
        """ a function template for creating a figure """
        pass

    @abc.abstractmethod
    def _generate_sample_data(self):
        """ private function template for generating random samples """
        pass
