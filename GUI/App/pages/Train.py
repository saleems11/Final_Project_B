import os
import threading
import traceback
from time import sleep
from tkinter import Label, Button, HORIZONTAL, IntVar, filedialog, messagebox, NORMAL, DISABLED
from tkinter.ttk import Progressbar

import numpy as np
import time
from PIL import Image, ImageTk
from keras import models

from Exceptions.Exceptions import SilhouetteBellowThreshold, AnchorsInSameCluster
from GUI.App.pages import parameters_page
from GUI.App.pages import ShowResultsPage
from GUI.App.pages.page import Page, def_fg, def_bg, TESTING_INFO
from GUI.App.pages.process_bar import ProcessBar
from Objects import TestingData
from models.LSTM.Bi_Direct_LSTM import Bi_Direct_LSTM
from models.LSTM.Parameters import Parameters

def_fg_label = 'black'
def_red_color = '#CC0000'
def_blue_color = '#5C5CFF'

def Sprite(picture, res1, res2):
    im = Image.open(picture).convert("RGBA").resize((res1, res2), Image.BOX)
    pic = ImageTk.PhotoImage(im)
    cor = Image.open(picture)
    print(cor.mode)
    return pic


class TrainPage(Page):
    def __init__(self, parent, parameters: Parameters, c1_embeded, c2_embeded, testing_data_embeded: TestingData):
        print("Showning settings page")
        self.parameters = parameters
        self.process_bar = ProcessBar()

        # for time estimating
        self.estimated_time_remaining = [-1]

        self.lstm = Bi_Direct_LSTM(parameters=self.parameters, process_bar=self.process_bar,
                                   estimated_time_remaining=self.estimated_time_remaining)

        self.p1 = threading.Thread(target=self.update_status, daemon=True)
        self.p = threading.Thread(target=self.start_training_testing, daemon=True)
        self.parent = parent
        self.c1_embeded = c1_embeded
        self.c2_embeded = c2_embeded
        self.testing_data_embeded = testing_data_embeded
        # init page/ delete old page
        Page.__init__(self, parent, title='Training and Testing Page')
        self.value = IntVar()
        self.value.set(5)
        """Status"""
        self.status = Label(self, text="Status Bar", bg=def_bg, fg=def_fg_label)
        self.status.place(x=100, y=100)
        """Status bar"""
        self.bar = Progressbar(self, orient=HORIZONTAL, length=700, mode="determinate")
        self.bar.place(x=200, y=100)
        """Accuracy"""
        self.accuracy = Label(self, text="Accuracy", bg=def_bg, fg=def_fg_label)
        self.accuracy.place(x=100, y=150)
        self.accuracy_text = Label(self, text="Loading", bg=def_bg, fg=def_fg_label)
        self.accuracy_text.place(x=200, y=150)
        """Loss"""
        self.loss = Label(self, text="Loss", bg=def_bg, fg=def_fg_label)
        self.loss.place(x=100, y=180)
        self.loss_text = Label(self, text="Loading", bg=def_bg, fg=def_fg_label)
        self.loss_text.place(x=200, y=180)
        """Iteration"""
        self.iteration = Label(self, text="Iteration", bg=def_bg, fg=def_fg_label)
        self.iteration.place(x=100, y=210)
        self.iteration_text = Label(self, text="{iteration_number}\{inumber_of_iteration}", bg=def_bg, fg=def_fg_label)
        self.iteration_text.place(x=200, y=210)
        """Val Accuracy"""
        self.val_accuracy = Label(self, text="Val Accuracy", bg=def_bg, fg=def_fg_label)
        self.val_accuracy.place(x=100, y=240)
        self.val_accuracy_text = Label(self, text="Loading", bg=def_bg, fg=def_fg_label)
        self.val_accuracy_text.place(x=200, y=240)
        """Val loss"""
        self.val_loss = Label(self, text="Val Loss", bg=def_bg, fg=def_fg_label)
        self.val_loss.place(x=100, y=270)
        self.val_loss_text = Label(self, text="Loading", bg=def_bg, fg=def_fg_label)
        self.val_loss_text.place(x=200, y=270)
        """silhouette_score"""
        self.silhouette_score = Label(self, text="Silhouette Score", bg=def_bg, fg=def_fg_label)
        self.silhouette_score.place(x=100, y=300)
        self.silhouette_score_text = Label(self, text="Loading", bg=def_bg, fg=def_fg_label)
        self.silhouette_score_text.place(x=200, y=300)
        """time_remaining"""
        self.time_remaining = Label(self, text="E.Time Remaining", bg=def_bg, fg=def_fg_label)
        self.time_remaining.place(x=100, y=330)
        self.time_remaining_text = Label(self, text="Loading", bg=def_bg, fg=def_fg_label)
        self.time_remaining_text.place(x=200, y=330)

        """Back"""
        self.back_btn = Button(self, text="Back", bg=def_red_color, fg=def_fg, command=self.back)
        self.back_btn.place(x=470, y=400)
        """Next"""
        self.next_btn = Button(self, text="Next", bg='#5CAD5C', fg=def_fg, command=self.next)
        self.next_btn.place(x=780, y=400)
        """Save Model"""
        self.save_model = Button(self, text="Save The Model", bg="#CC8400", fg=def_fg, command=self.save_the_model)
        self.save_model.place(x=510, y=400)
        """Load Model"""
        self.load_model_btn = Button(self, text="Load Model", bg="#CC8400", fg=def_fg, command=self.load_model)
        self.load_model_btn.place(x=390, y=400)
        """Start Testing"""
        self.start_training_and_testing = Button(self, text="Start Training and Testing", bg='#5CAD5C', fg=def_fg, command=self.start_lstm_model)
        self.start_testing = Button(self, text="Start Testing", bg='#5CAD5C', fg=def_fg, command=self.start_lstm_testing)
        self.start_training_and_testing.place(x=610, y=400)
        if not self.process_bar.finished:
            self.save_model['state'] = DISABLED
            self.next_btn['state'] = DISABLED
            # self.back_btn['state'] = DISABLED

    def start_lstm_testing(self):
        """ this function will start testing the model, and update the page of start
        testing and training parameters """

        """ disable all the buttons """
        self.back_btn['state'] = DISABLED
        self.start_testing['state'] = DISABLED
        self.save_model['state'] = DISABLED
        self.next_btn['state'] = DISABLED
        self.start_testing['state'] = DISABLED
        self.load_model_btn['state'] = DISABLED

        try:
            self.M, self.silhoutte_score = self.lstm.test_model(self.testing_data_embeded)
            self.silhouette_score_text['text'] = self.silhoutte_score
            self.process_bar.finished = True
            self.set_progress_bar(100.0)

            """ show popup when finished successfully """
            messagebox.showinfo(title='Testing Finished',
                                message='Running on the testing data is finished')
            """ make buttons click-able """
            self.next_btn['state'] = NORMAL
            self.load_model_btn['state'] = NORMAL

        except SilhouetteBellowThreshold as e:
            """ Handle the Exceptions """
            messagebox.showwarning(title='Error of Silhouette Bellow Threshold', message=f'{str(e)}')

            parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
                                  testing_data_embeded=self.testing_data_embeded,
                                  tweet_length=self.lstm.parameters.tweet_length)

        except AnchorsInSameCluster as e:
            messagebox.showwarning(title='Error of AnchorsInSameCluster', message=f'{str(e)}')

            parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
                                  testing_data_embeded=self.testing_data_embeded,
                                  tweet_length=self.lstm.parameters.tweet_length)

    def load_model(self):
        """this function load the model from data file"""
        model_dir = filedialog.askdirectory()
        if not model_dir:
            return
        if not os.path.exists(os.path.join(model_dir, 'saved_model.pb')) or\
                not os.path.exists(os.path.join(model_dir, 'parameters.txt')):
            messagebox.showwarning(title='File not found', message='The saved_model.pb file is not exist\n or parameters file not exist')
            return


        """ disable all buttons """
        self.back_btn['state'] = DISABLED
        self.save_model['state'] = DISABLED
        self.next_btn['state'] = DISABLED
        self.start_testing['state'] = DISABLED
        self.start_training_and_testing['state'] = DISABLED
        self.load_model_btn['state'] = DISABLED

        messagebox.showinfo(title='Loading Model',
                            message='Loading The model could take some time')

        self.load_parameters(file_path=os.path.join(model_dir, 'parameters.txt'))

        self.lstm.model = models.load_model(model_dir)
        self.start_training_and_testing.place_forget()

        """ reset all buttons """
        """ set start testing status to normal """
        self.start_testing.place(x=610, y=400)
        self.start_testing['state'] = NORMAL
        self.next_btn.place(x=690, y=400)
        self.back_btn['state'] = NORMAL
        self.load_model_btn['state'] = NORMAL
        self.title['text'] = 'Testing Page'
        self.info_data = TESTING_INFO

    def save_the_model(self):
        """this function will save the model"""
        model_saved_path = filedialog.askdirectory()
        if not model_saved_path:
            return
        bi_lstm_dir = os.path.join(model_saved_path, 'model')
        if not os.path.exists(bi_lstm_dir):
            os.makedirs(bi_lstm_dir)
        self.lstm.model.save(bi_lstm_dir)
        self.save_parameters(bi_lstm_dir)
        messagebox.showinfo(title='Model status', message='The model saved successfully')

    def set_progress_bar(self, value: float):
        """This function will set the process bar value"""
        self.bar['value'] = value

    def start_lstm_model(self):
        """This function will start two threads:
            1.will be able to update the status of training for the labels
            2.will update the process bar from the lstm mode
        """
        self.p.start()
        self.p1.start()

    def start_training_testing(self):
        """This function will create bi-lstm model and making training,testing on the model"""
        try:
            history, M, silhoutte_score = self.lstm.train_test_for_iteration(c1=self.c1_embeded, c2=self.c2_embeded, testing_data=self.testing_data_embeded)
            self.M = M
            self.history = history
            self.silhoutte_score = silhoutte_score
            # self.book_names_in_order_of_M = book_names_in_order_of_M
            self.silhouette_score_text['text'] = self.silhoutte_score
            sleep(1)
            self.process_bar.finished = True

        except SilhouetteBellowThreshold as e:
            messagebox.showwarning(title='Error of Silhouette Bellow Threshold', message=f'{str(e)}')

            self.process_bar.finished = True

            while self.p1.is_alive():
                sleep(2)
            parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
                                  testing_data_embeded=self.testing_data_embeded,
                                  tweet_length=self.lstm.parameters.tweet_length)

        except AnchorsInSameCluster as e:
            messagebox.showwarning(title='Error of AnchorsInSameCluster', message=f'{str(e)}')
            self.process_bar.finished = True

            while self.p1.is_alive():
                sleep(2)
            parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
                                  testing_data_embeded=self.testing_data_embeded,
                                  tweet_length=self.lstm.parameters.tweet_length)

    def back(self):
        """Return back to the parameters page"""
        parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
              testing_data_embeded=self.testing_data_embeded, tweet_length=self.lstm.parameters.tweet_length)

    def next(self):
        """Go next to the result page after the model finishing the training and testing"""
        ShowResultsPage.ShowResultsPage(self.parent, self.M, self.testing_data_embeded)

    def update_status(self):
        """This method will update the labels of the training page and
        process bar till the model is not finished """
        self.back_btn['state'] = DISABLED
        self.start_training_and_testing['state'] = DISABLED
        self.start_testing['state'] = DISABLED
        self.load_model_btn['state'] = DISABLED

        # to save the prev time
        prev_time = time.time()

        # while self.p.is_alive():
        while not self.process_bar.finished:
            self.set_progress_bar(value=self.process_bar.process*100)
            self.iteration_text['text'] = self.process_bar.status
            if self.estimated_time_remaining[0] >= 0:
                self.time_remaining_text['text'] = "%ds" % int(self.estimated_time_remaining[0])
                self.estimated_time_remaining[0] -= (time.time()-prev_time)
                self.estimated_time_remaining[0] = max(0, self.estimated_time_remaining[0])
                prev_time = time.time()

            if self.lstm.history:
                self.val_loss_text['text'] = self.lstm.history.history['val_loss'][-1]
                self.val_accuracy_text['text'] = self.lstm.history.history['val_accuracy'][-1]
                self.loss_text['text'] = self.lstm.history.history['loss'][-1]
                self.accuracy_text['text'] = self.lstm.history.history['accuracy'][-1]
            sleep(2)

        self.save_model['state'] = NORMAL
        self.next_btn['state'] = NORMAL
        self.back_btn['state'] = NORMAL
        self.start_testing['state'] = NORMAL
        self.time_remaining_text['text'] = "finished"

    def save_parameters(self,path):
        """This function create parameter file into the giving path"""
        with open(os.path.join(path, 'parameters.txt'), 'w') as parameters_file:
            parameters_file.write(f'Activation Function:{self.parameters.activation_function}\n')
            parameters_file.write(f'Number of Iterations:{self.parameters.number_of_iteration}\n')
            parameters_file.write(f'F1- The Under Sampling Rate:{self.parameters.undersampling_rate}\n')
            parameters_file.write(f'F2- The Multiplying Rate:{self.parameters.multiplying_rate}\n')
            parameters_file.write(f'Accuracy Threshold:{self.parameters.accuracy_threshold}\n')
            parameters_file.write(f'Silhouette Threshold:{self.parameters.silhouette_threshold}\n')
            parameters_file.write(f'Learning Rate:{self.parameters.learning_rate}\n')
            parameters_file.write(f'Number Of Epoch:{self.parameters.number_of_epoch}\n')
            parameters_file.write(f'Optimizer:{self.parameters.optimizer}\n')
            parameters_file.write(f'Drop Out:{self.parameters.drop_out}\n')
            parameters_file.write(f'Hidden State Size:{self.parameters.lstm_hidden_state_size}\n')
            parameters_file.write(f'Batch Size:{self.parameters.batch_size}\n')
            parameters_file.write(f'Fully Connected Layer:{self.parameters.fully_connect_layer}\n')
            parameters_file.write(f'Tweet Length:{self.parameters.tweet_length}\n')

    def load_parameters(self, file_path : str):
        """This function get txt file with data inside :
            Its will convert all the data inside into the parameter page
            If there an error it will give an error message
        """
        with open(file=file_path) as parameter_file:
            for line in parameter_file:
                parameter, value = line.split(':')
                parameter = str(parameter).title()
                value: str = value.strip()
                if parameter == 'Tweet Length':
                    if int(self.parameters.tweet_length) != int(value):
                        return messagebox.showwarning(title='Tweet length equality',
                                                      message=f'The current tweet length: {self.parameters.tweet_length}\n'
                                                              f'and the Tweet length of loaded model = {value}\n'
                                                              f'please provide another model')
        with open(file=file_path) as parameter_file:
            for line in parameter_file:
                parameter, value = line.split(':')
                parameter = str(parameter).title()
                value: str = value.strip()
                from GUI.App.pages.parameters_page import OPTIMZERS
                from GUI.App.pages.parameters_page import ACTIVATION_FUNCTION
                if parameter == 'Activation Function' and value in ACTIVATION_FUNCTION:
                    self.parameters.activation_function = value
                elif parameter == 'Number Of Iterations':
                    self.parameters.number_of_iteration = int(value)
                elif parameter == 'F1- The Under Sampling Rate':
                    self.parameters.undersampling_rate = int(value)
                elif parameter == 'F2- The Multiplying Rate':
                    self.parameters.multiplying_rate = int(value)
                elif parameter == 'Accuracy Threshold':
                    self.parameters.accuracy_threshold = float(value)
                elif parameter == 'Silhouette Threshold':
                    self.parameters.silhouette_threshold = float(value)
                elif parameter == 'Learning Rate':
                    self.parameters.learning_rate = float(value)
                elif parameter == 'Number Of Epoch':
                    self.parameters.number_of_epoch = int(value)
                elif parameter == 'Optimizer' and value in OPTIMZERS:
                    self.parameters.optimizer = value
                elif parameter == 'Drop Out':
                    self.parameters.drop_out = float(value)
                elif parameter == 'Hidden State Size':
                    self.parameters.lstm_hidden_state_size = int(value)
                elif parameter == 'Batch Size':
                    self.parameters.batch_size = int(value)
                elif parameter == 'Fully Connected Layer':
                    self.parameters.fully_connect_layer = int(value)
                elif parameter == 'Tweet Length':
                    self.parameters.tweet_length = int(value)
