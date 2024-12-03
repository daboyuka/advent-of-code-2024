#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

l1, l2 = [], idict()
for a, b in lines(pdelim("   "), ptuple(int)):
    l1.append(a)
    l2[b] += 1

total = 0
for v in l1:
    total += v * l2[v]

print(total)
