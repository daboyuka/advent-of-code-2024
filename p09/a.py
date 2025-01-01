#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

data = lines(list, ptuple(int))[0]
pairs = list(batched(data, 2))

disk = []
for i, rec in enumerate(pairs):
    alloc, free = rec if len(rec) == 2 else rec + (0,)
    disk += list(repeat(i, alloc))
    disk += list(repeat(None, free))

j = len(disk)-1
for i in range(len(disk)):
    while j > i and disk[i] is None:
        disk[i], disk[j] = disk[j], disk[i]
        j -= 1

disk = disk[:disk.index(None)]

print(disk)
total = 0
for i, v in enumerate(disk):
    total += i * v

print(total)
