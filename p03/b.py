#!/usr/bin/env python3
from helpers import *
from itertools import *
from collections import *
from functools import *
from tqdm import *
import re

inp = sys.stdin.read() #lines()

pat = re.compile(r"(mul|do|don't)\((?:(\d+),(\d+))?\)")

total = 0
enabled = True
for cmd, x, y in pat.findall(inp):
    print(cmd, x, y)
    if cmd == "do":
        enabled = True
    elif cmd == "don't":
        enabled = False
    elif cmd == "mul" and enabled and x != "" and y != "":
        total += int(x)*int(y)

print(total)
