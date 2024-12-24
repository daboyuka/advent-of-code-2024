#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

g = parsegrid(lines())

towers = ldict()
for pt, t in g.itertiles():
    if t != '.':
        towers[t].append(pt)

ans = set()

for kind, pts in towers.items():
    for a, b in combinations(pts, 2):
        delta = a - b
        for i in count():
            c = a + i*delta
            if not g.inbounds(c):
                break
            ans.add(c)
        for i in count(-1,-1):
            c = a + i*delta
            if not g.inbounds(c):
                break
            ans.add(c)

print(len(ans))
