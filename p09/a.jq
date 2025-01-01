#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def parse:
  def _todisk($fidx):
    if length == 0 then []
    else
      [
        (range(.[0]) | $fidx),
        (range(.[1] // 0) | null)
      ] +
      (.[2:] | _todisk($fidx+1))
    end;

  lines[0] | split("") | map(tonumber) | _todisk(0);

def compact:
  if length == 0 then .
  else
    .[-1] as $last |
    index(null) as $fidx |
    if $last == null then .[:-1] | compact
    elif $fidx == null then .
    else .[:$fidx] + [$last] + (.[$fidx+1:-1] | compact) end
  end;

def compact2:
  if length == 0 then empty
  elif .[0] != null then
    .[0], (.[1:] | compact2)
  elif .[-1] == null then
    .[:-1] | compact2
  else
    .[-1], (.[1:-1] | compact2)
  end;

def score: to_entries | map(.key * .value) | add;

parse | [ compact2 ] | debug | score
