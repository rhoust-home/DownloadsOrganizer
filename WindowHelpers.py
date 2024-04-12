# Helper functions for DownloadsOrganizer input window

import os
import tkinter as tk
from tkinter import ttk

def update_subdirectories(event, subDropDown, userPath):

    # get path from main directory combo box
    mainDropDown = event.widget
    path = userPath + mainDropDown.get()

    options = os.scandir(path)
    optionNames = []

    # filter out hidden files / non-directories in options
    for item in options:
        if item.name[0] == '.' or not item.is_dir() or item.name[-4:] == '.app':
            continue

        optionNames.append(item.name)

    optionNames.append('NONE')
    subDropDown.config(values=optionNames)


def create_label(tRoot, text):
    L = tk.Label(tRoot, text=text)
    L.pack(anchor=tk.W, padx=10)


def create_combo_box(tRoot, values):
    cBox = ttk.Combobox(tRoot, values=values)
    cBox.pack(anchor=tk.W, padx=10)
    return cBox


def create_button(tRoot, text):
    btn = tk.Button(tRoot, text=text, command=tRoot.destroy)
    btn.pack(anchor=tk.SW, padx=10)
    return btn