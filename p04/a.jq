#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/grid";

def dirs: [0,0] | nbr8;

def check($pt; $d):
    [  # list all tiles
      at(
        $pt |  # ...starting from pt...
        addpt($d | mulpt(range(4)))  # ...for 4 tiles in dir $d
      )
    ] |
    add == "XMAS"  # concat and check
;

parsegrid |
reduce (check(scangrid; dirs) | select(.)) as $_ (
  0; . + 1
)
