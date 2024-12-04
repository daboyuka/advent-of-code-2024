#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def parsecmds:
  capture("(?<c>mul|do|don't)\\((?:(?<x>\\d+),(?<y>\\d+))?\\)"; "g") |  # find cmd patterns
  (.x, .y) |= tonumber?  # convert to numbers
;

reduce parsecmds as {$c, $x, $y} (
    {v: 0, enable: true};
    if $c == "do" and $x == null and $y == null then
      .enable = true
    elif $c == "don't" and $x == null and $y == null then
      .enable = false
    elif $c == "mul" and .enable and $x != null and $y != null then
      .v += $x * $y
    else
      .
    end
) |
.v
