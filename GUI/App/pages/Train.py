import threading
import traceback
from time import sleep
from tkinter import Label, Button, HORIZONTAL, IntVar, filedialog, messagebox, NORMAL, DISABLED
from tkinter.ttk import Progressbar

import numpy as np
import time
from PIL import Image, ImageTk

from Exceptions.Exceptions import SilhouetteBellowThreshold, AnchorsInSameCluster
from GUI.App.pages import parameters_page
from GUI.App.pages import ShowResultsPage
from GUI.App.pages.page import Page, def_fg, def_bg
from GUI.App.pages.process_bar import ProcessBar
from models.LSTM.Bi_Direct_LSTM import Bi_Direct_LSTM
from models.LSTM.Parameters import Parameters


def Sprite(picture, res1, res2):
    im = Image.open(picture).convert("RGBA").resize((res1, res2), Image.BOX)
    pic = ImageTk.PhotoImage(im)
    cor = Image.open(picture)
    print(cor.mode)
    return pic


class TrainPage(Page):
    def __init__(self, parent, parameters: Parameters, c1_embeded, c2_embeded, testing_data_embeded):
        print("Showning settings page")
        self.parameters = parameters
        self.process_bar = ProcessBar()

        # for time estimating
        self.average_iteration_time = [0.0]

        self.lstm = Bi_Direct_LSTM(parameters=self.parameters, process_bar=self.process_bar,
                                   average_iteration_time=self.average_iteration_time)

        self.p1 = threading.Thread(target=self.update_status, daemon=True)
        self.p = threading.Thread(target=self.start_training_testing, daemon=True)
        self.parent = parent
        self.c1_embeded = c1_embeded
        self.c2_embeded = c2_embeded
        self.testing_data_embeded = testing_data_embeded
        # init page/ delete old page
        Page.__init__(self, parent, title='Train Page')
        self.value = IntVar()
        self.value.set(5)
        """Status"""
        self.status = Label(self, text="Status Bar", bg=def_bg, fg=def_fg)
        self.status.place(x=100, y=100)
        """Status bar"""
        self.bar = Progressbar(self, orient=HORIZONTAL, length=700, mode="determinate")
        self.bar.place(x=200, y=100)
        """Accuracy"""
        self.accuracy = Label(self, text="Accuracy", bg=def_bg, fg=def_fg)
        self.accuracy.place(x=100, y=150)
        self.accuracy_text = Label(self, text="Loading", bg=def_bg, fg=def_fg)
        self.accuracy_text.place(x=200, y=150)
        """Loss"""
        self.loss = Label(self, text="Loss", bg=def_bg, fg=def_fg)
        self.loss.place(x=100, y=180)
        self.loss_text = Label(self, text="Loading", bg=def_bg, fg=def_fg)
        self.loss_text.place(x=200, y=180)
        """Iteration"""
        self.iteration = Label(self, text="Iteration", bg=def_bg, fg=def_fg)
        self.iteration.place(x=100, y=210)
        self.iteration_text = Label(self, text="{iteration_number}\{inumber_of_iteration}", bg=def_bg, fg=def_fg)
        self.iteration_text.place(x=200, y=210)
        """Val Accuracy"""
        self.val_accuracy = Label(self, text="Val Accuracy", bg=def_bg, fg=def_fg)
        self.val_accuracy.place(x=100, y=240)
        self.val_accuracy_text = Label(self, text="Loading", bg=def_bg, fg=def_fg)
        self.val_accuracy_text.place(x=200, y=240)
        """Val loss"""
        self.val_loss = Label(self, text="Val Loss", bg=def_bg, fg=def_fg)
        self.val_loss.place(x=100, y=270)
        self.val_loss_text = Label(self, text="Loading", bg=def_bg, fg=def_fg)
        self.val_loss_text.place(x=200, y=270)
        """silhouette_score"""
        self.silhouette_score = Label(self, text="Silhouette Score", bg=def_bg, fg=def_fg)
        self.silhouette_score.place(x=100, y=300)
        self.silhouette_score_text = Label(self, text="Loading", bg=def_bg, fg=def_fg)
        self.silhouette_score_text.place(x=200, y=300)
        """time_remaining"""
        self.time_remaining = Label(self, text="E.Time Remaining", bg=def_bg, fg=def_fg)
        self.time_remaining.place(x=100, y=330)
        self.time_remaining_text = Label(self, text="Loading", bg=def_bg, fg=def_fg)
        self.time_remaining_text.place(x=200, y=330)

        """Back"""
        self.back_btn = Button(self, text="Back", bg='red', fg=def_fg, command=self.back)
        self.back_btn.place(x=470, y=400)
        """Next"""
        self.next_btn = Button(self, text="Next", bg='green', fg=def_fg, command=self.next)
        self.next_btn.place(x=720, y=500)
        """Save Model"""
        self.save_model = Button(self, text="Save The Model", bg='blue', fg=def_fg, command=self.save_the_model)
        self.save_model.place(x=520, y=400)
        """Start Testing"""
        self.start_testing = Button(self, text="Start Training and Testing", bg='green', fg=def_fg, command=self.start_lstm_model)
        self.start_testing.place(x=620, y=400)
        if not self.process_bar.finished:
            self.save_model['state'] = DISABLED
            self.next_btn['state'] = DISABLED
            self.back_btn['state'] = DISABLED

    def save_the_model(self):
        """this function will save the model"""
        c2_dir = filedialog.askdirectory()

        self.lstm.model.save(c2_dir)

    def set_progress_bar(self, value: float):
        self.bar['value'] = value

    def start_lstm_model(self):
        self.p.start()
        self.p1.start()

    def start_training_testing(self):
        try:
            history, M, silhoutte_score, book_names_in_order_of_M = self.lstm.train_test_for_iteration(c1=self.c1_embeded, c2=self.c2_embeded, testing_data=self.testing_data_embeded)
            self.M = M
            self.history = history
            self.silhoutte_score = silhoutte_score
            self.book_names_in_order_of_M = book_names_in_order_of_M
            self.silhouette_score_text['text'] = self.silhoutte_score
            self.process_bar.finished = True

        except SilhouetteBellowThreshold as e:
            messagebox.showwarning(title='Error of Silhouette Bellow Threshold', message=f'{str(e)}')

            self.process_bar.finished = True

            while self.p1.is_alive():
                sleep(1)
            parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
                                  testing_data_embeded=self.testing_data_embeded,
                                  tweet_length=self.lstm.parameters.tweet_length)

        except AnchorsInSameCluster as e:
            messagebox.showwarning(title='Error of AnchorsInSameCluster', message=f'{str(e)}')
            self.process_bar.finished = True

            while self.p1.is_alive():
                sleep(1)
            parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
                                  testing_data_embeded=self.testing_data_embeded,
                                  tweet_length=self.lstm.parameters.tweet_length)

    def back(self):
        parameters_page.Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded,
              testing_data_embeded=self.testing_data_embeded, tweet_length=self.lstm.parameters.tweet_length)

    def next(self):
        ShowResultsPage.ShowResultsPage(self.parent, self.M, self.testing_data_embeded, self.book_names_in_order_of_M)

    def update_status(self):
        self.back_btn['state'] = DISABLED
        self.start_testing['state'] = DISABLED
        while not self.process_bar.finished:
            self.set_progress_bar(value=self.process_bar.process*100)
            # self.iteration_text['text'] = self.process_bar.status
            self.time_remaining_text['text'] = "%.2fs" % self.average_iteration_time[0]
            if self.lstm.history:
                self.val_loss_text['text'] = self.lstm.history.history['val_loss'][-1]
                self.val_accuracy_text['text'] = self.lstm.history.history['val_accuracy'][-1]
                self.loss_text['text'] = self.lstm.history.history['loss'][-1]
                self.accuracy_text['text'] = self.lstm.history.history['accuracy'][-1]
            sleep(1)

        self.save_model['state'] = NORMAL
        self.next_btn['state'] = NORMAL
        self.back_btn['state'] = NORMAL
        self.start_testing['state'] = DISABLED