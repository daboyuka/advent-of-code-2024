#!/usr/bin/env jq -s -R -r -f
include "./helpers";
include "./helpers/grid";

# scanheight is as scangrid but only returns points where the tile == $h
# input: grid, output: stream of points
def scanheight($h):
  visitgrid | select(.[1] == $h) | .[0];

def populate($h; $g):
  # input: score table, output: rating at $pt if at height $h or null otherwise
  def _ratingpt($pt; $h):
    if $g | at($pt) != $h then 0
    else .[$pt|tostring] end;

  # input: score table, output: sum of rating of neighbors of $pt at height $h or null otherwise
  def _ratingnbrs($pt; $h):
    [ _ratingpt($pt | nbr4; $h) ] | add;

  reduce ($g | scanheight($h)) as $pt (  # iterate over points at height
    .;
    ($pt | tostring) as $key |
    if $h == 9 then .[$key] = 1                # if height 9, return rating 1
    else .[$key] = _ratingnbrs($pt; $h+1) end  # otherwise, return sum of ratings of next-higher neighbors
  );

parsegrid |
map(map(tonumber? // null)) | . as $g |  # convert grid to numbers and capture as $g
reduce range(9; -1; -1) as $h (  # build up score table from height 9 down to 0
  {}; populate($h; $g)
) |
reduce (.[$g | scanheight(0) | tostring]) as $rating (  # add up ratings for all height 0 tiles
  0; . += $rating
)
