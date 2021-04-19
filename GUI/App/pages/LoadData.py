from tkinter import Label, Button, HORIZONTAL, filedialog
from tkinter.ttk import Progressbar

from GUI.App.pages.Parameters import Parameter
from GUI.App.pages.page import Page
from GUI.App.sidebar import side_bar_tab_list

c1_dir: str = ''
c2_dir: str = ''
c3_dir: str = ''

def_bg = "#201F1E"
def_fg = "lightgrey"

class HomePage(Page):
    def __init__(self, parent):
        self.value = None
        self.parent = None
        print("Showing Home page")
        # init page/ delete old page
        Page.__init__(self, parent, title='Load Data And Embedding')

        self.c1 = Label(self, text="Please Select C1 directory", bg=def_bg, fg=def_fg)
        self.c1.place(x=100, y=150)
        self.load_data_btn1 = Button(self, text='Select', bg=def_bg, fg=def_fg, command=self.browse_button)
        self.load_data_btn1.place(x=130, y=170)

        self.X1 = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_c1)
        if c1_dir:
            self.X1.place(x=110, y=170)
            self.load_data_btn1['text'] = c1_dir

        self.c2 = Label(self, text="Please Select C2 directory", bg=def_bg, fg=def_fg)
        self.c2.place(x=100, y=200)
        self.load_data_btn2 = Button(self, text="Select", bg=def_bg, fg=def_fg, command=self.browse_button2)
        self.load_data_btn2.place(x=130, y=220)

        self.X2 = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_c2)
        if c2_dir:
            self.X2.place(x=110, y=220)
            self.load_data_btn2['text'] = c2_dir

        self.c3 = Label(self, text="Please Select C3 directory", bg=def_bg, fg=def_fg)
        self.c3.place(x=100, y=250)
        self.load_data_btn3 = Button(self, text="Select", bg=def_bg, fg=def_fg, command=self.browse_button3)
        self.load_data_btn3.place(x=130, y=270)

        self.X3 = Button(self, text="X", bg='red', fg=def_fg, command=self.clear_c3)
        if c3_dir:
            self.X3.place(x=110, y=270)
            self.load_data_btn3['text'] = c3_dir
        self.bar = Progressbar(self, orient=HORIZONTAL, length=700, mode="determinate")
        self.start_embedding = Button(self, text="Start Embedding", bg='green', fg=def_fg, command=self.clear_c3)
        self.check_dir()

    def set_progress_bar(self, value: int):
        self.value.set(value=value)

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


    def clear_c3(self) -> None:
        global c3_dir
        c3_dir = ''
        self.load_data_btn3['text'] = 'Select'
        self.X3.place_forget()
        self.check_dir()


    def browse_button(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c1_dir
        c1_dir = filedialog.askdirectory()
        self.load_data_btn1['text'] = c1_dir
        self.X1.place(x=110, y=170)
        self.check_dir()
        print(f'C1: {c1_dir}')

    def browse_button2(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c2_dir
        c2_dir = filedialog.askdirectory()
        self.load_data_btn2['text'] = c2_dir
        self.X2.place(x=110, y=220)
        self.check_dir()
        print(f'C2: {c2_dir} ')

    def browse_button3(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c3_dir
        c3_dir = filedialog.askdirectory()
        self.load_data_btn3['text'] = c3_dir
        self.X3.place(x=110, y=270)
        self.check_dir()
        print(f'C3: {c3_dir}')

    def check_dir(self):
        if c1_dir and c2_dir and c3_dir:
            self.bar.place(x=100, y=400)
            self.start_embedding.place(x=100, y=500)
        else:
            self.bar.place_forget()
            self.start_embedding.place_forget()


