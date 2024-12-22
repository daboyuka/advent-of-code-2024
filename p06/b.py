#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

t2d = { '^': north, 'V': south, '<': west, '>': east }

g = parsegrid(lines())

pos = next(iter(g.find(lambda t: t in t2d)))
d = t2d[g.at(pos)]
g.set(pos, '.')

def move(p, d):
    p2 = p + d.gvec()
    t = g.at(p2)
    if not g.inbounds(p2):
        return None, None
    elif t == '.':
        return p2, d
    else:
        return p, d.turn(3)

def checkcycle(pos, d):
    visited = set()
    while pos:
        if (pos, d) in visited:
            return True, visited
        visited.add((pos, d))
        pos, d = move(pos, d)
    return False, visited

_, path = checkcycle(pos, d)

cycles = set()
for checkp, checkd in path:
    p2 = checkp + checkd.gvec()
    if g.at(p2) == '.':
        g.set(p2, '#')
        iscycle, _ = checkcycle(pos, d)
        if iscycle:
            cycles.add(p2)
        g.set(p2, '.')

print(len(cycles))
