#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/grid";

def antis($gdims):
  # _antis takes an input point and streams points offset
  # by 0 or more $delta until out of bounds
  def _antis($delta):
    if inrange([0, 0]; $gdims) then        # only continue if in bounds
      ., (addpt($delta) | _antis($delta))  # produce current point plus recurse after offset by $delta
    else empty end;

  . as [$a, $b] |                      # unpack input points
  ($a | subpt($b)) as $delta |         # compute delta
  $a | _antis($delta | mulpt(1, -1));  # start from $a and recurse in both directions until out of bounds

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

