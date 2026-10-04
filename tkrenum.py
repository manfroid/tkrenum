import os
import tkinter as tk
from files import *
from numbering import *
from ui import *
from typing import Any, Dict, Optional

PARENT = ".."
# PARENT = "↖"


def get_options() -> Dict[str, Any]:
    return {
        OPT_RENUMBER: renumber.get(),
        OPT_REVERSE: reverse.get(),
        OPT_START: int(start.get() or "1"),
        OPT_STEP: int(step.get() or "1"),
        OPT_WIDTH: int(width.get() or "1"),
    }


def options_changed(name: Optional[str], old_value: Optional[str], new_value: Optional[str]) -> Optional[List[Dict[str, Any]]]:
    options = get_options()
    # print(f"options changed: {options}")
    return fill_file_lists()


def dir_list_dblclk(event: Optional[tk.Event] = None) -> None:
    sel_indexes = dir_list.curselection()
    if sel_indexes:
        dir_name = dir_list.get(sel_indexes[0])
        if dir_name == PARENT:
            set_parent_dir()
        else:
            # don't forget to strip '[' and ']' from dir_name (like I did...)
            dir_name = Path(Path(folder.get()) / dir_name[1:-1])
            folder.set(str(dir_name.resolve()))
            fill_lists()


def fill_dir_list() -> None:
    dir_list.delete(0, tk.END)
    path = Path(folder.get()).resolve()
    if has_parent(path):
        dir_list.insert(0, PARENT)
    dirs = get_dirs(path)
    if dirs:
        dirs = list(filter(lambda s: not s.startswith('.'), dirs))
        dirs = [f"[{dir}]" for dir in sorted(dirs, key=str.lower)]
        dir_list.insert(tk.END, *sorted(dirs))


def fill_file_lists() -> Optional[List[Dict[str, Any]]]:
    # first, remove all files from list (applies to folder without any files, too)
    file_list.delete(0, tk.END)
    renamed_file_list.delete(0, tk.END)
    path = Path(folder.get())
    if path.exists():
        files = get_files(path)
        if files:
            files = list(filter(lambda s: not s.startswith('.'), files))
            file_map = build_file_name_map(files)
            if file_map:
                file_list.insert(tk.END, *get_in_file_names(file_map))
                renamed_file_list.insert(
                    tk.END, *get_out_file_names(file_map, get_options()))
                return file_map
    return None


def update_widgets() -> None:
    path = Path(folder.get()).resolve()
    # print(f"update widgtes for path {path} (exists: {path.exists()})")
    folder_entry["fg"] = "white" if path.exists() else "red"
    folder_up_button["state"] = tk.NORMAL if has_parent(path) else tk.DISABLED


# fill_lists may get called from a binding (event supplied) or from a wodget command
def fill_lists(event: Optional[tk.Event] = None) -> None:
    """fill dir and file lists and update related widgets"""
    folder.set(str(Path(folder.get()).resolve()))
    fill_dir_list()
    fill_file_lists()
    update_widgets()


def set_parent_dir(event: Optional[tk.Event] = None) -> None:
    path = Path(folder.get()).resolve()
    folder.set(str(path.parent.resolve()))
    fill_lists()


# def show_dirs_clicked():
#     fill_file_lists()


root = tk.Tk()
root.title("reNUM")
root.geometry("640x480")
root.minsize(width=320, height=240)

# associated variables
folder = tk.StringVar()

mainmargin = 8
tweenmargin = 8
uifont = ("Courier", 16)

# folder input area
folder_frame = tk.Frame(root)
folder_entry_label = tk.Label(folder_frame, text="Folder: ", font=uifont)
folder_entry = tk.Entry(folder_frame, textvariable=folder, font=uifont)
folder_entry.bind("<Return>", fill_lists)
folder_scan_button = tk.Button(
    folder_frame, text="Scan", font=uifont, command=fill_lists)
folder_up_button = tk.Button(
    folder_frame, text="UP", font=uifont, command=set_parent_dir)
# directories list
dir_list = tk.Listbox(root, height=6, font=uifont)
dir_list.bind("<Double-Button-1>", dir_list_dblclk)
dir_list.bind("<Return>", dir_list_dblclk)
dir_list.bind("<BackSpace>", set_parent_dir)
# file name list frame
file_list_frame = tk.Frame(root)
file_list = tk.Listbox(file_list_frame, font=uifont)
renamed_file_list = tk.Listbox(file_list_frame, font=uifont)

# arrange widgets
folder_entry_label.pack(side=tk.LEFT)
folder_entry.pack(side=tk.LEFT, padx=(tweenmargin, 0), fill=tk.X, expand=True)
folder_up_button.pack(side=tk.LEFT, padx=(tweenmargin, 0))
folder_scan_button.pack(side=tk.LEFT, padx=(tweenmargin, 0))
folder_frame.pack(padx=mainmargin, pady=(
    mainmargin, tweenmargin), fill=tk.X, expand=False)

dir_list.pack(padx=mainmargin, pady=(0, tweenmargin), fill=tk.X, expand=False)

file_list.pack(side=tk.LEFT, padx=(0, tweenmargin), fill=tk.BOTH, expand=True)
renamed_file_list.pack(side=tk.LEFT,
                       fill=tk.BOTH, expand=True)
file_list_frame.pack(fill=tk.BOTH, padx=mainmargin,
                     pady=(0, tweenmargin), expand=True)

# OPTIONS frame
options_frame = tk.Frame(root)
reverse = tk.BooleanVar()
options_reverse = tk.Checkbutton(
    options_frame, text="reverse", variable=reverse, command=options_changed)
renumber = tk.BooleanVar()
options_renumber = tk.Checkbutton(
    options_frame, text="renumber", variable=renumber, command=options_changed)
options_width_label = tk.Label(options_frame, text="width")
width = tk.StringVar(options_frame, value="0")
options_width = tkNumberEntry(options_frame, textvariable=width, width=2)
width.trace_add("write", options_changed)
options_start_label = tk.Label(options_frame, text="start", justify=tk.RIGHT)
start = tk.StringVar(options_frame, value="1")
options_start = tkNumberEntry(
    options_frame, min=1, textvariable=start, width=8)
start.trace_add("write", options_changed)
options_step_label = tk.Label(options_frame, text="step", justify=tk.RIGHT)
step = tk.StringVar(options_frame, value="1")
options_step = tkNumberEntry(options_frame, min=1, textvariable=step, width=4)
step.trace_add("write", options_changed)
options_apply = tk.Button(options_frame, text="Apply")

options_reverse.pack(side=tk.LEFT, padx=(0, tweenmargin))
options_renumber.pack(side=tk.LEFT, padx=(0, tweenmargin))
options_width_label.pack(side=tk.LEFT, padx=(0, tweenmargin))
options_width.pack(side=tk.LEFT)
options_start_label.pack(side=tk.LEFT, padx=(0, tweenmargin))
options_start.pack(side=tk.LEFT)
options_step_label.pack(side=tk.LEFT, padx=(0, tweenmargin))
options_step.pack(side=tk.LEFT)
options_apply.pack(side=tk.RIGHT)
options_frame.pack(fill=tk.BOTH, padx=mainmargin,
                   pady=(0, mainmargin), expand=False)

fill_lists()

root.mainloop()
