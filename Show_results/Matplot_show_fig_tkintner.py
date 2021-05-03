import abc


class show_in_tkinter(metaclass=abc.ABCMeta):

    # in percent
    main_data_window_size = 0.8

    @staticmethod
    @abc.abstractmethod
    def create_GUI(result_obj, main_frame, data):
        pass

    @staticmethod
    @abc.abstractmethod
    def create_figure(result_obj, data, dpi):
        pass

    @abc.abstractmethod
    def _generate_sample_data(self):
        pass
