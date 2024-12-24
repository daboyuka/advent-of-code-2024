#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

eqs = lines(
    pdelim(": "),
    ptuple(int, pdelim(" ", int)),
)

def cat(a, b):
    return int(str(a) + str(b))

def check(seq, v, target):
    if len(seq) == 0:
        return v == target
    elif v > target:
        return False

    first, nextSeq = seq[0], seq[1:]
    for v2 in [cat(v, first), v * first, v + first]:
        if check(nextSeq, v2, target):
            return True
    return False

total = 0
for result, seq in eqs:
    if check(seq[1:], seq[0], result):
        total += result

print(total)
