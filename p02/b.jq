#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def safe:
  pairwise | map(.[1] - .[0]) |             # convert to array of deltas
  (all(.[]; . < 0) or all(.[]; . > 0)) and  # ensure all positive or all negative
  all(.[] | abs; . >= 1 and . <= 3);        # ensure all between 1 and 3 (abs val)

def safe2:
  safe or  # safe as-is
  any(
    keys[] as $i | del(.[$i]);  # try deleting each element
    safe                        # and checking safety
  );

lines | map(
  split(" ") | map(tonumber) |  # convert to array of arrays of numbers
  select(safe2)                 # keep safe reports only
) |
length