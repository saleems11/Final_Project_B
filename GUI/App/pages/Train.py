from tkinter import Label, Button, HORIZONTAL, IntVar
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk

from GUI.App.pages.page import Page, def_fg, def_bg
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
        self.parent = parent
        self.parameters = parameters
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
        self.accuracy_text = Label(self, text="0%", bg=def_bg, fg=def_fg)
        self.accuracy_text.place(x=200, y=150)
        """Loss"""
        self.loss = Label(self, text="Loss", bg=def_bg, fg=def_fg)
        self.loss.place(x=100, y=180)
        self.loss_text = Label(self, text="%", bg=def_bg, fg=def_fg)
        self.loss_text.place(x=200, y=180)
        """Iteration"""
        self.iteration = Label(self, text="Iteration", bg=def_bg, fg=def_fg)
        self.iteration.place(x=100, y=210)
        self.iteration_text = Label(self, text="{iteration_number}\{inumber_of_iteration}", bg=def_bg, fg=def_fg)
        self.iteration_text.place(x=200, y=210)
        """Val Accuracy"""
        self.val_accuracy = Label(self, text="Val Accuracy", bg=def_bg, fg=def_fg)
        self.val_accuracy.place(x=100, y=240)
        self.val_accuracy_text = Label(self, text="%", bg=def_bg, fg=def_fg)
        self.val_accuracy_text.place(x=200, y=240)
        """Val loss"""
        self.val_loss = Label(self, text="Val Loss", bg=def_bg, fg=def_fg)
        self.val_loss.place(x=100, y=270)
        self.val_loss_text = Label(self, text="%", bg=def_bg, fg=def_fg)
        self.val_loss_text.place(x=200, y=270)
        """Back"""
        self.back = Button(self, text="Back", bg='red', fg=def_fg, command=self.back)
        self.back.place(x=450, y=400)
        """Save Model"""
        self.save_model = Button(self, text="Save The Model", bg='blue', fg=def_fg)
        self.save_model.place(x=490, y=400)
        """Start Testing"""
        self.start_testing = Button(self, text="Start Testing", bg='green', fg=def_fg)
        self.start_testing.place(x=590, y=400)

    def set_progress_bar(self, value: int):
        self.value.set(value=value)

    def back(self):
        # Param(self.parent, c1_embeded=self.c1_embeded, c2_embeded=self.c2_embeded, testing_data_embeded=self.testing_data_embeded)
        pass

    def set_iteration(self, current_iteration: int):
        self.iteration_text['text']= f'{current_iteration} / {self.parameters.number_of_iteration}'
