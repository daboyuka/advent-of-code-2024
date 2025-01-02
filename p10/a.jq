#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/grid";

# scanheight is as scangrid but only returns points where the tile == $h
# input: grid, output: stream of points
def scanheight($h):
  visitgrid | select(.[1] == $h) | .[0];

def populate($h; $g):
  # input: score table, output: scoreset at $pt if at height $h or null otherwise
  def _scorept($pt; $h):
    if $g | at($pt) != $h then null
    else .[$pt|tostring] end;

  # input: score table, output: union of scoresets of neighbors of $pt at height $h or null otherwise
  def _scorenbrs($pt; $h):
    [ _scorept($pt | nbr4; $h) ] | add;

  reduce ($g | scanheight($h)) as $pt (  # iterate over points at height
    .;
    ($pt | tostring) as $key |
    if $h == 9 then .[$key] = {$key:true}     # if height 9, return identity scoreset
    else .[$key] = _scorenbrs($pt; $h+1) end  # otherwise, return union of scoresets of next-higher neighbors
  );

parsegrid |
map(map(tonumber? // null)) | . as $g |  # convert grid to numbers and capture as $g
reduce range(9; -1; -1) as $h (  # build up score table from height 9 down to 0
  {}; populate($h; $g)
) |
reduce (.[$g | scanheight(0) | tostring] | length) as $score (  # add up scoresets sizes for all height 0 tiles
  0; . += $score
)
