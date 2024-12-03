#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

l1, l2 = [], []
for a, b in lines(pdelim("   "), ptuple(int)):
    l1.append(a)
    l2.append(b)

total = 0
for a, b in zip(sorted(l1), sorted(l2)):
    total += abs(a - b)

print(total)
