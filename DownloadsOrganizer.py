import os
import shutil
import subprocess
import sys
import tkinter as tk
import WindowHelpers as wh


########################################################################################################################
# GLOBALS:


newPath = ""

# establish file paths and main user directory options
downloadPath = "/Users/rhoust/Downloads/"
userPath = "/Users/rhoust/"
userDirectories = ['Desktop', 'Documents', 'Music', 'Pictures']


########################################################################################################################
# FUNCTIONS:


def open_finder_at_path(file_path):
    subprocess.run(["open", "-R", file_path])


# These functions are helpers for the user input window
# but they can't return any vals (thus they must modify global vars)
def on_submit_click(event, mainDropDown, subDropDown):
    global newPath
    global userPath
    newPath = userPath + mainDropDown.get() + '/' + subDropDown.get() + '/'


def on_default_click(event):
    global newPath
    global downloadPath
    newPath = downloadPath

# create_window - populates user input window to specify where to move download file to
def create_window(filename):

    global userDirectories
    global userPath

    # make root tkinter window
    root = tk.Tk()
    root.title("Downloads Organization Wizard")
    root.geometry("300x210")

    wh.create_label(root, "Moving file/folder: '" + filename + "'")

    # button to instantly send to downloads folder
    sendToDownloadsButton = wh.create_button(root, "Leave File In Downloads")

    wh.create_label(root, "OR: ")
    wh.create_label(root, "Choose Main Directory")

    # make main directory combo box
    mainDropDown = wh.create_combo_box(root, userDirectories)

    wh.create_label(root, "Choose Sub-Directory")

    # make subdirectory combo box
    subDropDown = wh.create_combo_box(root, [])

    # finally, create a submit button
    submitButton = wh.create_button(root, "Submit")

    # populate subdirectory drop down based on selection in first window
    mainDropDown.bind("<<ComboboxSelected>>", lambda event: wh.update_subdirectories(event, subDropDown, userPath))

    # update global "new path" based on button choice
    submitButton.bind("<Button>", lambda event: on_submit_click(event, mainDropDown, subDropDown))
    sendToDownloadsButton.bind("<Button>", on_default_click)

    root.mainloop()


########################################################################################################################
# MAIN:


# get most recently downloaded file - sent to stdin by automator
downloadFile = sys.stdin.readline().strip().split('/')
downloadFile = downloadFile[-1]

# use UI to get new desired path from user
if downloadFile != "":
    create_window(downloadFile)
else:
    raise Exception("Error: file in downloads has no name or file does not exist in downloads")

if newPath == "":
    # operation was cancelled - leave download in downloads
    exit(0)
else:
    # move file to new path!
    if os.path.exists(newPath):
        shutil.move(downloadPath + downloadFile, newPath + downloadFile)

    elif newPath.split('/')[-2] == "NONE":
        # move file to new path - omit the none option at the end
        newPath = newPath[:-5]
        shutil.move(downloadPath + downloadFile, newPath)

    # filepath does not exist
    else:
        raise Exception("Error: filepath not found")

# open new file path in macOS finder for custom rearrangement
open_finder_at_path(newPath + downloadFile)

