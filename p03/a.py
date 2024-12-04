#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

inp = sys.stdin.read() #lines()

pat = re.compile(r"mul\((\d+),(\d+)\)")

total = 0
for x, y in pat.findall(inp):
    total += int(x)*int(y)
    print(x, y)

print(total)
