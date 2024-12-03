#!/usr/bin/env jq -s -R -r -f
include "./helpers";

lines | map(
  split("   ")
) |
transpose |
(
  .[1] | reduce .[] as $x (
    {};
    .[$x] += 1
  )
) as $table |
.[0] | map(
  tonumber * ($table[.] // 0)
)
