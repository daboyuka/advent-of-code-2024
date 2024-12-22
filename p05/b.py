#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

rulesRaw, seqs = linegroups(
    pchain(pdelim('|'), ptuple(int)),
    pdelim(',', int),
)
rules = set(rulesRaw)

def safe(seq):
    for i, v1 in enumerate(seq):
        for v2 in seq[i+1:]:
            if (v2, v1) in rules:
                return False
    return True

def popfirst(seq):
    for i, v in enumerate(seq):
        if not any(v2 for v2 in seq if (v2, v) in rules):
            return seq.pop(i), seq

def reorder(seq):
    out = []
    while len(seq) > 0:
        v, seq = popfirst(seq)
        out.append(v)
    return out

total = 0
for seq in seqs:
    if not safe(seq):
        seq = reorder(seq)
        total += seq[int(len(seq)/2)]

print(total)
