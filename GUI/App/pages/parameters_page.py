from tkinter import Label, StringVar, Button, messagebox, END
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Entry
from typing import List

from models.LSTM.Parameters import Parameters
from .Train import TrainPage
from .page import Page, def_bg, def_fg
ITERATION_MAX_NUMBER = 10000
OPTIMZERS = [
    "Adam",
    "SGD",
    "Adagrad",
    "AdaDelta",
    "RMSProp"

]
ACTIVATION_FUNCTION = ["Sigmoid", "RElu"]




class Param(Page):
    def __init__(self, parent, c1_embeded, c2_embeded, testing_data_embeded, tweet_length):
        Page.__init__(self, parent, title='Parameters')
        self.parent = parent
        self.filename: str = ''
        self.c1_embeded = c1_embeded
        self.c2_embeded = c2_embeded
        self.testing_data_embeded = testing_data_embeded
        self.tweet_length = tweet_length
        """ Activation_Function """
        self.activation_function = Label(self, text="Activation Function", bg=def_bg, fg=def_fg)
        self.activation_function.place(x=50, y=100)
        self.n = StringVar()
        self.active_function = Combobox(parent, width=15, textvariable=self.n)
        self.active_function['values'] = ACTIVATION_FUNCTION
        self.active_function.place(x=250, y=100)
        self.active_function.current(ACTIVATION_FUNCTION.index('RElu'))

        """Number Of Iterations"""
        self.number_of_iterations = Label(self, text='Number Of Iterations', bg=def_bg, fg=def_fg)
        self.number_of_iterations.place(x=50, y=130)
        self.number_of_iterations_text = Entry(self, width=15)
        self.number_of_iterations_text.place(x=250, y=130)
        self.number_of_iterations_text.insert(0,'3')
        """F1- the undersampling rate"""
        self.f1_sampling = Label(self, text='F1- the under sampling rate', bg=def_bg, fg=def_fg)
        self.f1_sampling.place(x=50, y=160)
        self.f1_sampling_text = Entry(self, width=15)
        self.f1_sampling_text.place(x=250, y=160)
        self.f1_sampling_text.insert(0,'3')
        """F- the multiplying rate"""
        self.f_multiplying = Label(self, text='F2- the multiplying rate', bg=def_bg, fg=def_fg)
        self.f_multiplying.place(x=50, y=190)
        self.f_multiplying_text = Entry(self, width=15)
        self.f_multiplying_text.place(x=250, y=190)
        self.f_multiplying_text.insert(0,'3')
        """Accuracy threshold"""
        self.accuracy_threshold = Label(self, text='Accuracy threshold', bg=def_bg, fg=def_fg)
        self.accuracy_threshold.place(x=50, y=220)
        self.accuracy_threshold_text = Entry(self, width=15)
        self.accuracy_threshold_text.place(x=250, y=220)
        self.accuracy_threshold_text.insert(0,'0.90')

        """Silhouette threshold"""
        self.silhouette_threshold = Label(self, text='Silhouette threshold', bg=def_bg, fg=def_fg)
        self.silhouette_threshold.place(x=50, y=250)
        self.silhouette_threshold_text = Entry(self, width=15)
        self.silhouette_threshold_text.place(x=250, y=250)
        self.silhouette_threshold_text.insert(0,'0.75')

        """Learning Rate"""
        self.learning_rate = Label(self, text='Learning Rate', bg=def_bg, fg=def_fg)
        self.learning_rate.place(x=50, y=280)
        self.learning_rate_text = Entry(self, width=15)
        self.learning_rate_text.place(x=250, y=280)
        self.learning_rate_text.insert(0,'0.001')

        """Number of epoch"""
        self.number_of_epoch = Label(self, text='Number of epoch', bg=def_bg, fg=def_fg)
        self.number_of_epoch.place(x=400, y=100)
        self.number_of_epoch_text = Entry(self, width=15)
        self.number_of_epoch_text.place(x=550, y=100)
        self.number_of_epoch_text.insert(0,'15')

        """Optimizer"""
        self.optimzer = Label(self, text='Optimizer', bg=def_bg, fg=def_fg)
        self.optimzer.place(x=400, y=130)
        self.n1 = StringVar()
        self.optimzer_func = Combobox(parent, width=15, textvariable=self.n1)
        self.optimzer_func['values'] = OPTIMZERS
        self.optimzer_func.current(0)
        self.optimzer_func.place(x=550, y=130)
        """Drop Out"""
        self.drop_out = Label(self, text='Drop Out', bg=def_bg, fg=def_fg)
        self.drop_out.place(x=400, y=160)
        self.drop_out_text = Entry(self, width=15)
        self.drop_out_text.place(x=550, y=160)
        self.drop_out_text.insert(0,'0.4')

        """Hidden State Size"""
        self.hidden_state_size = Label(self, text='Hidden State Size', bg=def_bg, fg=def_fg)
        self.hidden_state_size.place(x=400, y=190)
        self.hidden_state_size_text = Entry(self, width=15)
        self.hidden_state_size_text.place(x=550, y=190)
        self.hidden_state_size_text.insert(0,'300')
        """Batch_Size"""
        self.batch_size = Label(self, text='Batch Size', bg=def_bg, fg=def_fg)
        self.batch_size.place(x=400, y=220)
        self.batch_size_text = Entry(self, width=15)
        self.batch_size_text.place(x=550, y=220)
        self.batch_size_text.insert(0,'300')


        """Buttons"""
        # self.back = Button(self, text="Back", bg='red', fg=def_fg, command=self.back)
        # self.back.place(x=560, y=400)
        self.add_parameters_btn = Button(self, text="Add Existing Parameters", bg='blue', fg=def_fg, command=self.add_exist_parameters)
        self.add_parameters_btn.place(x=610, y=400)
        self.next_btn = Button(self, text="Next", bg='green', fg=def_fg, command=self.next)
        self.next_btn.place(x=760, y=400)

    def back(self):
        pass

    def next(self):
        result: List[str] = [self.check_if_integer(value=self.number_of_iterations_text.get(), min_number=1,
                                                    max_number=ITERATION_MAX_NUMBER,msg='Number of iteration'),
                              self.check_if_integer(value=self.f1_sampling_text.get(), min_number=0,
                                                    max_number=ITERATION_MAX_NUMBER, msg='F1-Under Sampling'),
                              self.check_if_integer(value=self.f_multiplying_text.get(), min_number=0,
                                                    max_number=ITERATION_MAX_NUMBER, msg='F-Multiplying'),
                              self.check_if_float(value=self.accuracy_threshold_text.get(), min_number=0,
                                                  max_number=1.0, msg='Accuracy threshold'),
                              self.check_if_float(value=self.silhouette_threshold_text.get(), min_number=0,
                                                  max_number=1.0, msg='Silhouette Threshold'),
                              self.check_if_float(value=self.learning_rate_text.get(), min_number=0,
                                                  max_number=1.0, msg='Learning Rate'),
                              self.check_if_integer(value=self.number_of_epoch_text.get(), min_number=0,
                                                    max_number=ITERATION_MAX_NUMBER, msg='Number of Epoch'),
                              self.check_if_float(value=self.drop_out_text.get(), min_number=0,
                                                  max_number=1.0, msg='DropOut'),
                              self.check_if_integer(value=self.hidden_state_size_text.get(), min_number=0,
                                                    max_number=ITERATION_MAX_NUMBER, msg='Hidden State Size'),
                             self.check_if_integer(value=self.batch_size_text.get(), min_number=0,
                                                   max_number=ITERATION_MAX_NUMBER, msg='Batch Size')
                             ]
        check_ = [not res for res in result]
        if all(check_):
            lstm_hidden_state_size = int(self.hidden_state_size_text.get())
            fully_connected_layer = int(300)
            drop_out = float(self.drop_out_text.get())
            learning_rate = float(self.learning_rate_text.get())
            number_of_epoch = int(self.number_of_epoch_text.get())
            number_of_iteration = int(self.number_of_iterations_text.get())
            undersampling_rate = int(self.f1_sampling_text.get())
            multiplying_rate = int(self.f_multiplying_text.get())
            accuracy_threshold = float(self.accuracy_threshold_text.get())
            silhouette_threshold = float(self.silhouette_threshold_text.get())
            optimizer = str(self.optimzer_func.get())
            activation_function = str(self.active_function.get())
            batch_size = int(self.batch_size_text.get())

            parameters = Parameters(lstm_hidden_state_size=lstm_hidden_state_size, fully_connect_layer=fully_connected_layer,
                                    drop_out=drop_out, learning_rate=learning_rate, number_of_epoch=number_of_epoch,
                                    number_of_iteration=number_of_iteration, undersampling_rate=undersampling_rate,
                                    multiplying_rate=multiplying_rate, accuracy_threshold=accuracy_threshold,
                                    silhouette_threshold=silhouette_threshold, optimizer=optimizer, activation_function=activation_function,
                                    batch_size=batch_size,tweet_length=self.tweet_length)
            TrainPage(parent=self.parent, parameters=parameters, c1_embeded=self.c1_embeded,
                      c2_embeded=self.c2_embeded, testing_data_embeded=self.testing_data_embeded)
        else:
            messagebox.showwarning(title='ERROR', message='\n'.join(result))

    def check_if_float(self,max_number: float, min_number: float, value, check: bool = True, msg: str = '') -> str:
        """
        return None str if it float and not None else return a good message
        """
        try:
            if not value:
                return f'{msg} -value is empty'
            val = float(value)
            if check:
                if min_number < val < max_number:
                    return ''
                return f'{msg}-Please enter value between {min_number} and {max_number}\n'
            return ''
        except ValueError:
            return f'{msg}- is not an float'


    def check_if_integer(self, max_number: float, min_number: float, value, check: bool = True, msg: str='') -> str:
        try:
            if not value:
                return f'{msg} -value is empty'
            val = int(value)
            if check:
                if min_number < val < max_number:
                    return ''
                return f'{msg}-Please enter value between {min_number} and {max_number}\n'
            return ''
        except ValueError:
            return f'{msg}- is not an integer'

    def add_exist_parameters(self):
        messagebox.showwarning(title='Tip', message='Please fill the text with parameters, parameter:value')
        self.filename = askopenfilename()
        print(self.filename)
        if not self.filename.endswith('.txt'):
            messagebox.showwarning(title='Tip', message='File is not txt file')
            return
        with open(file=self.filename) as parameter_file:
            for line in parameter_file:
                parameter, value = line.split(':')
                value: str = value.strip()
                if parameter == 'Activation Function' and value in ACTIVATION_FUNCTION:
                    self.active_function.current(ACTIVATION_FUNCTION.index(value))
                elif parameter == 'Number Of Iterations':
                    self.number_of_iterations_text.delete(0, END)
                    self.number_of_iterations_text.insert(0, value)
                elif parameter == 'F1- the under sampling rate':
                    self.f1_sampling_text.delete(0, END)
                    self.f1_sampling_text.insert(0, value)
                elif parameter == 'F2- the multiplying rate':
                    self.f_multiplying_text.delete(0, END)
                    self.f_multiplying_text.insert(0, value)
                elif parameter == 'Accuracy threshold':
                    self.accuracy_threshold_text.delete(0, END)
                    self.accuracy_threshold_text.insert(0, value)
                elif parameter == 'Silhouette threshold':
                    self.silhouette_threshold_text.delete(0, END)
                    self.silhouette_threshold_text.insert(0, value)
                elif parameter == 'Learning Rate':
                    self.learning_rate_text.delete(0, END)
                    self.learning_rate_text.insert(0, value)
                elif parameter == 'Number of epoch':
                    self.number_of_epoch_text.delete(0, END)
                    self.number_of_epoch_text.insert(0, value)
                elif parameter == 'Optimizer' and value in OPTIMZERS:
                    print(OPTIMZERS.index(value))
                    self.optimzer_func.current(OPTIMZERS.index(value))
                elif parameter == 'Drop Out':
                    self.drop_out_text.delete(0, END)
                    self.drop_out_text.insert(0, value)
                elif parameter == 'Hidden State Size':
                    self.hidden_state_size_text.delete(0, END)
                    self.hidden_state_size_text.insert(0, value)
                else:
                    messagebox.showwarning(title='Tip', message=f'The {parameter} is not exist please check it or\n it not assigned perfectly')


