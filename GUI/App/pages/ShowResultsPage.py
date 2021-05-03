from tkinter import Frame
from GUI.App.pages.Pages_parameters import Pages_parameters
from GUI.App.pages.page import Page
from tkinter import Button

import tkinter as tk


class ShowResultsPage(Page):
    def __init__(self, parent_frame):
        # init page/ delete old page
        Page.__init__(self, parent_frame)

        self.pages_types = ['heat_map', 'error_bar', 'chunks_labels', 'histogram']
        self.current_page = ''

        # split the GUi to three parts vertically
        self.top_frame = Frame(parent_frame)
        self.top_frame.grid(row=0, column=0, sticky="nswe")

        self.mid_frame = Frame(parent_frame)
        self.mid_frame.grid(row=1, column=0, sticky="nswe")

        self.bottom_frame = Frame(parent_frame)
        self.bottom_frame.grid(row=2, column=0, sticky="nswe")

        # add GUI parts

        # top frame parameters init
        self.top_frame_prev_pressed_Btn = None
        self.heat_map_show_Btn = None
        self.error_bar_show_Btn = None
        self.chunks_labels_show_Btn = None
        self.histogram_show_Btn = None
        self.init_top_frame()

        # bottom frame parameters init
        self.finish_Btn = None
        self.init_bottom_frame()

    ''' Initializing the Main frame sections'''

    def init_top_frame(self):
        self.heat_map_show_Btn = \
            Button(self.top_frame, text="Heat Map", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_heat_map_show_Btn)
        self.error_bar_show_Btn = \
            Button(self.top_frame, text="Error Bar", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_error_bar_show_Btn)
        self.chunks_labels_show_Btn = \
            Button(self.top_frame, text="Chunks Labels", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_chunks_labels_show_Btn)
        self.histogram_show_Btn = \
            Button(self.top_frame, text="Histogram", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_histogram_show_Btn)

        self.heat_map_show_Btn.grid(row=0, column=0, padx=10, pady=10)
        self.error_bar_show_Btn.grid(row=0, column=1, padx=10, pady=10)
        self.chunks_labels_show_Btn.grid(row=0, column=2, padx=10, pady=10)
        self.histogram_show_Btn.grid(row=0, column=3, padx=10, pady=10)

    def init_mid_frame(self):
        pass

    def init_bottom_frame(self):
        self.finish_Btn = \
            Button(self.bottom_frame, text="Finish", bg=Pages_parameters.def_bg,
                   fg=Pages_parameters.def_fg, command=self.clicked_on_finish_Btn)
        self.finish_Btn.pack(padx=10, pady=10, side=tk.RIGHT)

    ''' Click management '''

    def clicked_on_heat_map_show_Btn(self):
        self.switch_top_frame_clicked_button(self.heat_map_show_Btn)
        pass

    def clicked_on_error_bar_show_Btn(self):
        self.switch_top_frame_clicked_button(self.error_bar_show_Btn)
        pass

    def clicked_on_chunks_labels_show_Btn(self):
        self.switch_top_frame_clicked_button(self.chunks_labels_show_Btn)
        pass

    def clicked_on_histogram_show_Btn(self):
        self.switch_top_frame_clicked_button(self.histogram_show_Btn)
        pass

    def clicked_on_finish_Btn(self):
        print("Still not Implemented")
        pass

    """ Logic's Handling """

    def switch_top_frame_clicked_button(self, cur_button):
        # reset the prev button

        if self.top_frame_prev_pressed_Btn != None:
            # reset
            self.top_frame_prev_pressed_Btn["state"] = tk.NORMAL

        cur_button["state"] = tk.DISABLED
        self.top_frame_prev_pressed_Btn = cur_button

