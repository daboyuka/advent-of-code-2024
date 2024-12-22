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

total = 0
for seq in seqs:
    if safe(seq):
        mid = seq[int(len(seq)/2)]
        print(mid)
        total += mid

print(total)
