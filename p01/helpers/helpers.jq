#
# Input
#

# Splits input as per -sR into non-empty lines
def lines: split("\n") | map(select(. != "")) ;

def htmlunescape: gsub("&gt;" ; ">") | gsub("&lt;" ; "<") ;

def linegroups:
  reduce split("\n")[] as $line ( [[]] ;
    if $line == "" then . + [[]]
    else                .[-1] += [$line]
    end
  ) |
  map(select(length > 0)) # only keep non-empty linegroups
;

#
# Math
#

def sgn: if . < 0 then -1 elif . > 0 then 1 else 0 end;

#
# Functional
#

# iterate application of f for $n times
# $n == 0 -> . , 1 -> f, 2 -> f|f, ...
def iterf($n; f): if $n == 0 then . else f | iterf($n-1; f) end;

#
# Debug
#

# debugtee is like debug, except values are filtered by "what" before writing to stderr
# (valuess still flow through unaffected).
def debugtee(what):
  (
    [what] |
    if length > 1 then map(tostring) | join(" ")
    else . end |
    debug |
    empty
  ), .
;

def assert(f; err; $loc):
    (if $loc then "\($loc.file):\($loc.line): " else "" end) as $pre |
    ( f // error($pre + (err|tostring)) | empty ), .;
def assert(f; err): assert(f; err; null);

def asserttype($t; $loc): assert(type == $t; "expected \($t), got \(type)"; $loc);
def asserttype($t): asserttype($t; null);
