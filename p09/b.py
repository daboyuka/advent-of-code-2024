#!/usr/bin/env python3
from argparse import ArgumentError

from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

data = lines(list, ptuple(int))[0]
pairs = list(batched(data, 2))

disk = []  # [(file, alloc, free)]
for i, rec in enumerate(pairs):
    alloc, free = rec if len(rec) == 2 else rec + (0,)
    disk.append((i, alloc, free))

def delpos(pos):
    _, alloc, free = disk.pop(pos)
    fidxPre, allocPre, freePre = disk[pos-1]  # we never delete the first file so this is safe
    disk[pos-1] = (fidxPre, allocPre, freePre + alloc + free)

def inspos(pos, fidx, alloc):
    fidxPre, allocPre, freePre = disk[pos]
    if alloc > freePre:
        raise ArgumentError(None, "exceeds freespace")

    disk[pos] = (fidxPre, allocPre, 0)
    disk.insert(pos+1, (fidx, alloc, freePre-alloc))

def relocate(pos):
    fidx, alloc, _ = disk[pos]
    for pos2, (_, _, free2) in enumerate(disk[:pos]):
        if free2 >= alloc:
            delpos(pos)
            inspos(pos2, fidx, alloc)
            return True
    return False

nextFidx, nextPos = len(disk)-1, len(disk)-1
while nextPos >= 0 and nextFidx > 0:
    fidx, _, _ = disk[nextPos]
    if fidx != nextFidx:
        nextPos -= 1
        continue
    nextFidx -= 1
    if relocate(nextPos):
        continue
    nextPos -= 1

print(disk)
total = 0
offset = 0
for i, (fidx, alloc, free) in enumerate(disk):
    mass = (2 * offset + alloc - 1) * alloc // 2
    total += mass * fidx
    offset += alloc + free

print(total)
