#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

g = parsegrid(lines())

def solveDelta(delta):
    return sum(1 for pt, _ in g.itertiles() if (
        all(g.at(pt + delta * i) == l for i, l in enumerate("XMAS"))
    ))

total = 0
deltas = P(0, 0).nbr8()
for delta in deltas:
    total += solveDelta(delta)

print(total)
