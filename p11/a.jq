#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def digits: log10 + 1 | floor;

def step:
  digits as $d |
  if . == 0 then 1
  elif $d % 2 == 1 then . * 2024
  else
    pow(10; $d / 2) as $m |
    (. / $m | floor), . % $m
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
  end;

split(" ") | map(tonumber) |
map(first(. as $val | {} | evolve($val; 25))) |
add
