from tkinter import Label, Button, filedialog, StringVar, HORIZONTAL, IntVar
from tkinter.ttk import Combobox, Entry, Progressbar

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

OPTIMZERS = [
    "SGD",
    "Nesterov accelerated gradient",
    "Adagrad",
    "AdaDelta",
    "RMSProp",
    "Adam"
]



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


    def clear_c1(self) -> None:
        global c1_dir
        c1_dir = ''
        self.load_data_btn1['text'] = 'Select'
        self.X1.place_forget()

    def clear_c2(self) -> None:
        global c2_dir
        c2_dir = ''
        self.load_data_btn2['text'] = 'Select'
        self.X2.place_forget()

    def clear_c3(self) -> None:
        global c3_dir
        c3_dir = ''
        self.load_data_btn3['text'] = 'Select'
        self.X3.place_forget()

    def browse_button(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c1_dir
        c1_dir = filedialog.askdirectory()
        self.load_data_btn1['text'] = c1_dir
        self.X1.place(x=110, y=170)
        print(f'C1: {c1_dir}')

    def browse_button2(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c2_dir
        c2_dir = filedialog.askdirectory()
        self.load_data_btn2['text'] = c2_dir
        self.X2.place(x=110, y=220)
        print(f'C2: {c2_dir} ')

    def browse_button3(self) -> None:
        # Allow user to select a directory and store it in global var
        # called folder_path
        global c3_dir
        c3_dir = filedialog.askdirectory()
        self.load_data_btn3['text'] = c3_dir
        self.X3.place(x=110, y=270)
        print(f'C3: {c3_dir}')


class Parameter(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.parent = parent
        global c1_dir, c2_dir, c3_dir
        if not c1_dir or not c2_dir or not c3_dir:

            HomePage(parent)
        else:
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
            self.f1_sampling = Label(self, text='F1- the undersampling rate', bg=def_bg, fg=def_fg)
            self.f1_sampling.place(x=50, y=160)
            self.f1_sampling_text = Entry(self, width=15)
            self.f1_sampling_text.place(x=250, y=160)
            """F- the multiplying rate"""
            self.f_multiplying = Label(self, text='F- the multiplying rate', bg=def_bg, fg=def_fg)
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
            self.optimzer_func.place(x=550, y=190)
            self.optimzer_func.current(0)
            """Pooling Size"""
            self.pooling_size = Label(self, text='Pooling Size', bg=def_bg, fg=def_fg)
            self.pooling_size.place(x=400, y=220)
            self.pooling_size_text = Entry(self, width=15)
            self.pooling_size_text.place(x=550, y=220)
            """L0- Bach size"""
            self.batch_size = Label(self, text='L0 Batch Size', bg=def_bg, fg=def_fg)
            self.batch_size.place(x=400, y=250)
            self.batch_size_text = Entry(self, width=15)
            self.batch_size_text.place(x=550, y=250)
            """L- training sequence length(tweet)"""
            self.training_seq_length = Label(self, text='Training Sequence Length', bg=def_bg, fg=def_fg)
            self.training_seq_length.place(x=400, y=280)
            self.training_seq_length_text = Entry(self, width=15)
            self.training_seq_length_text.place(x=550, y=280)
            """Buttons"""
            self.back = Button(self, text="Back", bg='red', fg=def_fg, command=self.back)
            self.back.place(x=450, y=400)
            self.add_existing_model = Button(self, text="Add Existing Model", bg='blue', fg=def_fg)
            self.add_existing_model.place(x=490, y=400)
            self.add_parameters = Button(self, text="Add Existing Parameters", bg='blue', fg=def_fg)
            self.add_parameters.place(x=610, y=400)
            self.start_training = Button(self, text="Start Training", bg='green', fg=def_fg)
            self.start_training.place(x=760, y=400)

    def back(self):
        HomePage(self.parent)

class TrainPage(Page):
    def __init__(self, parent):
        print("Showning settings page")
        self.parent = parent
        # init page/ delete old page
        Page.__init__(self, parent)
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
        """Iteration"""
        self.iteration = Label(self, text="Iteration", bg=def_bg, fg=def_fg)
        self.iteration.place(x=100, y=180)
        self.iteration_text = Label(self, text="{iteration_number}\{inumber_of_iteration}", bg=def_bg, fg=def_fg)
        self.iteration_text.place(x=200, y=180)
        """Loss"""
        self.loss = Label(self, text="Loss", bg=def_bg, fg=def_fg)
        self.loss.place(x=100, y=210)
        self.loss_text = Label(self, text="%", bg=def_bg, fg=def_fg)
        self.loss_text.place(x=200, y=210)
        """Max Accuracy"""
        self.max_accuracy = Label(self, text="Max Accuracy", bg=def_bg, fg=def_fg)
        self.max_accuracy.place(x=100, y=240)
        self.max_accuracy_text = Label(self, text="%", bg=def_bg, fg=def_fg)
        self.max_accuracy_text.place(x=200, y=240)
        """Back"""
        self.back = Button(self, text="Back", bg='red', fg=def_fg, command=self.back)
        self.back.place(x=450, y=400)
        """Save Model"""
        self.save_model = Button(self, text="Save The Model", bg='blue', fg=def_fg)
        self.save_model.place(x=490, y=400)
        """Start Testing"""
        self.start_testing = Button(self, text="Start Testing", bg='green', fg=def_fg)
        self.start_testing.place(x=590, y=400)

    def start_progress_bar(self):
        self.bar.start()
        self.bar.step(10)

    def increment(self):
        self.value.set(self.value.get() + 5)

    def back(self):
        Parameter(self.parent)

class TestPage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        print("Showning test page")
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
        """Iteration"""
        self.iteration = Label(self, text="Iteration", bg=def_bg, fg=def_fg)
        self.iteration.place(x=100, y=180)
        self.iteration_text = Label(self, text="{iteration_number}\{inumber_of_iteration}", bg=def_bg, fg=def_fg)
        self.iteration_text.place(x=200, y=180)
        """Loss"""
        self.loss = Label(self, text="Loss", bg=def_bg, fg=def_fg)
        self.loss.place(x=100, y=210)
        self.loss_text = Label(self, text="%", bg=def_bg, fg=def_fg)
        self.loss_text.place(x=200, y=210)
        """Max Accuracy"""
        self.max_accuracy = Label(self, text="Max Accuracy", bg=def_bg, fg=def_fg)
        self.max_accuracy.place(x=100, y=240)
        self.max_accuracy_text = Label(self, text="%", bg=def_bg, fg=def_fg)
        self.max_accuracy_text.place(x=200, y=240)
        """Back"""
        self.back = Button(self, text="Back", bg='red', fg=def_fg)
        self.back.place(x=450, y=400)
        """Save Model"""
        self.save_model = Button(self, text="Show Graph", bg='orange', fg=def_fg)
        self.save_model.place(x=490, y=400)


    def start_progress_bar(self):
        self.bar.start()
        self.bar.step(10)

    def increment(self):
        self.value.set(self.value.get() + 5)

class ResultPage(Page):
    def __init__(self, parent):
        print("Showning test page")

        # init page/ delete old page
        Page.__init__(self, parent)

        t = Button(self, text="Result", bg=def_bg, fg=def_fg)
        t.place(x=100, y=100)



