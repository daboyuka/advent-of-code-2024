#!/usr/bin/env jq -s -R -r -f
include "./helpers";

[
  capture("mul\\((?<x>\\d+),(?<y>\\d+)\\)"; "g") |  # find mul patterns
  map_values(tonumber)                              # convert to numbers
] |
map(.x * .y) | add  # compute products and sum
