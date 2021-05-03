import glob
import os
import threading
from time import sleep
from tkinter import Label, Button, HORIZONTAL, filedialog, Listbox, Scrollbar, RIGHT, BOTH
from tkinter.ttk import Progressbar
from typing import List
import Algs.Embedd_DataSet as Emb_D

from GUI.App.pages.Parameters import Parameter
from GUI.App.pages.page import Page
from models.LoadingBalancingData.DataManagement import DataManagement
from utils.doc_utils import Documents_utils
import random as rnd
import numpy as np

c1_dir: str = ''
c2_dir: str = ''
anchor_c1_dir: List[str] = []
anchor_c2_dir: List[str] = []
original_dir: List[str] = []
pseudo_dir: List[str] = []
list_test: str = ''
process_bar: int = 0
def_bg = "#201F1E"
def_fg = "lightgrey"


class HomePage(Page):
    def __init__(self, parent, root):
        self.root = root
        self.value = None
        self.parent = None
        self.finished_embedding = False
        print("Showing Home page")
        # init page/ delete old page
        self.tweet_size = 200
        self.embed_data_set = Emb_D.Embedd_DataSet()
        self.p1 = threading.Thread(target=self.update_status, daemon=True)
        self.p = threading.Thread(target=start_embedding, args=(self.embed_data_set, self.tweet_size,), daemon=True)
        Page.__init__(self, parent, title='Load Data And Embedding')
        self.scroll_bar = Scrollbar(self)
        self.lb = Listbox(self, height=10, width=60, selectmode='multiple')
        self.lb.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.lb.yview)
        self.c1 = Label(self, text="Please Select C1 directory", bg=def_bg, fg=def_fg)
        self.c1.place(x=100, y=150)
        self.load_data_btn1 = Button(self, text='Select', bg=def_bg, fg=def_fg, command=self.browse_button)
        self.load_data_btn1.place(x=130, y=170)

        self.X1 = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_c1)
        if c1_dir:
            self.X1.place(x=110, y=170)
            self.load_data_btn1['text'] = c1_dir + f' -Number of words files: {count_word_files(c1_dir)}'

        self.c2 = Label(self, text="Please Select C2 directory", bg=def_bg, fg=def_fg)
        self.c2.place(x=100, y=200)
        self.load_data_btn2 = Button(self, text="Select", bg=def_bg, fg=def_fg, command=self.browse_button2)
        self.load_data_btn2.place(x=130, y=220)

        self.X2 = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_c2)
        if c2_dir:
            self.X2.place(x=110, y=220)
            self.load_data_btn2['text'] = c2_dir + f' -Number of words files: {count_word_files(c2_dir)}'

        self.c3 = Label(self, text="Please Select Test directory", bg=def_bg, fg=def_fg)
        self.c3.place(x=100, y=260)

        self.progress_bar_level: int = 0
        self.list_size = 0
        self.c3_list_btn = Button(self, text="Select C3 directory", bg='red', fg=def_fg, command=self.get_list_of_test)
        self.c3_list_btn.place(x=130, y=300)
        self.anchor_c1_btn = Button(self, text="Select anchor C1", bg=def_bg, fg=def_fg, command=self.browse_anchor_c1)
        self.anchor_c1_btn.place(x=130, y=330)
        self.anchor_c2_btn = Button(self, text="Select anchor C2", bg=def_bg, fg=def_fg, command=self.browse_anchor_c2)
        self.anchor_c2_btn.place(x=130, y=360)
        self.al_ghazali_btn = Button(self, text="Select Al Ghazali books", bg=def_bg, fg=def_fg,
                                     command=self.browse_original)
        self.al_ghazali_btn.place(x=130, y=390)
        self.pseudo_al_ghazali_btn = Button(self, text="Select Pseudo Al Ghazali books", bg=def_bg, fg=def_fg,
                                            command=self.browse_pseudo)
        self.pseudo_al_ghazali_btn.place(x=130, y=420)

        self.anchor_c1_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_anchor_c1)
        self.anchor_c2_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_anchor_c2)
        self.original_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_original_btn)
        self.pseudo_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_pseudo_btn)

        if anchor_c1_dir:
            self.anchor_c1_x_btn.place(x=110, y=330)
        if anchor_c2_dir:
            self.anchor_c2_x_btn.place(x=110, y=360)
        if original_dir:
            self.original_x_btn.place(x=110, y=390)
        if pseudo_dir:
            self.pseudo_x_btn.place(x=110, y=420)
        self.bar = Progressbar(self, orient=HORIZONTAL, length=700, mode="determinate")
        self.start_embedding = Button(self, text="Start Embedding", bg='green', fg=def_fg, command=self.embedding_files)
        self.check_dir()

    def set_progress_bar(self, value: int):
        self.bar['value'] = value*700

    def back(self):
        Parameter(self.parent)

    def clear_c1(self) -> None:
        global c1_dir
        c1_dir = ''
        self.load_data_btn1['text'] = 'Select'
        self.X1.place_forget()
        self.check_dir()

    def clear_c2(self) -> None:
        global c2_dir
        c2_dir = ''
        self.load_data_btn2['text'] = 'Select'
        self.X2.place_forget()
        self.check_dir()

    def clear_anchor_c1(self) -> None:
        global anchor_c1_dir
        for file in anchor_c1_dir:
            self.lb.insert(self.list_size, file)
            self.list_size = self.list_size + 1
        anchor_c1_dir = []
        self.anchor_c1_btn['text'] = 'Select anchor C1'
        self.anchor_c1_x_btn.place_forget()
        self.check_dir()

    def clear_anchor_c2(self) -> None:
        global anchor_c2_dir
        for file in anchor_c2_dir:
            self.lb.insert(self.list_size, file)
            self.list_size = self.list_size + 1
        anchor_c2_dir = []
        self.anchor_c2_btn['text'] = 'Select anchor C2'
        self.anchor_c2_x_btn.place_forget()
        self.check_dir()

    def clear_original_btn(self) -> None:
        global original_dir
        for file in original_dir:
            self.lb.insert(self.list_size, file)
            self.list_size = self.list_size + 1
        original_dir = []
        self.al_ghazali_btn['text'] = 'Select Al Ghazali books'
        self.original_x_btn.place_forget()
        self.check_dir()

    def clear_pseudo_btn(self) -> None:
        global pseudo_dir
        for file in pseudo_dir:
            self.lb.insert(self.list_size, file)
            self.list_size = self.list_size + 1
        pseudo_dir = []
        self.pseudo_al_ghazali_btn['text'] = 'Select Pseudo Al Ghazali books'
        self.pseudo_x_btn.place_forget()
        self.check_dir()

    def browse_button(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c1_dir
        c1_dir = filedialog.askdirectory()
        self.load_data_btn1['text'] = c1_dir + f' -Number of words files: {count_word_files(c1_dir)}'
        self.X1.place(x=110, y=170)
        self.check_dir()
        print(f'C1: {c1_dir}')

    def browse_button2(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c2_dir
        c2_dir = filedialog.askdirectory()
        self.load_data_btn2['text'] = c2_dir + f' -Number of words files: {count_word_files(c2_dir)}'
        self.X2.place(x=110, y=220)
        self.check_dir()
        print(f'C2: {c2_dir} ')

    def check_dir(self):
        if c1_dir and c2_dir and anchor_c1_dir and anchor_c2_dir and original_dir and pseudo_dir:
            self.bar.place(x=100, y=550)
            self.start_embedding.place(x=150, y=550)
        else:
            self.bar.place_forget()
            self.start_embedding.place_forget()

    def get_list_of_test(self):
        global list_test
        try:
            list_test = filedialog.askdirectory()
            if not list_test:
                self.lb.delete(0, 'end')

            self.clear_anchor_c1()
            self.clear_anchor_c2()
            self.clear_original_btn()
            self.clear_pseudo_btn()

            self.lb.place(x=600, y=300)
            for file in os.listdir(path=list_test):
                if file.endswith('.txt'):
                    _, tail = os.path.split(file)
                    self.lb.insert(self.list_size, tail)
                    self.list_size = self.list_size + 1
        except FileNotFoundError as filenotfound:
            print(f'something went wrong with getting c3 folder : {filenotfound.strerror}')

    def browse_anchor_c1(self):
        global anchor_c1_dir
        if not len(self.lb.curselection()) > 0:
            return
        for i in self.lb.curselection():
            anchor_c1_dir.append(self.lb.get(i))
        self.call_delete()
        self.anchor_c1_x_btn.place(x=110, y=330)
        self.check_dir()
        print(f'anchor c1 dir: {anchor_c1_dir} ')

    def browse_anchor_c2(self):
        global anchor_c2_dir
        if not len(self.lb.curselection()) > 0:
            return
        for i in self.lb.curselection():
            anchor_c2_dir.append(self.lb.get(i))
        self.call_delete()
        self.anchor_c2_x_btn.place(x=110, y=360)
        self.check_dir()
        print(f'anchor c2 dir: {anchor_c2_dir} ')

    def browse_original(self):
        global original_dir
        if not len(self.lb.curselection()) > 0:
            return
        for i in self.lb.curselection():
            original_dir.append(self.lb.get(i))
        self.call_delete()
        self.original_x_btn.place(x=110, y=390)
        self.check_dir()
        print(f'original dir: {original_dir} ')

    def browse_pseudo(self):
        global pseudo_dir
        if not len(self.lb.curselection()) > 0:
            return
        for i in self.lb.curselection():
            pseudo_dir.append(self.lb.get(i))
        self.call_delete()
        self.pseudo_x_btn.place(x=110, y=420)
        self.check_dir()
        print(f'pseudo dir: {pseudo_dir} ')

    def embedding_files(self) -> None:
        global progress_bar_level

        self.p.start()
        self.p1.start()

    def call_delete(self):
        selection = self.lb.curselection()
        for i in reversed(selection):
            self.lb.delete(i)
            self.list_size = self.list_size - 1

    def update_status(self):
        while not self.embed_data_set.finished:
            print(f'updated progress bar : {self.embed_data_set.process}')
            self.set_progress_bar(value=self.embed_data_set.process * 700)
            sleep(0.2)
        # self.next_btn.place(x=blabla, youblabla)

def count_word_files(dir_path: str) -> int:
    return len(glob.glob1(dir_path, "*.txt"))

def start_embedding(embed_data_set: Emb_D.Embedd_DataSet, tweet_size: int) :
    print('Start embedding')
    global process_bar
    c1 = Documents_utils.get_list_of_books(c1_dir)
    c1 = c1[:min(1000, len(c1))]
    c2 = Documents_utils.get_list_of_books(c2_dir)
    c2 = c2[:min(1000, len(c2))]
    c3 = Documents_utils.get_list_of_books(list_test)
    c3 = [c3[rnd.randint(0, len(c3) - 1)]]

    c1, c2, anchor_c1, anchor_c2 = DataManagement.manage_anchor_data(c1, c2, 7, 2)

    embedded_anchor_c1 = []
    embedded_anchor_c2 = []
    embedded_data_c3 = []
    embedded_data_c1 = embed_data_set.embedd_Elmo(books=c1, tweet_size=tweet_size)

    embedded_data_c2 = embed_data_set.embedd_Elmo(books=c2, tweet_size=tweet_size)

    for i in range(0, len(c3)):
        embedded_data_c3.append(
            embed_data_set.embedd_Elmo(books=np.array([c3[i], ]), tweet_size=tweet_size))
    for i in range(len(anchor_c1)):
        embedded_anchor_c1.append(
            embed_data_set.embedd_Elmo(books=np.array([anchor_c1[i], ]), tweet_size=tweet_size))

    for i in range(len(anchor_c2)):
        embedded_anchor_c2.append(
            embed_data_set.embedd_Elmo(books=np.array([anchor_c2[i], ]), tweet_size=tweet_size))
    embed_data_set.finished = True