from pathlib import *


def get_files(path):
    if path.exists():
        return [file.name for file in path.iterdir() if file.is_file()]
    return []


def get_dirs(path):
    if path.exists():
        return [dir.name for dir in path.iterdir() if dir.is_dir()]
    return []


def has_parent(dir):
    return dir.resolve() != dir.parent.resolve()
