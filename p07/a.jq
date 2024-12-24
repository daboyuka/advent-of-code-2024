#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def parse:
  split(": ") |
  .[0] |= tonumber |
  .[1] |= (split(" ") | map(tonumber));

def check:
  def _check($cur; $target):
    if length == 0 then $cur == $target
    elif $cur > $target then false
    else
      [
        (.[0] * $cur, .[0] + $cur) as $next |
        .[1:] | _check($next; $target)
      ] | any
    end;
  . as [$target, $seq] |
  $seq[1:] |
  _check($seq[0]; $target);

lines | map(
  parse |
  select(check) |
  .[0]
) | add
