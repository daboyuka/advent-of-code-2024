#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

stones = lines(pdelim(" ", int))[0]

memo = idict()  # (val, depth) -> nstones

def digits(val):
    return 1 if val < 10 else 1 + digits(val//10)

def step(val):
    if val == 0: return (1, )
    d = digits(val)
    if d % 2 == 0:
        m = 10 ** (d//2)
        return val // m, val % m
    return (val * 2024, )

def evolve(val, depth):
    if depth == 0:
        return 1

    k = (val, depth)
    if k in memo:
      return memo[k]

    total = sum(evolve(val2, depth-1) for val2 in step(val))
    memo[k] = total
    return total

total = sum(evolve(val, 25) for val in stones)
print(total)


