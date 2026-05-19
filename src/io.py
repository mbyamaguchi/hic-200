import gzip
from typing import List
import numpy as np
from pathlib import Path

def make_tidy(strlst, mode="txtgz") -> List:
    """converts string in list all to integer"""
    if not (mode == "txtgz"):
        print("Error: not implemented.")
        return

    mapping = {
        'I': 1,
        'II': 2,
        'III': 3,
    }
    
    tidylst = [mapping.get(x, x) for x in strlst]

    return tidylst

def count_length(path: Path) -> int:
    """Counts length of the file"""
    with gzip.open(path, mode="rt", encoding="utf-8") as f:
        return sum(1 for _ in f)

def read_txtgz(path: Path, nlines, delimiter="\t",
                datatype="list", lenmax=None, ignore_interchrom=True) -> List[List]:
    """main process: reads txt.gz and converts to list[list]"""
    try:
        with gzip.open(path, mode="rt", encoding="utf-8") as f:
            lines = []
            line = f.readline()
            
            if lenmax is None:
                lenmax = nlines
            else:
                lenmax = min(lenmax, nlines)
            
            for _ in range(lenmax):
                line = f.readline()                
                tidyline = list(map(int, make_tidy(line.rstrip().split(delimiter))))

                if not tidyline[0] == tidyline[4]:
                    continue
                else:
                    lines.append(tidyline)

    except Exception as e:
        print("Error:", e)

    if datatype == "list":
        return lines
    elif datatype == "numpy":
        return lines

def show_txtgz(path: Path, nheads=5, include_header=True, show_raw=False):
    try:
        with gzip.open(Path("../examples/HiC_Double-MHM_fragment_pair.txt.gz"),
                       mode="rt", encoding="utf-8") as f:
            if not include_header:
                line = f.readline()
            for i in range(nheads):
                line = f.readline()
                if show_raw:
                    print(repr(line))
                else:
                    print(line.rstrip().replace('\t', ' '))
    except Exception as e:
        print("Error:", e)