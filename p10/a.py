#!/usr/bin/env python3
from collections import defaultdict

from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

g = grid(lines(list, pmap(lambda t: int(t) if t != '.' else None)))

endpoints = defaultdict(set)  # pt -> endpoint set

for pt in g.find(9):
    endpoints[pt] = {pt}

for height in range(8, -1, -1):
    for pt in g.find(height):
        for pt2 in pt.nbr4():
            if g.at(pt2) == height+1:
                endpoints[pt] = endpoints[pt].union(endpoints[pt2])

total = 0
for pt in g.find(0):
    total += len(endpoints[pt])

print(total)
