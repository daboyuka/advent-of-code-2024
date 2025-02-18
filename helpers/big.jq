include "./helpers";

def normbig: if length == 0 then [0] elif .[-1] == 0 then .[:-1] else . end;

def addbig($v):
  [ foreach (.[], 0) as $x (
    [0, $v];  # [output, carry]
    $x + .[1] | [. % 1e9, (. / 1e9 | floor)];
    .[0]
  ) ] |
  normbig;

def mulbig($v):
  [ foreach (.[], 0) as $x (
    [0, 0];  # [output, carry]
    $x * $v + .[1] | [. % 1e9, (. / 1e9 | floor)];
    .[0]
  ) ] |
  normbig;

def digitsbig:
  (length - 1) * 9 +
  (.[-1] | if . > 0 then log10 else 0 end + 1 | floor);

def tobig: . as $v | [] | addbig($v);

def tostringpad($d): tostring | "0" * ($d - length) + .;

def bigtostring:
  normbig | reverse | [ (.[0] | tostring), (.[1:][] | tostringpad(9)) ] | add;

def stringtobig:
  [ rpart(9) ] | map(tonumber) | reverse;
