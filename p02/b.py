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

def safe2(report):
    if safe(report):
        return True
    for i, _ in enumerate(report):
        if safe(report[:i] + report[i+1:]):
            return True
    return False

total = 0
for report in lines(pdelim(), ptuple(int)):
    if safe2(report):
        total += 1
        print(report)

print(total)
