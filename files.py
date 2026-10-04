from pathlib import *
from typing import List


def get_files(path: Path) -> List[str]:
    if path.exists():
        return [file.name for file in path.iterdir() if file.is_file()]
    return []


def get_dirs(path: Path) -> List[str]:
    if path.exists():
        return [dir.name for dir in path.iterdir() if dir.is_dir()]
    return []


def has_parent(dir: Path) -> bool:
    return dir.resolve() != dir.parent.resolve()
