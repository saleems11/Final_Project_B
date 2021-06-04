from tkinter import *

active_page = []

def_fg = "lightgrey"
def_bg = "#201F1E"
TRAIN_INFO = 'In this page we can see:\n' \
                             'Load existing model, this can be process \n' \
                             'if the model are exist and parameter txt file\n' \
                             'are exist and the tweet length the same tweet\n' \
                             'length' \
                             '\n\n' \
                             'Save the model will be executable if the model\n' \
                             'finished his training and testing process' \
                             '\n\n' \
                             'Info: there are 7 labels\n' \
                             'The two for accuracy and loss\n' \
                             'The other Two for validation accuracy and validation loss\n' \
                             'One estimated time to let us know how much time the model need\n' \
                             'One for iteration in which iteration the model processing\n' \
                             'One for Silhouette score will be visible after the model finishing'
PARAMETER_INFO = 'There are 3 types of input:\n' \
                             'One to check from list box\n' \
                             'One to enter integer number between the 0 and big number\n' \
                             'One to enter float number between 0 and 1 \n' \
                             'If you did entered one bad number the model will \n' \
                             'ask you if you can change this value' \
                             '\n\n' \
                             'And the last thing you can import parameter file\n' \
                             'the file show be writting like this:' \
                             'Activation Function:$value\n' \
                             'Number Of Iterations:$value....\n' \
                             'If one parameter are wrong the model will give error message'
LOAD_DATA_INFO = 'There are 3 types of selecting data:\n' \
                             '1.selecting original books directory\n' \
                             '2.selecting pseudo Al-Ghazali books directory\n' \
                             '3.selecting testing directory and after that select\n' \
                             '\tfrom the list box the wanted files[You can select just one for testing]\n'
TESTING_INFO= 'In this page you did loaded existing model\n' \
              'so here you just test the books you did selected\n' \
              'them in the load data and here you just check it'
class Page(Frame):
    def __init__(self, parent, title: str = ''):
        """creating new page with specific title"""
        self.width = 1200
        self.height = 600
        # remove old page
        try:
            active_page[0].delete()
        except:
            pass

        # create new tab
        Frame.__init__(self, parent, bg="#201F1E", height=self.height, width=self.width)

        # place page
        self.place(x=0, y=0)
        self.title = Label(self, text=title, bg='white', fg='black')
        self.info_data = ''
        if title == 'Load Data And Embedding':
            self.info_data = LOAD_DATA_INFO
        elif title == 'Train Page':
            self.info_data = TRAIN_INFO
        elif title == 'Parameters':
            self.info_data = PARAMETER_INFO
        elif title == 'Testing Page':
            self.info_data = TESTING_INFO
        else:
            self.info_data = ''
        self.title.config(font=("Courier", 30))
        self.title.place(x=100, y=20)
        self.user_info = Button(self, text="Help?", bg='blue', fg=def_fg, command=self.show_info)
        self.user_info.place(x=1100, y=30)
        active_page.append(self)

    def delete(self):
        """delete the previous page"""
        print("destroying previous tab")
        global active_page
        active_page.remove(self)
        self.destroy()

    def show_info(self):
        window = Toplevel()

        label = Label(window, text=self.info_data)
        label.pack(fill='x', padx=50, pady=5)

        button_close = Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')