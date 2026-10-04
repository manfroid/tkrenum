import re
from typing import Any, List, Dict, Tuple

# dictionary key constants to avoid typos when used multiple times
NUMBER = "number"
IN_FILE_NAME = "in-file-name"
FILENAME_TAIL = "file-name-tail"
OUT_FILE_NAME = "out-file-name"

# transformation options:
#   REVERSE
#   RENUMBER
#   START
#   STEP
#   WIDTH
OPT_RENUMBER = "renumber"
OPT_REVERSE = "reverse"
OPT_START = "start"
OPT_STEP = "step"
OPT_WIDTH = "width"


def build_file_name_map(files: List[str]) -> List[Dict[str, Any]]:
    """Build a list of dicts with file names matching the implicit pattern"""
    file_map = []
    for file in files:
        m = re.match((r"\[(\d+)\](.+)"), file)
        if m:
            file_map.append(
                {NUMBER: int(m.group(1)), FILENAME_TAIL: m.group(2), IN_FILE_NAME: file, OUT_FILE_NAME: file})
    file_map.sort(key=lambda item: item[NUMBER])
    return file_map


def get_in_file_names(file_map: List[Dict[str, Any]]) -> List[str]:
    """Get a list of all input file names from the file_map"""
    return [entry[IN_FILE_NAME]for entry in file_map]


def get_out_file_names(file_map: List[Dict[str, Any]], options: Dict[str, Any]) -> List[str]:
    """Get a list of all transformed output file names from the file_map"""
    apply_options(file_map, options)
    return [entry[OUT_FILE_NAME]for entry in file_map]


def apply_options(file_map: List[Dict[str, Any]], options: Dict[str, Any]) -> List[Dict[str, Any]]:
    """transform file names to output file names applying fn to each entry in file_map"""
    (start, end, width) = get_number_stats(file_map)
    # print(f"{start}-{end}:{width}")
    if options[OPT_RENUMBER]:
        number = options[OPT_START]
        for entry in file_map:
            entry[OUT_FILE_NAME] = f"[{number:0{max(width, options[OPT_WIDTH])}}]{entry[FILENAME_TAIL]}"
            # print(entry[OUT_FILE_NAME])
            number += options[OPT_STEP]
    elif (options[OPT_REVERSE]):
        for entry in file_map:
            number = end - entry[NUMBER] + 1
            entry[OUT_FILE_NAME] = f"[{number + options[OPT_START] - 1:0{max(width, options[OPT_WIDTH])}}]{entry[FILENAME_TAIL]}"
    else:
        for entry in file_map:
            entry[OUT_FILE_NAME] = f"[{entry[NUMBER] + options[OPT_START] - 1:0{max(width, options[OPT_WIDTH])}}]{entry[FILENAME_TAIL]}"
    return file_map


def get_number_stats(file_map: List[Dict[str, Any]]) -> Tuple[int, int, int]:
    """Get the minimum and maximum number along with the latter's number of digits in file_map"""
    min_number = min(entry[NUMBER] for entry in file_map)
    max_number = max(entry[NUMBER] for entry in file_map)
    # return {"min": min_number, "max": max_number, "width": len(str(max_number))}
    return (min_number, max_number, len(str(max_number)))


if __name__ == "__main__":
    map = build_file_name_map([
        "[1] test",
        "[2] another test",
        "3 not to be found",
        "[10] a longer number"
    ])
    # print(map)
    print(get_number_stats(map))
    print(get_in_file_names(map))
    for entry in map:
        print(entry)
