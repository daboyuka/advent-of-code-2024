#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/grid";

def antis($gdims):
  . as [$a, $b] |
    ($a | mulpt(2) | subpt($b)),
    ($b | mulpt(2) | subpt($a)) |
  select(inrange([0, 0]; $gdims));

def towers:
  reduce visitgrid as [$pt, $t] (
    {};
    if $t != "." then .[$t] += [$pt]
    else . end
  );

def combos:
  range(length) as $i |
  range($i+1; length) as $j |
  [.[$i, $j]];

parsegrid | griddims as $gdims | towers | map(
  combos | antis($gdims)
) |
unique |
length

