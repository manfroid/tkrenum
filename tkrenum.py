import os
import tkinter as tk
from files import *

PARENT = ".."
# PARENT = "↖"


def dir_list_dblclk(event=None):
    sel_indexes = dir_list.curselection()
    if sel_indexes:
        dir_name = dir_list.get(sel_indexes[0])
        if dir_name == PARENT:
            set_parent_dir()
        else:
            # don't forget to strip '[' and ']' from dir_name (like I did...)
            dir_name = Path(Path(folder.get()) / dir_name[1:-1])
            folder.set(dir_name.resolve())
            fill_lists()


def fill_dir_list():
    dir_list.delete(0, tk.END)
    dir_list.insert(0, PARENT)
    path = Path(folder.get()).resolve()
    dirs = get_dirs(path)
    if dirs:
        dirs = [f"[{dir}]" for dir in sorted(dirs, key=str.lower)]
        dir_list.insert(tk.END, *sorted(dirs))


def fill_file_list():
    # first, remove all files from list (applies to folder without any files, too)
    file_list.delete(0, tk.END)
    path = Path(folder.get())
    if path.exists:
        files = get_files(path)
        if files:
            file_list.insert(tk.END, *sorted(files, key=str.lower))


def update_widgets():
    path = Path(folder.get()).resolve()
    # print(f"update widgtes for path {path} (exists: {path.exists()})")
    folder_entry["fg"] = "white" if path.exists() else "red"
    folder_up_button["state"] = tk.NORMAL if path != path.parent else tk.DISABLED


# fill_lists may get called from a binding (event supplied) or from a wodget command
def fill_lists(event=None):
    """fill dir and file lists and update related widgets"""
    folder.set(Path(folder.get()).resolve())
    fill_dir_list()
    fill_file_list()
    update_widgets()


def set_parent_dir(event=None):
    path = Path(folder.get()).resolve()
    folder.set(path.parent.resolve())
    fill_lists()


# def show_dirs_clicked():
#     fill_file_list()


root = tk.Tk()
root.title("reNUM")

# associated variables
folder = tk.StringVar()

# folder input area
folder_frame = tk.Frame(root)
folder_entry_label = tk.Label(folder_frame, text="Folder: ")
folder_entry = tk.Entry(folder_frame, textvariable=folder)
folder_entry.bind("<Return>", fill_lists)
folder_scan_button = tk.Button(folder_frame, text="Scan", command=fill_lists)
folder_up_button = tk.Button(folder_frame, text="UP", command=set_parent_dir)

# arrange widgets
folder_entry_label.pack(side=tk.LEFT)
folder_entry.pack(side=tk.LEFT, padx=8, pady=8, fill=tk.X, expand=True)
folder_up_button.pack(side=tk.LEFT)
folder_scan_button.pack(side=tk.LEFT)
folder_frame.pack(padx=16, fill=tk.X, expand=False)

dir_list = tk.Listbox(root, height=6)
dir_list.bind("<Double-Button-1>", dir_list_dblclk)
dir_list.bind("<BackSpace>", set_parent_dir)
dir_list.pack(fill=tk.X, expand=False, padx=16)

# file name list frame
file_list_frame = tk.Frame(root)
# list of file names
file_list = tk.Listbox(file_list_frame)
file_list.pack(side=tk.LEFT, padx=16, pady=8, fill=tk.BOTH, expand=True)
# list of renamed files
renamed_file_list = tk.Listbox(file_list_frame)
renamed_file_list.pack(side=tk.LEFT, padx=16, pady=8,
                       fill=tk.BOTH, expand=True)
file_list_frame.pack(fill=tk.BOTH, expand=True)

fill_lists()

root.mainloop()
