import glob
import os
import threading
from time import sleep
from tkinter import Label, Button, HORIZONTAL, filedialog, Listbox, Scrollbar, messagebox, Entry
from tkinter.ttk import Progressbar
from typing import List
from models.LoadingBalancingData.DataManagement import DataManagement

from .page import Page
from .parameters_page import Param, ITERATION_MAX_NUMBER
from .process_bar import ProcessBar
TESTING: bool = False
c1_dir: str = ''
c2_dir: str = ''
c3_dir: str = ''
anchor_c1_dir: List[str] = []
anchor_c2_dir: List[str] = []
original_dir: List[str] = []
pseudo_dir: List[str] = []
test_dir:List[str] = []
process_bar: int = 0

def_bg = "#201F1E"
def_fg = "lightgrey"


class HomePage(Page):
    def __init__(self, parent, testing=False):
        self.value = None
        self.parent = None
        self.finished_embedding = False
        self.process_bar = ProcessBar()
        print("Showing Home page")
        # init page/ delete old page
        self.tweet_size = 200
        self.process = 0

        if testing:
            global c1_dir, c2_dir, c3_dir, anchor_c1_dir, anchor_c2_dir, original_dir, pseudo_dir, test_dir
            c1_dir = "C:/Users/iamme/Desktop/Books/t1"
            c2_dir = "C:/Users/iamme/Desktop/Books/t2"
            c3_dir = "C:/Users/iamme/Desktop/Books/t3"
            anchor_c1_dir = ['Al_Mankhul_min_Taliqat_al_Usul.txt']
            anchor_c2_dir = ['Kimiya_yi_Saadat.txt']
            original_dir = ['al_iqtisad_fi_al_itiqad.txt', 'Al_Mustasfa_min_ilm_al_Usul.txt', 'Fada_ih_al_Batiniyya_wa_Fada_il_al_Mustazhiriyy.txt', 'Faysal_at_Tafriqa_Bayna_al_Islam_wa_al_Zandaqa.txt', 'Iljam_Al_Awamm_an_Ilm_Al_Kalam.txt', 'Mishakat_al_Anwar.txt']
            pseudo_dir = ['al_Madnun_bihi_ala_ghayri.txt']
            test_dir = ['Tahafut_al_Falasifa.txt']

        self.p1 = threading.Thread(target=self.update_status, daemon=True)
        self.p = threading.Thread(target=self.start_embedding_process, daemon=True)
        self.c1_embeded = self.c2_embeded = self.testing_data_embeded = None
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
        self.test_btn = Button(self, text="Select Test Book", bg=def_bg, fg=def_fg, command=self.browse_test)
        self.test_btn.place(x=130, y=450)

        self.pseudo_al_ghazali_btn.place(x=130, y=420)
        self.anchor_c1_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_anchor_c1)
        self.anchor_c2_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_anchor_c2)
        self.original_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_original_btn)
        self.pseudo_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_pseudo_btn)
        self.test_x_btn = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_test_btn)

        self.next_btn = Button(self, text="Next - Training Page", bg='red', fg=def_fg, command=self.go_to)
        if anchor_c1_dir:
            self.anchor_c1_x_btn.place(x=110, y=330)
        if anchor_c2_dir:
            self.anchor_c2_x_btn.place(x=110, y=360)
        if original_dir:
            self.original_x_btn.place(x=110, y=390)
        if pseudo_dir:
            self.pseudo_x_btn.place(x=110, y=420)
        if test_dir:
            self.test_x_btn.place(x=110, y=450)
        self.bar = Progressbar(self, orient=HORIZONTAL, length=700, mode="determinate")
        self.start_embedding = Button(self, text="Start Embedding", bg='green', fg=def_fg, command=self.embedding_files)
        self.check_dir()
        """Tweet_length"""
        self.tweet_length = Label(self, text='Tweet Length', bg='RED', fg=def_fg)
        self.tweet_length.place(x=830, y=515)
        self.tweet_length_text = Entry(self, width=15)
        self.tweet_length_text.place(x=830, y=550)
        self.tweet_length_text.insert(0, '200')
        self.down_status = Label(self, text='Status', bg='RED', fg=def_fg)
        self.down_status_text = Label(self, text='Loading...', bg='RED', fg=def_fg)

    def set_progress_bar(self, value: float):
        self.bar['value'] = value

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
            self.list_size += 1
        anchor_c1_dir = []
        self.anchor_c1_btn['text'] = 'Select anchor C1'
        self.anchor_c1_x_btn.place_forget()
        self.check_dir()

    def clear_anchor_c2(self) -> None:
        global anchor_c2_dir
        for file in anchor_c2_dir:
            self.lb.insert(self.list_size, file)
            self.list_size += 1
        anchor_c2_dir = []
        self.anchor_c2_btn['text'] = 'Select anchor C2'
        self.anchor_c2_x_btn.place_forget()
        self.check_dir()

    def clear_original_btn(self) -> None:
        global original_dir
        for file in original_dir:
            self.lb.insert(self.list_size, file)
            self.list_size += 1
        original_dir = []
        self.al_ghazali_btn['text'] = 'Select Al Ghazali books'
        self.original_x_btn.place_forget()
        self.check_dir()

    def clear_pseudo_btn(self) -> None:
        global pseudo_dir
        for file in pseudo_dir:
            self.lb.insert(self.list_size, file)
            self.list_size += 1
        pseudo_dir = []
        self.pseudo_al_ghazali_btn['text'] = 'Select Pseudo Al Ghazali books'
        self.pseudo_x_btn.place_forget()
        self.check_dir()

    def clear_test_btn(self) -> None:
        global test_dir
        for file in test_dir:
            self.lb.insert(self.list_size, file)
            self.list_size += 1

        # empty the list
        test_dir = []
        self.test_btn['text'] = 'Select Test Book'
        self.test_x_btn.place_forget()
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
        if c1_dir and c2_dir and anchor_c1_dir and anchor_c2_dir and original_dir and pseudo_dir and c3_dir and test_dir:
            self.bar.place(x=100, y=550)
            self.start_embedding.place(x=950, y=550)
        else:
            self.bar.place_forget()
            self.start_embedding.place_forget()

    def get_list_of_test(self):
        global c3_dir
        try:
            c3_dir = filedialog.askdirectory()
            self.lb.delete(0, 'end')
            self.clear_anchor_c1()
            self.clear_anchor_c2()
            self.clear_original_btn()
            self.clear_pseudo_btn()

            self.lb.place(x=600, y=300)
            for file in os.listdir(path=c3_dir):
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

    def browse_test(self):
        global test_dir
        if len(self.lb.curselection()) == 0 or len(self.lb.curselection()) > 1:
            messagebox.showwarning(title='ERROR', message='Please choose 1 book for testing')
            return
        for i in self.lb.curselection():
            test_dir.append(self.lb.get(i))
        self.call_delete()
        self.test_x_btn.place(x=110, y=450)
        self.check_dir()
        print(f'test dir: {test_dir} ')

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
        self.start_embedding.place_forget()
        self.down_status.place(x=130, y=515)
        self.down_status_text.place(x=230, y=515)
        while not self.process_bar.finished:
            print(f'updated progress bar : {self.process_bar.process}')
            self.set_progress_bar(value=self.process_bar.process*100)
            self.down_status_text['text'] = self.process_bar.status
            sleep(0.5)

        self.set_progress_bar(value=self.process_bar.process * 100)
        self.down_status_text['text'] = self.process_bar.status

        self.next_btn.place(x=830, y=550)
        self.tweet_length_text.place_forget()
        self.tweet_length.place_forget()

    def start_embedding_process(self):
        print('Start embedding')
        global c1_dir, c2_dir, c3_dir, anchor_c2_dir, anchor_c1_dir
        result: List[str] = [
                             self.check_if_integer(value=self.tweet_length_text.get(), min_number=0,
                                                   max_number=ITERATION_MAX_NUMBER, msg='Batch Size')
                             ]
        check_ = [not res for res in result]
        if not all(check_):
            messagebox.showwarning(title='ERROR', message='\n'.join(result))
            return

        self.tweet_length_parameter = int(self.tweet_length_text.get())
        self.test_x_btn['state'] = 'disabled'
        self.original_x_btn['state'] = 'disabled'
        self.anchor_c1_x_btn['state'] = 'disabled'
        self.anchor_c2_x_btn['state'] = 'disabled'
        self.pseudo_x_btn['state'] = 'disabled'
        self.al_ghazali_btn['state'] = 'disabled'
        self.pseudo_al_ghazali_btn['state'] = 'disabled'
        self.anchor_c1_btn['state'] = 'disabled'
        self.anchor_c2_btn['state'] = 'disabled'
        self.test_btn['state'] = 'disabled'
        self.c3_list_btn['state'] = 'disabled'
        self.X1['state'] = 'disabled'
        self.X2['state'] = 'disabled'
        self.load_data_btn1['state'] = 'disabled'
        self.load_data_btn2['state'] = 'disabled'

        c3_test_names = test_dir
        self.embed_data = DataManagement(tweet_size=self.tweet_length_parameter, embedding_size=1024,
                                         c1_anchor_name=anchor_c1_dir, c2_anchor_name=anchor_c2_dir,
                                         c1_test_names=original_dir, c2_test_names=pseudo_dir,
                                         c3_test_names=c3_test_names, c1_dir=c1_dir, c2_dir=c2_dir, c3_dir=c3_dir)
        if not TESTING:
            c1, c2, testing_data = self.embed_data.load_data(self.process_bar)
            self.c1_embeded = c1
            self.c2_embeded = c2
            self.testing_data_embeded = testing_data
        self.process_bar.finished = True

    def go_to(self):
        Param(self.parent, self.c1_embeded, self.c2_embeded, self.testing_data_embeded, self.tweet_length_parameter)

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


def count_word_files(dir_path: str) -> int:
    return len(glob.glob1(dir_path, "*.txt"))



