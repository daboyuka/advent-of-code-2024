include "./helpers";

def parsegrid: lines | map(split(""));
def parsenumgrid: lines | map(split("")|map(tonumber));

def rendergrid: map(join("")) | join("\n");

def griddims: [., .[0] | length];  # returns [rows, cols]

def inrange($startpt; $endpt):
  .[0] >= $startpt[0] and .[0] < $endpt[0] and
  .[1] >= $startpt[1] and .[1] < $endpt[1];

def inbounds($pt):
  griddims as $endpt |
  $pt | inrange([0, 0]; $endpt)
;

def at($p):
  if inbounds($p) then .[$p[0]][$p[1]]
  else null end
;

def set($p; $to): .[$p[0]][$p[1]] = $to;

# output: all coordinates between $startpt (incl.) and $endpt (excl.)
def scanpoints($startpt; $endpt):
  (range($startpt[0]; $endpt[0])|[.]) + (range($startpt[1]; $endpt[1])|[.])
;
# input: grid, output: all coordinates
def scangrid: scanpoints([0, 0]; griddims);

def visitpoints($startpt; $endpt):
  range($startpt[0]; $endpt[0]) as $r |
  range($startpt[1]; $endpt[1]) as $c |
  [$r, $c] as $pt |
  [$pt, at($pt)];

def visitgrid: visitpoints([0, 0]; griddims);

def nbr4: .[0] += (-1, 1), .[1] += (-1, 1);
def nbr8: nbr4, ( .[0] += (-1, 1) | .[1] += (-1, 1) );

def addpt($delta): [.[0] + $delta[0], .[1] + $delta[1]];
def subpt($delta): [.[0] - $delta[0], .[1] - $delta[1]];
def mulpt($x): [.[0] * $x, .[1] * $x];
