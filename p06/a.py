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

visited = set()
while pos:
    visited.add(pos)
    pos, d = move(pos, d)

print(len(visited))
