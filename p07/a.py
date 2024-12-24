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

def check(seq, v, target):
    if len(seq) == 0:
        return v == target
    elif v > target:
        return False

    first, nextSeq = seq[0], seq[1:]
    mulv, addv = v * first, v + first
    return check(nextSeq, mulv, target) or check(nextSeq, addv, target)

total = 0
for result, seq in eqs:
    if check(seq[1:], seq[0], result):
        total += result

print(total)
