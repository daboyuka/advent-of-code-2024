#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def reorder($rules):
  if length < 2 then .
  else
    first as $v1 |
    reduce .[1:][] as $v2 (
      [[], []];
      if any($rules[]; . == [$v1, $v2]) then .[1] += [$v2]
      else .[0] += [$v2] end
    ) |
    map(reorder($rules)) |
    [.[0][], $v1, .[1][]]
  end;

linegroups |
(.[0] | map(split("|"))) as $rules |  # parse out the rules section
.[1] | map(                       # handle sequences
  split(",") |                    # split on commas
  select(. == reorder($rules)) |  # keep safe sequences
  .[length/2] | tonumber          # take middle element and convert to number
) |
add  # add up middle elements



