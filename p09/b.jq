#!/usr/bin/env jq -s -R -r -f
include "./helpers";

def parse:
  def _todisk($fidx):
    if length == 0 then []
    else
      [[$fidx, .[0], .[1] // 0]] +
      (.[2:] | _todisk($fidx+1))
    end;

  lines[0] | split("") | map(tonumber) | _todisk(0);

def score:
  reduce .[] as [$fidx, $alloc, $free] (
    {pos: 0, sum: 0};
    .sum += $fidx * (2*.pos + $alloc - 1) * $alloc / 2 |
    .pos += $alloc + $free
  ) |
  .sum;

def compact:
  def _find($size):
    if length == 0 then 0
    else
      first as [$fidx, $alloc, $free] |
      if $free >= $size then 0
      else .[1:] | 1 + _find($size) end
    end;

  def _pushalloc($fidx2; $alloc2):
    .[0] as [$fidx, $alloc, $free] |
    [ [$fidx, $alloc, 0], [$fidx2, $alloc2, $free-$alloc2] ];

  def _popalloc($alloc2; $free2):
    .[0] as [$fidx, $alloc, $free] |
    [ [$fidx, $alloc, $free+$alloc2+$free2] ];

  def _compact($target):
    debugtee($target) |
    if length == 0 then .
    else
      last as [$fidx, $alloc, $free] |
      if $fidx != $target then
        .[:-1] |= _compact($target)  # not eligible to move -> skip, compact the rest
      else
        _find($alloc) as $pos |
        if $pos >= length-1 then
          .[:-1] |= _compact($target-1)  # no free spot to move -> keep, compact the rest
        else
          .[-2:] |= _popalloc($alloc; $free)  |          # pop last (move freespace to prior)
          .[$pos:$pos+1] |= _pushalloc($fidx; $alloc) |  # push alloc into earlier slot
          .[_find(1):] |= _compact($target-1)
        end
      end
    end;

  _compact(length-1);

parse | compact | score
