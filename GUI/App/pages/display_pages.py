from tkinter import Label, Button, filedialog, StringVar
from tkinter.ttk import Combobox, Entry

from PIL import Image, ImageTk

from GUI.App.pages.page import Page

c1_dir: str = ''
c2_dir: str = ''
c3_dir: str = ''
OPTIONS = [
    "Jan",
    "Feb",
    "Mar"
]  # etc


def get_c1():
    global c1_dir
    return str(c1_dir) if c1_dir else ''


def get_c2():
    global c2_dir
    return str(c2_dir) if c2_dir else ''


def get_c3():
    global c3_dir
    return str(c3_dir) if c3_dir else ''


def Sprite(picture, res1, res2):
    im = Image.open(picture).convert("RGBA").resize((res1, res2), Image.BOX)
    pic = ImageTk.PhotoImage(im)
    cor = Image.open(picture)
    print(cor.mode)
    return pic


"""
defualt widget color:
#201F1E
"""
def_bg = "#201F1E"
def_fg = "lightgrey"


class HomePage(Page):
    def __init__(self, parent):
        print("Showing Home page")
        # init page/ delete old page
        Page.__init__(self, parent)

        t = Label(self, text="Please Select C1 directory", bg=def_bg, fg=def_fg)
        t.place(x=100, y=150)
        load_data_btn1 = Button(self, text='Select', bg=def_bg, fg=def_fg, command=browse_button)
        load_data_btn1.place(x=130, y=170)

        t1 = Label(self, text="Please Select C2 directory", bg=def_bg, fg=def_fg)
        t1.place(x=100, y=200)
        load_data_btn2 = Button(self, text="Select", bg=def_bg, fg=def_fg, command=browse_button2)
        load_data_btn2.place(x=130, y=220)

        t1 = Label(self, text="Please Select C3 directory", bg=def_bg, fg=def_fg)
        t1.place(x=100, y=250)
        load_data_btn3 = Button(self, text="Select", bg=def_bg, fg=def_fg, command=browse_button3)
        load_data_btn3.place(x=130, y=270)


class Parameter(Page):
    def __init__(self, parent):
        # print("Showning settings page")
        # global c1_dir, c2_dir, c3_dir
        # if not c1_dir or not c2_dir or not c3_dir:
        #     HomePage(parent)
        # else:
        # # init page/ delete old page
        Page.__init__(self, parent)
        """ Activation_Function """
        activation_function = Label(self, text="Activation Function", bg=def_bg, fg=def_fg)
        activation_function.place(x=50, y=100)
        n = StringVar()
        monthchoosen = Combobox(parent, width=15, textvariable=n)
        monthchoosen['values'] = (' Sigmoid',
                                  ' RElu')
        monthchoosen.place(x=250, y=100)
        monthchoosen.current(0)
        """Number Of Iterations"""
        number_of_iterations = Label(self, text='Number Of Iterations', bg=def_bg, fg=def_fg)
        number_of_iterations.place(x=50, y=130)
        number_of_iterations_text = Entry(self, width=15)
        number_of_iterations_text.place(x=250, y=130)

        """F1- the undersampling rate"""
        f1_sampling = Label(self, text='F1- the undersampling rate', bg=def_bg, fg=def_fg)
        f1_sampling.place(x=50, y=160)
        f1_sampling_text = Entry(self, width=15)
        f1_sampling_text.place(x=250, y=160)
        """F- the multiplying rate"""
        f_multiplying = Label(self, text='F- the multiplying rate', bg=def_bg, fg=def_fg)
        f_multiplying.place(x=50, y=190)
        f_multiplying_text = Entry(self, width=15)
        f_multiplying_text.place(x=250, y=190)
        """Accuracy threshold"""
        accuracy_threshold = Label(self, text='Accuracy threshold', bg=def_bg, fg=def_fg)
        accuracy_threshold.place(x=50, y=220)
        accuracy_threshold_text = Entry(self, width=15)
        accuracy_threshold_text.place(x=250, y=220)
        """Silhouette threshold"""
        silhouette_threshold = Label(self, text='Silhouette threshold', bg=def_bg, fg=def_fg)
        silhouette_threshold.place(x=50, y=250)
        silhouette_threshold_text = Entry(self, width=15)
        silhouette_threshold_text.place(x=250, y=250)
        """Learning Rate"""
        learning_rate = Label(self, text='Learning Rate', bg=def_bg, fg=def_fg)
        learning_rate.place(x=50, y=280)
        learning_rate_text = Entry(self, width=15)
        learning_rate_text.place(x=250, y=280)
        """Number of epoch"""
        number_of_epoch = Label(self, text='Number of epoch', bg=def_bg, fg=def_fg)
        number_of_epoch.place(x=400, y=100)
        number_of_epoch_text = Entry(self, width=15)
        number_of_epoch_text.place(x=550, y=100)
class TrainPage(Page):
    def __init__(self, parent):
        print("Showning settings page")

        # init page/ delete old page
        Page.__init__(self, parent)

        t = Label(self, text="Einstellungen", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)


class TestPage(Page):
    def __init__(self, parent):
        print("Showning test page")

        # init page/ delete old page
        Page.__init__(self, parent)

        t = Button(self, text="Test", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)


class ResultPage(Page):
    def __init__(self, parent):
        print("Showning test page")

        # init page/ delete old page
        Page.__init__(self, parent)

        t = Button(self, text="Result", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)


def browse_button() -> None:
    # Allow user to select a directory and store it in global var
    # called folder_path
    global c1_dir
    c1_dir = filedialog.askdirectory()
    print(f'C1: {c1_dir}')


def browse_button2() -> None:
    # Allow user to select a directory and store it in global var
    # called folder_path
    global c2_dir
    c2_dir = filedialog.askdirectory()
    print(f'C2: {c2_dir} ')


def browse_button3() -> None:
    # Allow user to select a directory and store it in global var
    # called folder_path
    global c3_dir
    c3_dir = filedialog.askdirectory()
    print(f'C3: {c3_dir}')
