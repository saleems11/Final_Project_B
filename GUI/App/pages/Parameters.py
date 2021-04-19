from tkinter import Label, StringVar, Button
from tkinter.ttk import Combobox, Entry

from GUI.App.pages import LoadData
from GUI.App.pages.page import Page, def_fg, def_bg

OPTIMZERS = [
    "Adam",
    "SGD",
    "Nesterov accelerated gradient",
    "Adagrad",
    "AdaDelta",
    "RMSProp"

]


class Parameter(Page):
    def __init__(self, parent):
        Page.__init__(self, parent, title='Parameters')
        self.parent = parent
        """ Activation_Function """
        self.activation_function = Label(self, text="Activation Function", bg=def_bg, fg=def_fg)
        self.activation_function.place(x=50, y=100)
        self.n = StringVar()
        self.active_function = Combobox(parent, width=15, textvariable=self.n)
        self.active_function['values'] = (' Sigmoid', ' RElu')
        self.active_function.place(x=250, y=100)
        self.active_function.current(0)
        """Number Of Iterations"""
        self.number_of_iterations = Label(self, text='Number Of Iterations', bg=def_bg, fg=def_fg)
        self.number_of_iterations.place(x=50, y=130)
        self.number_of_iterations_text = Entry(self, width=15)
        self.number_of_iterations_text.place(x=250, y=130)

        """F1- the undersampling rate"""
        self.f1_sampling = Label(self, text='F1- the under sampling rate', bg=def_bg, fg=def_fg)
        self.f1_sampling.place(x=50, y=160)
        self.f1_sampling_text = Entry(self, width=15)
        self.f1_sampling_text.place(x=250, y=160)
        """F- the multiplying rate"""
        self.f_multiplying = Label(self, text='F2- the multiplying rate', bg=def_bg, fg=def_fg)
        self.f_multiplying.place(x=50, y=190)
        self.f_multiplying_text = Entry(self, width=15)
        self.f_multiplying_text.place(x=250, y=190)
        """Accuracy threshold"""
        self.accuracy_threshold = Label(self, text='Accuracy threshold', bg=def_bg, fg=def_fg)
        self.accuracy_threshold.place(x=50, y=220)
        self.accuracy_threshold_text = Entry(self, width=15)
        self.accuracy_threshold_text.place(x=250, y=220)
        """Silhouette threshold"""
        self.silhouette_threshold = Label(self, text='Silhouette threshold', bg=def_bg, fg=def_fg)
        self.silhouette_threshold.place(x=50, y=250)
        self.silhouette_threshold_text = Entry(self, width=15)
        self.silhouette_threshold_text.place(x=250, y=250)
        """Learning Rate"""
        self.learning_rate = Label(self, text='Learning Rate', bg=def_bg, fg=def_fg)
        self.learning_rate.place(x=50, y=280)
        self.learning_rate_text = Entry(self, width=15)
        self.learning_rate_text.place(x=250, y=280)
        """Number of epoch"""
        self.number_of_epoch = Label(self, text='Number of epoch', bg=def_bg, fg=def_fg)
        self.number_of_epoch.place(x=400, y=100)
        self.number_of_epoch_text = Entry(self, width=15)
        self.number_of_epoch_text.place(x=550, y=100)
        """Momentum"""
        self.momentum = Label(self, text='Momentum', bg=def_bg, fg=def_fg)
        self.momentum.place(x=400, y=130)
        self.momentum_text = Entry(self, width=15)
        self.momentum_text.place(x=550, y=130)
        """Decay"""
        self.decay = Label(self, text='Decay', bg=def_bg, fg=def_fg)
        self.decay.place(x=400, y=160)
        self.decay_text = Entry(self, width=15)
        self.decay_text.place(x=550, y=160)
        """Optimizer"""
        self.optimzer = Label(self, text='Optimizer', bg=def_bg, fg=def_fg)
        self.optimzer.place(x=400, y=190)
        self.n = StringVar()
        self.optimzer_func = Combobox(parent, width=15, textvariable=self.n)
        self.optimzer_func['values'] = OPTIMZERS
        self.optimzer_func.current(0)
        self.optimzer_func.place(x=550, y=190)
        self.optimzer_func.current(0)
        """Drop Out"""
        self.drop_out = Label(self, text='Drop Out', bg=def_bg, fg=def_fg)
        self.drop_out.place(x=400, y=220)
        self.drop_out_text = Entry(self, width=15)
        self.drop_out_text.place(x=550, y=220)
        """Tweet Length"""
        self.tweet_length = Label(self, text='Tweet Length', bg=def_bg, fg=def_fg)
        self.tweet_length.place(x=400, y=250)
        self.tweet_length_text = Entry(self, width=15)
        self.tweet_length_text.place(x=550, y=250)
        """Hidden State Size"""
        self.hidden_state_size = Label(self, text='Hidden State Size', bg=def_bg, fg=def_fg)
        self.hidden_state_size.place(x=400, y=280)
        self.hidden_state_size_text = Entry(self, width=15)
        self.hidden_state_size_text.place(x=550, y=280)
        """Buttons"""
        self.back = Button(self, text="Back", bg='red', fg=def_fg, command=self.back)
        self.back.place(x=450, y=400)
        self.add_existing_model = Button(self, text="Add Existing Model", bg='blue', fg=def_fg)
        self.add_existing_model.place(x=490, y=400)
        self.add_parameters_btn = Button(self, text="Add Existing Parameters", bg='blue', fg=def_fg)
        self.add_parameters_btn.place(x=610, y=400)
        self.next_btn = Button(self, text="Next", bg='green', fg=def_fg, command=self.next)
        self.next_btn.place(x=760, y=400)

    def back(self):
        LoadData.HomePage(self.parent)

    def next(self):
        activation_function = self.active_function.get()
