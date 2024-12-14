#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/grid";

# returns a pair of pairs of
# diagonally-opposed point deltas
def crossdeltas:
    [[-1,-1], [-1,1]] |
    map([mulpt(1, -1)]);

def check($pt):
  at($pt) == "A" and  # center must be A
  all(
    crossdeltas[] as $d |       # for each diagonal...
    [ at($pt | addpt($d[])) ];  # ...gather its pair of tiles...
    sort | add == "MS"          # ...then check if they're M and S
  );

parsegrid |
reduce (check(scangrid) | select(.)) as $_ (
  0; . + 1
)
