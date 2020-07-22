#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 12:21:41 2020

tk frames and tk subframes related to the oven for the repeated flash 
experiment GUI

@author: melinapannier
"""


import tkinter as tk
from tkinter import ttk


class Laser(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((1), weight=1)
        self.columnconfigure((0), weight=1)
        
        self.title_label = ttk.Label(self, 
                                     text="LASER CONTROL",
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
        
        
        right_container = RightContainer(sub_container)
        right_container.grid(row=0, column=1)
        
        
        for child in sub_container.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky="NSEW")
            child["style"]="Frame.TFrame"
            #child["padding"]=10
        

        
class LeftContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0,1,2,3,4), weight=1)
        self.columnconfigure((1), weight=1)
        
        
        mode_label = ttk.Label(self, text="Mode : ")
        mode_label.grid(row=0, column=0)
        mode_value = tk.StringVar()
        mode = ttk.Combobox(self, 
                            textvariable=mode_value)
        mode["values"] = ("Burst", "Continued")
        mode.grid(row=0, column=1)
        
        
        repetition_rate_label = ttk.Label(self, text="Répétition Rate : ")
        repetition_rate_label.grid(row=1, column=0)
        repetition_rate_value = tk.StringVar()
        repetition_rate = ttk.Combobox(self, 
                                       textvariable=repetition_rate_value)
        repetition_rate["values"] = ("0", "100","300","700","1000",)
        repetition_rate.grid(row=1, column=1)
        
        
        pulse_label = ttk.Label(self, text="Pulse Rate (kHz): ")
        pulse_label.grid(row=2, column=0)
        pulse_value = tk.StringVar()
        pulse = ttk.Combobox(self, 
                             textvariable=pulse_value)
        pulse["values"] = ("0", "10", "20", "30")
        pulse.grid(row=2, column=1)
        
        
        frequency_label = ttk.Label(self, text="Frequency (kHz): ")
        frequency_label.grid(row=3, column=0)
        frequency_value = tk.StringVar()
        frequency = ttk.Combobox(self, 
                                 textvariable=frequency_value)
        frequency["values"] = ("0", "3", "7", "10")
        frequency.grid(row=3, column=1)
        
        
        magnitude_label = ttk.Label(self, text="Magnitude (%): ")
        magnitude_label.grid(row=4, column=0)
        magnitude_value = tk.StringVar()
        magnitude = ttk.Combobox(self, 
                                 textvariable=magnitude_value)
        magnitude["values"] = ("0", "20", "50", "70", "100")
        magnitude.grid(row=4, column=1)
        
        
        for child in self.winfo_children():
            if isinstance(child, tk.ttk.Label) == True :
                child.grid_configure(sticky="W")
                child["style"]='Label.TLabel'
            if isinstance(child, tk.ttk.Combobox) == True :
                child.grid_configure(sticky="EW")

        
                
class RightContainer(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container,**kwargs)
        
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0), weight=1)
        
        
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
        
        
        play_button = ttk.Button(self, 
                                 text="Play", 
                                 padding=10, 
                                 style="Button.TButton"
                                 )
        play_button.grid(row=1, column=0)