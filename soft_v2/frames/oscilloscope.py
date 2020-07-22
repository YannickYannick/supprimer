#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:40:24 2020

tk frames and tk subframes related to the oscilloscope for the repeated flash 
experiment GUI

@author: melinapannier
"""


import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from communication.pico9000 import CommunicationPicoscope


import numpy as np


class Oscilloscope(ttk.Frame):
    def __init__(self, container, main_frame, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((1), weight=1)
        self.columnconfigure((0), weight=1)
    
        self.main_frame = main_frame
        self.update_val  = 0
        
        self.title_label = ttk.Label(self, 
                                     text="OSCILLOSCOPE CONTROL",
                                     style="Title.TLabel"
                                     )
        self.title_label.grid(row=0, column=0, sticky="W")
        
        
        sub_container = ttk.Frame(self,
                                   padding=10,
                                   style='Frame.TFrame'
                                   )
        sub_container.grid(row=1, column=0, sticky="NSEW")       
        sub_container.rowconfigure((0), weight=1)
        sub_container.columnconfigure((0,1), weight=1)
        
        
        left_container = LeftContainer(sub_container)
        left_container.grid(row=0, column=0)
        
        
        right_container = RightContainer(sub_container, self)
        right_container.grid(row=0, column=1)

        
        for child in sub_container.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky="NSEW")
            child["style"]='Frame.TFrame'
            #child["padding"]=10
        

        
class LeftContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        
        # fig = Figure(figsize=(3, 2), dpi=100)
        # t = np.arange(0, 3, .01)
        # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        
        # canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        # canvas.draw()
        # canvas.get_tk_widget().grid(row=0, column=0, sticky="NSEW")
        
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas.get_tk_widget().grid(row=0, column=0, sticky="NSEW")
        
        # plot_container = ttk.Frame(self)
        # plot_container.grid(row=0, column=0,
        #                     sticky="NSEW"
        #                     )
        
        
class RightContainer(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        
        self.controller = controller
        
        
        dialogue_box_container= ttk.LabelFrame(self, 
                                               padding=10, 
                                               text="Dialogue Box",
                                               style="Label.TLabelframe"
                                               )
        dialogue_box_container.grid(row=0, column=0,
                                    sticky="NSEW"
                                    )        
        dialogue_value = tk.StringVar()
        dialogue_box = ttk.Label(dialogue_box_container, 
                                 textvariable=dialogue_value,
                                 style="Label.TLabel"
                                 )
        dialogue_box.grid(row=0, column=0)
        
        
        oscilloscope_selection = tk.StringVar()
        oscillo1 = ttk.Radiobutton(
            self, 
            text="Picoscope 1 (2204A)", 
            variable=oscilloscope_selection, 
            value="pico1",
            style="Radiobutton.TRadiobutton"
        )
        oscillo1.grid(column=0, row=1, sticky="NESW")
        
        oscillo2 = ttk.Radiobutton(
            self, 
            text="Picoscope 2 (9000)", 
            variable=oscilloscope_selection, 
            value="pico2",
            style="Radiobutton.TRadiobutton"
        )
        oscillo2.grid(column=0, row=2, sticky="NESW")
        
        
        
        spinbox_container= ttk.Frame(self, padding=10, 
                                     style="Frame.TFrame")
        spinbox_container.grid(row=3, column=0, sticky="NESW")
        spinbox_container.rowconfigure((0,1,2,3), weight=1)
        spinbox_container.columnconfigure((0,1), weight=1)
        
        
        time_scale_label = ttk.Label(spinbox_container, text="Time Scale", 
                                     style="Label.TLabel")
        time_scale_label.grid(column=0, row=0, sticky="NESW")
               
        self.time_scale_value = tk.StringVar()
        time_scale_input = ttk.Spinbox(
            spinbox_container,
            from_=0,
            to=120,
            increment=1,
            justify="center",
            textvariable=self.time_scale_value,
            width=10,
        )
        time_scale_input.grid(column=1, row=0, sticky="NESW")
        time_scale_input.bind('<KeyRelease>',self.entry_in_timespinbox)
        
   
        average_label = ttk.Label(spinbox_container, 
                                  text="Average", 
                                  style="Label.TLabel"
                                  ) 
        average_label.grid(column=0, row=1, sticky="NESW")
        
        self.average_value = tk.IntVar()
        self.average_value_str = tk.StringVar()
        self.average_value_before = tk.StringVar(value=0)
        average_display = ttk.Label(spinbox_container, 
                                    textvariable=self.average_value_str, 
                                    ) 
        average_display.grid(column=1, row=1, sticky="NESW")
        
        average_scale = ttk.Scale(self, 
                                  orient="horizontal", 
                                  from_=0, 
                                  to=10000, 
                                  variable = self.average_value
                                  )
        average_scale.grid(row=4, column=0, sticky="NESW")
        average_scale.bind('<Motion>',self.motion_in_scale)
        
        self.reglage_1 = self.controller.main_frame.communication_picoscope.picoscope_properties["self.average"]

        
    def motion_in_scale(self,event):
        received_average = self.average_value.get()
        self.average_value_str.set(str(received_average))
        self.controller.main_frame.communication_picoscope.picoscope_properties["self.average"]=received_average
        #print(received_average)
        
    def entry_in_timespinbox(self,event):
        received_time_scale = self.time_scale_value.get()
        self.update_val  = 1
        self.CommunicationPicoscope()
        #print(received_time_scale)
        
        