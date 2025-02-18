#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/big";

def step:
  digitsbig as $d |
  if . == [] or . == [0] then [1]
  elif $d % 2 == 1 then mulbig(2024)
  else
    bigtostring |
    length as $l | .[$l/2:], .[:$l/2] |
    stringtobig
  end;

# input: memo table, output: nstones, updated memo table
def evolve($val; $depth):
  if $depth == 0 then 1, .
  else
    ([$val, $depth] | tostring) as $k |
    if .[$k] != null then .[$k], .
    else
      reduce ($val | step) as $val2 (
        [0, .];
        [ .[1] | evolve($val2; $depth - 1) ] as [$nstones, $memo] |
        .[0] += $nstones |
        .[1] = $memo
      ) |
      .[0], .[1] + {$k: .[0]}
    end
  end |
  if $depth > 60 then debugtee($depth) else . end;

split(" ") | map(tonumber | tobig) |
map(first(. as $val | {} | evolve($val; 75))) |
add
