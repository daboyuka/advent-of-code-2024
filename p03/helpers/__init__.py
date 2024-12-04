#!/usr/bin/env python3
import collections
import functools
import itertools
import math
import sys
import re
import operator
import heapq

BLK = "\u2588"  # full ASCII block

#
# Parsing
#

# Split input on newlines into list of strings.
# parsers are item mappers applied to each line (in sequence).
def lines(*parsers):
    ls = sys.stdin.readlines()
    ls = map(lambda x: x.rstrip("\n"), ls)
    for p in parsers:
        ls = map(p, ls)
    return list(ls)

# parsers are item mappers where the i'th parser applies to the lines
# of the i'th linegroup. If there are more linegroups than parsers, the
# last parser is used for all remaining linegroups.
def linegroups(*parsers):
    def r(parts, x):
        if x == "":
            parts.append([])
        else:
            if len(parsers) > 0:
                lgi = len(parts)-1
                parser = parsers[lgi if lgi < len(parsers) else -1]
                x = parser(x)
            parts[-1].append(x)
        return parts

    return list(functools.reduce(r, lines(), [[]]))


def pdebug(prefix="DEBUG"):
    def _parse(l):
        print(prefix, l)
        return l
    return _parse

# pchain returns an item mapper that applies mappers in sequence
# to each item.
def pchain(*mappers):
    if len(mappers) == 0:
        return lambda l: l
    elif len(mappers) == 1:
        return mappers[0]

    def _parse(l):
        for m in mappers:
            l = m(l)
        return l
    return _parse

# pdelim returns an item mapper that splits a line on a delim.
# If mappers are given, they are composed and applied to map each split value.
def pdelim(d=" ", *mappers):
    return lambda l: list(map(pchain(*mappers), l.split(d)))

# predelim returns an item mapper that splits a line on a regex delim.
# If mappers are given, they are composed and applied to map each split value.
def predelim(d=" +", *mappers):
    r = re.compile(d)
    return lambda l: list(map(pchain(*mappers), r.split(l)))

# pmap returns an item mapper for tuples/lists that applies mappers
# to the elements of the input list.
def pmap(*mappers):
    return lambda l: tmap(pchain(*mappers), l)

# ptuple returns an item mapper for tuples that maps the i'th component
# of each tuple using emappers[i].
#
# If a tuple has fewer components than emappers, later emappers are ignored
# If a tuple has more components than emappers, emappers[-1] is applied to excess components
def ptuple(*emappers):
    return lambda t: tuple(
        emappers[i if i < len(emappers) else -1](e)
        for (i, e) in enumerate(t)
    )

# pre returns an item mapper that parses a line using regexp r,
# returning all capture groups as a tuple
def pre(r):
    r = re.compile(r)
    return lambda l: r.match(l).groups()

# pre1 is as pre, but returns a single capture group as a string (not tuple).
def pre1(r):
    r = re.compile(r)
    return lambda l: r.match(l).group(1)

# prelg returns an item mapper that parses a linegroup using regexp r,
# returning all capture groups as a tuple
#
# The regexp is stripped, and linegroup lines are stripped and joined by
# newline (with no final newline). This allows a triple-quoted raw string
# to be used as the regexp without worrying about stray newlines at the edges).
def prelg(r):
    next = pre("(?m)" + r.strip())
    return lambda lg: next("\n".join(map(str.strip, lg)))

#
# Data structs and list funcs
#

def idict(): return collections.defaultdict(lambda: 0)
def sdict(): return collections.defaultdict(lambda: "")
def bdict(): return collections.defaultdict(lambda: False)
def ldict(): return collections.defaultdict(lambda: [])

def tmap(f, iterable):
    t = type(iterable)
    return t(map(f, iterable))

def prod(l):
    return functools.reduce(operator.mul, l, 1)

# part partitions seq into tuples of length n.
# If seq's length is not a multiple of n, pad with fillvalue.
def part(seq, n, fillvalue=None):
    return itertools.zip_longest(*[iter(seq)] * n, fillvalue=fillvalue)

# edgedist: lambda x, y: weight of edge (x, y) (only called on neighboring nodes)
#           (weight must be additive and comparable)
def shortpath(a, b, nbrs, edgedist, maxd=None):
    # trace from b backwards, to build path table
    path = {}  # node -> next node on shortest path to b
    next = [(None, b, None)]  # a heap of (dist, node, prev node on path to b)
    while len(next) > 0:
        d, cur, prev = heapq.heappop(next)
        if cur in path:
            continue
        elif maxd != None and d >= maxd:
            continue

        path[cur] = prev
        if cur == a:
            return d, path

        for nbr in nbrs(cur):
            d2 = edgedist(nbr, cur)
            if d != None:
                d2 += d
            heapq.heappush(next, (d2, nbr, cur))

    return None, None

#
# Math
#

def sgn(x): return 1 if x > 0 else -1 if x < 0 else 0

#
# Points and geometry
#

# Compute bounding box of list of pts
def bounds(pts):
    ndim = len(next(iter(pts)))
    lb, ub = (), ()
    for dim in range(ndim):
        lb += (min(pt[dim] for pt in pts),)
        ub += (max(pt[dim] for pt in pts) + 1,)
    return P(*lb), P(*ub)

# Iterate over bounding box from pt a to b
def iterbb(a, b):
    ranges = map(lambda lu: range(*lu), zip(a, b))
    return itertools.product(*ranges)

# Iterate over horizontal/vertical line
def iterline(a, b, incl=True):
    idxs = [i for i in range(len(a)) if a[i] != b[i]]
    if len(idxs) == 0:
        yield a
    elif len(idxs) > 1:
        raise ValueError("{} and {} have {} differing coordinates".format(a, b, len(idxs)))

    i = idxs[0]
    ai, bi = (a[i], b[i]) if a[i] < b[i] else (b[i], a[i])
    for x in range(ai, bi + (1 if incl else 0)):
        yield a.replace(i, x)

# iterborder iterates over the (inclusive) boundary of bounding box from pt a to b
# (Ex: includes a; excludes b)
# BROKEN
def iterborder(a, b):
    yield from iterline(a, b.replace(0, a[0]), False)
    yield from iterline(b.replace(0, a[0]), b, False)
    yield from iterline(b, a.replace(1, b[0]), False)
    yield from iterline(a.replace(1, b[0]), a, False)

# Manhattan distance
def mdist(a, b):
    return sum(abs(a[i] - b[i]) for i in range(len(a)))

# Euclidean distance
def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))


class P(tuple):
    class _f(int):
        def __get__(self, obj, objtype=None):
            return obj[self]

    x, y, z, w = _f(0), _f(1), _f(2), _f(3)
    r, c = _f(0), _f(1)

    def __new__(cls, *args):
        p = super().__new__(cls, args)
        p.dim = len(args)
        return p

    def __add__(self, other):
        return P(*map(sum, zip(self, other)))
    def __sub__(self, other):
        return P(*map(lambda pt: pt[0] - pt[1], zip(self, other)))
    def __neg__(self):
        return P(*map(lambda x: -x, self))
    def __mul__(self, other):
        return P(*map(lambda x: x * other, self))
    def __truediv__(self, other):
        return P(*map(lambda x: x / other, self))
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    def replace(self, idx, v):
        return P(*self[:idx], v, *self[idx+1:])

    # Return P with all coords increased by 1 (e.g. inclusive -> exclusive bound)
    def inc(self):
        return P(*(v + 1 for v in self))
    # Return P with all coords decreased by 1 (e.g. exclusive -> inclusive bound)
    def dec(self):
        return P(*(v - 1 for v in self))

    def nbr4(self):
        for i in range(self.dim):
            yield self + P(*(1 if i == j else 0 for j in range(self.dim)))
            yield self + P(*(-1 if i == j else 0 for j in range(self.dim)))
    def nbr8(self):
        for delta in itertools.product([-1, 0, 1], repeat=self.dim):
            if -1 in delta or 1 in delta:
                yield self + P(*delta)

class dir(int):
    x, y = [1, 0, -1, 0], [0, 1, 0, -1]
    r, c = [0, -1, 0, 1], [1, 0, -1, 0]
    def vec(self, l=1):
        return P(dir.x[self]*l, dir.y[self]*l)
    def gvec(self, l=1):
        return P(dir.r[self]*l, dir.c[self]*l)
    def turn(self, amt):
        return dir((self + amt) % 4)

east, north, west, south = tuple(map(dir, range(4)))

class grid(list):
    def __init__(self, rows, base=(0,0)):
        super().__init__(rows)
        self.base = P(*base)

    def size(self):
        return P(len(self), len(self[0]))
    def bounds(self):
        return self.base, self.base + self.size()
    def inbounds(self, pt):
        lb, ub = self.bounds()
        return pt.r >= lb.r and pt.r < ub.r and pt.c >= lb.c and pt.c < ub.c
    def at(self, pt, default=None):
        if not self.inbounds(pt):
            return default
        pt -= self.base
        return self[pt.r][pt.c]
    def set(self, pt, v):
        if not self.inbounds(pt):
            raise Exception("out of bounds: {} outside {}".format(pt, self.bounds()))
        pt -= self.base
        self[pt.r][pt.c] = v

    def render(self):
        return "\n".join(["".join(row) for row in self])

    def itertiles(self, d=south):
        rs, cs = self.size()
        rows = range(rs) if d != north else reversed(range(rs))
        cols = range(cs) if d != west else reversed(range(cs))

        if d == north or d == south:
            it = ((r, c) for r in rows for c in cols)
        else:
            it = ((r, c) for c in cols for r in rows)

        for r, c in it:
            yield self.base + P(r, c), self[r][c]
    def iterrows(self):
        for r, row in enumerate(self):
            yield self.base[0] + r, row
    def itercols(self):
        for c in range(0, len(self[0])):
            yield c + self.base[1], [self[r][c] for r in range(len(self))]

    def count(self, v):
        return sum(self.find(v))
    def find(self, v):
        if not callable(v):
            find = v
            v = lambda t: t == find
        return (pt for pt, t in self.itertiles() if v(t))

    # passable: tileval -> True/False (can walk on)
    def shortpath(self, a, b, passable, maxd=None, nbrs=P.nbr4):
        _passable = passable if callable(passable) else lambda t: t == passable
        _nbrs = lambda pt: (nbr for nbr in nbrs(pt) if self.inbounds(nbr) and _passable(self.at(nbr)))

        return shortpath(a, b, _nbrs, lambda x, y: 1, maxd)

    # visit: pt, tileval, vals[pt], vals -> yield (pt2, v2), ...
    # where vals is the current table of pt -> v
    def flood(self, pt, v, visit):
        vals = {pt: v}
        next = collections.deque([pt])
        while len(next) > 0:
            nextpt = next.popleft()
            for pt2, v2 in visit(nextpt, self.at(nextpt), vals[nextpt], vals):
                if pt2 not in vals:
                    vals[pt2] = v2
                    next.append(pt2)
        return vals

    def copy(self):
        g2 = grid([])
        g2.base = self.base
        for row in self:
            g2.append(row.copy())
        return g2

def newgrid(ub, fillval):
    return grid([[fillval for j in range(ub.c)] for i in range(ub.r)])

def newgridbased(lb, ub, fillval):
    return grid([[fillval for j in range(ub.c - lb.c)] for i in range(ub.r - lb.r)], lb)

def newgridpts(pts, ptval, fillval):
    lb, ub = bounds(pts)
    g = newgridbased(lb, ub, fillval)
    for pt in pts:
        g.set(pt, ptval)
    return g

def parsegrid(lines):
    return grid(tmap(list, lines))

class infgrid(dict):
    def __init__(self, pts=[], ptval='#', fillval='.', loose=False):
        super().__init__((pt, ptval) for pt in pts)
        self.fillval, self.loose = fillval, loose
        if len(self) > 0:
            self.lb, self.ub = self._computebb()
        else:
            self.lb, self.ub = P(0,0), P(0,0)

    def _computebb(self):
        return bounds(self.keys())
    def size(self):
        return self.ub - self.lb
    def bounds(self):
        return self.lb, self.ub
    def inbounds(self, pt):
        lb, ub = self.bounds()
        return pt.r >= lb.r and pt.r < ub.r and pt.c >= lb.c and pt.c < ub.c
    def onbounds(self, pt):
        lb, ub = self.bounds()
        return pt.r == lb.r or pt.r == ub.r-1 or pt.c == lb.c or pt.c == ub.c-1

    def at(self, pt):
        return self.get(pt, self.fillval) if self.inbounds(pt) else self.fillval
    def set(self, pt, v):
        if v == self.fillval:
            self.pop(pt, None)
            if not self.loose and self.onbounds(pt):
                self.lb, self.ub = self._computebb()  # tighten bounds if we removed a potential boundary point
        else:
            self[pt] = v
            if len(self) == 1:
                self.lb, self.ub = pt, pt.inc()
            else:
                self.lb, self.ub = bounds([self.lb, self.ub.dec(), pt])

    def render(self):
        lb, ub = self.bounds()
        out = ""
        for r in range(lb.r, ub.r):
            line = ""
            for c in range(lb.c, ub.c):
                line += self.at(P(r, c))
            out += line + "\n"
        return out

    def itertiles(self):
        return self.items()
    def count(self, v):
        if not callable(v):
            find = v
            v = lambda x: x == find

        return sum(1 for x in self.values() if v(x))

    # passable: tileval -> True/False (can walk on)
    def shortpath(self, a, b, passable, maxd=None, nbrs=P.nbr4):
        _passable = passable if callable(passable) else lambda t: t == passable
        _nbrs = lambda pt: (nbr for nbr in nbrs(pt) if self.inbounds(nbr) and _passable(self.at(nbr)))

        return shortpath(a, b, _nbrs, lambda x, y: 1, maxd)

    def copy(self):
        g2 = super().copy()
        g2.fillval, self.loose, g2.lb, g2.ub = self.fillval, self.loose, self.lb, self.ub
        return g2

# half-open interval
class intv(tuple):
    def __new__(cls, a, b):
        if a >= b: a, b = 0, 0
        return super().__new__(cls, [a, b])

    def degen(self): return self[0] >= self[1]

    def intersects(self, other):
        return self[0] < other[1] and other[0] < self[1]
    def contains(self, other):
        return self[0] <= other[1] and self[1] >= other[1]
    def overlaps(self, other):
        return self.intersects(other) and not self.contains(other) and not other.contains(self)
    def has(self, x):
        return self[0] <= x < self[1]

    def labuts(self, other): return self[1] == other[0]
    def rabuts(self, other): return self[0] == other[1]
    def abuts(self, other): return self.labuts(other) or self.rabuts(other)

    def union(self, other):
        if self.intersects(other) or self.abuts(other):
            return intv(min(self[0], other[0]), max(self[1], other[1])), (0,0)
        else:
            return self, other

    def intersect(self, other):
        if not self.intersects(other):
            return intv(0, 0)
        return intv(max(self[0], other[0]), min(self[1], other[1]))

    def sub(self, other):
        return intv(self[0], min(self[1], other[0])), intv(max(self[0], other[1]), self[1])

    def shift(self, amt):
        return intv(self[0]+amt, self[1]+amt)

# iterintvs generates intervals as the (union of intervals pos) minus (union of intervals neg)
def iterintvs(pos, neg):
    evts = []  # (position, is end?, is pos?)

    for x in pos:
        evts.append((x[0], False, True))
        evts.append((x[1], True, True))
    for x in neg:
        evts.append((x[0], False, False))
        evts.append((x[1], True, False))

    evts.sort()
    poscount, negcount = 0, 0
    begin = None
    def on(): return poscount > 0 and negcount == 0

    for x, isEnd, isPos in evts:
        wasOn = on()

        delta = -1 if isEnd else 1
        if isPos:
            poscount += delta
        else:
            negcount += delta

        # print(x, isEnd, isPos, "=>", wasOn, on(), delta, poscount, negcount)

        if not wasOn and on():
            begin = x
        elif wasOn and not on():
            out = intv(begin, x)
            if not out.degen():
                yield out
