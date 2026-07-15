#!/usr/bin/env bash
#
# Smoke test for ttmap.py - exercises every command against throwaway maps and
# asserts on counts, geometry and diff cleanliness. Self-contained: builds all
# its own maps (no dependency on the Unity project) and overrides generator
# settings via --set so results do not depend on generatorsSettings.json.
#
# Usage:  ./tests/smoke_ttmap.sh
# Exit code 0 = all passed, 1 = at least one failure.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EDITOR_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TTMAP="$EDITOR_ROOT/ttmap.py"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

pass=0
fail=0

# --- helpers --------------------------------------------------------------- #

tt() { python3 "$TTMAP" "$@" >/dev/null 2>&1; }   # run a mutating command quietly

count() {   # count <map> <model> [z]   -> number of that model at z-level (default 0)
  python3 "$TTMAP" describe "$1" --json 2>/dev/null | \
    python3 -c "import sys,json;d=json.load(sys.stdin);print(d['counts'].get('${3:-0}',{}).get('$2',0))"
}

field() {   # field <map> <key>   -> top-level describe field (width/height/basePrefab)
  python3 "$TTMAP" describe "$1" --json 2>/dev/null | \
    python3 -c "import sys,json;print(json.load(sys.stdin)['$2'])"
}

rot_count() {   # rot_count <map> "x y w h" <rotation>   -> squares in rect with that rotation
  python3 "$TTMAP" dump "$1" --rect "$2" --json 2>/dev/null | \
    python3 -c "import sys,json;print(sum(1 for s in json.load(sys.stdin) if s.get('rotation')=='$3'))"
}

squares_at() {   # squares_at <map> "x y w h"   -> number of squares in rect (all layers)
  python3 "$TTMAP" dump "$1" --rect "$2" --json 2>/dev/null | \
    python3 -c "import sys,json;print(len(json.load(sys.stdin)))"
}

diff_lines() { diff "$1" "$2" | grep -cE '^[<>]' || true; }

assert_eq() {   # assert_eq <actual> <expected> <msg>
  if [ "$1" = "$2" ]; then pass=$((pass+1)); echo "  PASS  $3  ($1)"
  else fail=$((fail+1)); echo "  FAIL  $3  (got '$1', want '$2')"; fi
}
assert_ge() {   # assert_ge <actual> <min> <msg>
  if [ "$1" -ge "$2" ] 2>/dev/null; then pass=$((pass+1)); echo "  PASS  $3  ($1 >= $2)"
  else fail=$((fail+1)); echo "  FAIL  $3  ($1 < $2)"; fi
}
assert_le() {   # assert_le <actual> <max> <msg>
  if [ "$1" -le "$2" ] 2>/dev/null; then pass=$((pass+1)); echo "  PASS  $3  ($1 <= $2)"
  else fail=$((fail+1)); echo "  FAIL  $3  ($1 > $2)"; fi
}

# --------------------------------------------------------------------------- #
echo "ttmap smoke test  (workdir: $WORK)"
echo "editor root:      $EDITOR_ROOT"

echo ""
echo "== new / fill / border =="
T="$WORK/t.json"
tt new "$T" --size 20 12
assert_eq "$(field "$T" width)"  "20"   "new: width"
assert_eq "$(field "$T" height)" "12"   "new: height"
assert_eq "$(field "$T" basePrefab)" "None" "new: terrain basePrefab is null"
tt fill "$T" --rect "0 0 20 12" --model Grass
assert_eq "$(count "$T" Grass)" "240"   "fill: 20x12 all Grass"
tt border "$T" --rect "0 0 20 12" --model Forest --width 2
assert_eq "$(count "$T" Forest)" "112"  "border: width-2 ring (240 - 16*8)"
assert_eq "$(count "$T" Grass)"  "128"  "border: interior Grass remains"

echo ""
echo "== place (stacks a layer) =="
tt place "$T" --at 10 6 --model Berries
assert_eq "$(count "$T" Berries)" "1"   "place: one Berries added"
assert_eq "$(count "$T" Grass)"   "128" "place: does NOT remove underlying Grass"
assert_eq "$(squares_at "$T" "10 6 1 1")" "2" "place: two layers now at (10,6)"

echo ""
echo "== setprop / delete =="
tt setprop "$T" --rect "0 0 20 2" --model Forest --prop rotation=90
assert_eq "$(rot_count "$T" "0 0 20 2" 90)" "40" "setprop: 40 top Forest cells rotated 90"
tt delete "$T" --rect "0 0 20 2" --model Forest
assert_eq "$(count "$T" Forest)" "72"   "delete: 40 Forest removed (112 -> 72)"

echo ""
echo "== diff cleanliness (position-preserving fill) =="
D="$WORK/d.json"; D0="$WORK/d0.json"; D1="$WORK/d1.json"
tt new "$D" --size 20 12
tt fill "$D" --rect "0 0 20 12" --model Grass
cp "$D" "$D0"
tt fill "$D" --rect "5 5 3 3" --model Forest      # 9 cells Grass -> Forest
n=$(diff_lines "$D0" "$D")
assert_ge "$n" "1"  "fill diff: change is recorded"
assert_le "$n" "72" "fill diff: no reordering (<= 9 cells * 8, would be ~200 if reordered)"
cp "$D0" "$D1"
tt fill "$D1" --rect "8 5 2 2" --model Grass       # Grass over Grass = no-op
assert_eq "$(diff_lines "$D0" "$D1")" "0" "fill diff: true no-op is byte-identical"

echo ""
echo "== wall-frame / roof-frame (house) =="
H="$WORK/h.json"
tt new "$H" --size 10 8 --base-prefab House
assert_eq "$(field "$H" basePrefab)" "House" "new: house basePrefab"
tt fill "$H" --rect "0 0 10 8" --model Floor
tt wall-frame "$H" --rect "0 0 10 8"
assert_eq "$(count "$H" Corner 0)" "4"  "wall-frame: 4 corners"
assert_eq "$(count "$H" Wall 0)"   "28" "wall-frame: 28 walls (perimeter 32 - 4)"
tt roof-frame "$H" --rect "0 0 10 8" --z 1
assert_eq "$(count "$H" RoofCorner 1)"  "4"  "roof-frame: 4 roof corners at z=1"
assert_eq "$(count "$H" PitchedRoof 1)" "28" "roof-frame: 28 pitched roof at z=1"
H2="$WORK/h2.json"
tt new "$H2" --size 10 8 --base-prefab House
tt fill "$H2" --rect "0 0 10 8" --model Floor
tt roof-frame "$H2" --rect "0 0 10 8" --z 1 --half
assert_eq "$(count "$H2" RoofCornerHalf 1)"  "4"  "roof-frame --half: 4 half corners"
assert_eq "$(count "$H2" PitchedRoofHalf 1)" "28" "roof-frame --half: 28 half pitched"

echo ""
echo "== generators (generate / clear, --set overrides) =="
SK="$WORK/sk.json"
tt new "$SK" --size 8 8
tt generate "$SK" --name MapSkeletonGenerator \
  --set landLotsRows=2 --set landLotsColumns=3 \
  --set landLotWidth=10 --set landLotHeight=8 \
  --set forestAroundMap=3 --set roadWidth=2
assert_eq "$(count "$SK" LandLot 0)" "6" "MapSkeleton: 2x3 land lots"
assert_ge "$(count "$SK" Grass 0)"  "1" "MapSkeleton: has Grass"
assert_ge "$(count "$SK" Road 0)"   "1" "MapSkeleton: has Road"
forest_before=$(count "$SK" Forest 0)
tt generate "$SK" --name ForestGenerator --set forestProbability=1.0
forest_after=$(count "$SK" Forest 0)
assert_ge "$forest_after" "$((forest_before + 1))" "ForestGenerator: added trees in lots"

tt generate "$SK" --name FogGenerator --set intervalSquares=5
assert_ge "$(count "$SK" Fog 0)" "1" "FogGenerator: placed fog"
tt clear "$SK" --name FogGenerator
assert_eq "$(count "$SK" Fog 0)" "0" "clear FogGenerator: removeAllMapObjects path (Step 1 fix)"

tt generate "$SK" --name BerriesGenerator --set probability=1.0
assert_ge "$(count "$SK" Berries 0)" "1" "BerriesGenerator: placed berries"
tt clear "$SK" --name BerriesGenerator
assert_eq "$(count "$SK" Berries 0)" "0" "clear BerriesGenerator: removed berries"

echo ""
echo "== --out (does not touch the input) =="
O="$WORK/o.json"
tt new "$O" --size 6 6
tt fill "$O" --rect "0 0 6 6" --model Grass
cp "$O" "$WORK/o_before.json"
tt fill "$O" --rect "0 0 6 6" --model Forest --out "$WORK/o_out.json"
assert_eq "$(diff_lines "$O" "$WORK/o_before.json")" "0" "--out: input left unchanged"
assert_eq "$(count "$WORK/o_out.json" Forest)" "36" "--out: result written to --out path"

echo ""
echo "=========================================="
echo "  PASSED: $pass    FAILED: $fail"
echo "=========================================="
[ "$fail" -eq 0 ]
