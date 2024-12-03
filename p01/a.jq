#!/usr/bin/env jq -s -R -r -f
include "./helpers";

lines | map(
  split("   ") | map(tonumber)
) |
transpose | map(sort) | transpose |
map(.[1] - .[0] | abs) |
add
