#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

g = parsegrid(lines())

def checkXmas(pt):
    return g.at(pt) == "A" and all( # center is A and both...
        set(g.at(pt + d) for d in [delta, -delta]) == {"M", "S"}
        for delta in [P(-1, -1), P(-1, 1)] # ...are MS
    )

total = sum(1 for pt, _ in g.itertiles() if checkXmas(pt))
print(total)
