#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

def safe(report):
    deltas = list(map(lambda t: t[1] - t[0], pairwise(report)))
    mono = all(map(lambda x: x > 0, deltas)) or all(map(lambda x: x < 0, deltas))
    deltasAbs = tmap(abs, deltas)
    return mono and min(deltasAbs) >= 1 and max(deltasAbs) <= 3


total = 0
for report in lines(pdelim(), ptuple(int)):
    if safe(report):
        total += 1
        print(report)

print(total)
