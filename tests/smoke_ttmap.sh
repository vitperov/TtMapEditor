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
echo "== delprop (remove additionalProperties) =="
DP="$WORK/dp.json"
tt new "$DP" --size 6 6 --base-prefab House
tt fill "$DP" --rect "0 0 6 6" --model Floor
tt setprop "$DP" --rect "0 0 6 6" --model Floor --prop internalTexture=floorWood1 --prop lootContainer=box
prop_count() {   # prop_count <map> <model> <propKey>  -> squares of model carrying that additionalProperty
  python3 "$TTMAP" dump "$1" --model "$2" --json 2>/dev/null | \
    python3 -c "import sys,json;print(sum(1 for s in json.load(sys.stdin) if '$3' in s.get('additionalProperties',{})))"
}
assert_eq "$(prop_count "$DP" Floor internalTexture)" "36" "delprop setup: 36 Floor carry internalTexture"
# delete one key -> the other survives
tt delprop "$DP" --rect "0 0 6 6" --model Floor --prop internalTexture
assert_eq "$(prop_count "$DP" Floor internalTexture)" "0"  "delprop --prop: internalTexture removed"
assert_eq "$(prop_count "$DP" Floor lootContainer)" "36"   "delprop --prop: lootContainer untouched"
# --all clears the rest; on save the additionalProperties key is omitted entirely
tt delprop "$DP" --rect "0 0 6 6" --model Floor --all
assert_eq "$(prop_count "$DP" Floor lootContainer)" "0" "delprop --all: every additionalProperty gone"
naked=$(python3 "$TTMAP" dump "$DP" --model Floor --json 2>/dev/null | \
  python3 -c "import sys,json;print(sum('additionalProperties' in s for s in json.load(sys.stdin)))")
assert_eq "$naked" "0" "delprop --all: additionalProperties key omitted on save"
# base props cannot be deleted (exit non-zero, model unchanged)
if tt delprop "$DP" --rect "0 0 6 6" --model Floor --prop model; then delok=yes; else delok=no; fi
assert_eq "$delok" "no" "delprop: refuses to delete a base prop (model)"
assert_eq "$(count "$DP" Floor)" "36" "delprop: base-prop guard left Floors intact"

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
echo "== insert / remove (grow & shrink, border-preserving) =="
G="$WORK/g.json"
tt new "$G" --size 10 8
tt fill "$G" --rect "0 0 10 8" --model Grass
tt border "$G" --rect "0 0 10 8" --model Forest --width 1
assert_eq "$(field "$G" width)"  "10" "insert: base width"
assert_eq "$(field "$G" height)" "8"  "insert: base height"
assert_eq "$(count "$G" Forest)" "32" "insert: base border ring (perimeter)"
# insert 2 rows in the middle, copying interior row 3 -> border ring preserved
tt insert "$G" --axis row --at 4 --count 2 --copy-from 3
assert_eq "$(field "$G" height)" "10" "insert rows: height 8 -> 10"
assert_eq "$(field "$G" width)"  "10" "insert rows: width unchanged"
assert_eq "$(count "$G" Forest)" "36" "insert --copy-from: border kept (32 + 2 rows*2 ends)"
assert_eq "$(squares_at "$G" "0 4 1 1")" "1" "insert --copy-from: one layer per new cell"
# insert 3 cols in the middle with --fill Grass
tt insert "$G" --axis col --at 5 --count 3 --fill Grass
assert_eq "$(field "$G" width)" "13" "insert cols --fill: width 10 -> 13"
# remove them again -> back to original interior size
tt remove "$G" --axis col --at 5 --count 3
assert_eq "$(field "$G" width)"  "10" "remove cols: width 13 -> 10"
tt remove "$G" --axis row --at 4 --count 2
assert_eq "$(field "$G" height)" "8"  "remove rows: height 10 -> 8"
assert_eq "$(count "$G" Forest)" "32" "remove: back to the original border ring"
# append at the far edge (POS == size)
tt insert "$G" --axis row --at 8 --count 1 --fill Grass
assert_eq "$(field "$G" height)" "9"  "insert at far edge (POS==size) appends"

echo ""
echo "== move (relocate + backfill origin + clear destination) =="
MV="$WORK/mv.json"
tt new "$MV" --size 20 20
tt fill "$MV" --rect "0 0 20 20" --model Grass
tt place "$MV" --at 2 2 --model house1          # house1 is 6x6
tt delete "$MV" --rect "2 2 6 6" --model Grass   # FixGrassUnderHouse convention
tt move "$MV" --from "2 2" --to "10 10" --model house1 --fill-old Grass --clear-new
assert_eq "$(count "$MV" house1)" "1" "move: house not duplicated"
assert_eq "$(squares_at "$MV" "10 10 1 1")" "1" "move: house sits at destination origin"
assert_eq "$(squares_at "$MV" "2 2 1 1")" "1" "move: origin cell holds one layer (grass)"
gold=$(python3 "$TTMAP" dump "$MV" --rect "2 2 6 6" --json 2>/dev/null | \
  python3 -c "import sys,json;print(sum(1 for s in json.load(sys.stdin) if s['model']=='Grass'))")
assert_eq "$gold" "36" "move --fill-old: origin 6x6 backfilled with Grass"
gnew=$(python3 "$TTMAP" dump "$MV" --rect "10 10 6 6" --json 2>/dev/null | \
  python3 -c "import sys,json;print(sum(1 for s in json.load(sys.stdin) if s['model']=='Grass'))")
assert_eq "$gnew" "0" "move --clear-new: destination 6x6 cleared of Grass"
# overlapping move (shift by 1) leaves no Grass under the house, backfills only the vacated column
tt move "$MV" --from "10 10" --to "11 10" --model house1 --fill-old Grass --clear-new
gover=$(python3 "$TTMAP" dump "$MV" --rect "11 10 6 6" --json 2>/dev/null | \
  python3 -c "import sys,json;print(sum(1 for s in json.load(sys.stdin) if s['model']=='Grass'))")
assert_eq "$gover" "0" "move overlap: no Grass under shifted house"
gcol=$(python3 "$TTMAP" dump "$MV" --rect "10 10 1 6" --json 2>/dev/null | \
  python3 -c "import sys,json;print(sum(1 for s in json.load(sys.stdin) if s['model']=='Grass'))")
assert_eq "$gcol" "6" "move overlap: vacated column backfilled with Grass"

echo ""
echo "== dump --model (find all of one type) / render =="
Q="$WORK/q.json"
tt new "$Q" --size 8 6
tt fill "$Q" --rect "0 0 8 6" --model Grass
tt border "$Q" --rect "0 0 8 6" --model Forest --width 1
# --model filters dump to just that type (JSON count unaffected by the text footer)
qf=$(python3 "$TTMAP" dump "$Q" --model Forest --json 2>/dev/null | \
  python3 -c "import sys,json;print(len(json.load(sys.stdin)))")
assert_eq "$qf" "24" "dump --model: finds all 24 Forest squares (perimeter of 8x6)"
qmix=$(python3 "$TTMAP" dump "$Q" --model Grass --json 2>/dev/null | \
  python3 -c "import sys,json;print(len(json.load(sys.stdin)))")
assert_eq "$qmix" "24" "dump --model: finds the 24 interior Grass squares"
# render: JSON grid is height rows wide by width, legend covers the models present
rrows=$(python3 "$TTMAP" render "$Q" --json 2>/dev/null | \
  python3 -c "import sys,json;print(len(json.load(sys.stdin)['rows']))")
assert_eq "$rrows" "6" "render: one row per map row (height)"
rw=$(python3 "$TTMAP" render "$Q" --json 2>/dev/null | \
  python3 -c "import sys,json;print(len(json.load(sys.stdin)['rows'][0]))")
assert_eq "$rw" "8" "render: each row is width chars wide"
rleg=$(python3 "$TTMAP" render "$Q" --json 2>/dev/null | \
  python3 -c "import sys,json;print(len(json.load(sys.stdin)['legend']))")
assert_eq "$rleg" "2" "render: legend lists the 2 models present (Grass, Forest)"
# a placed structure draws over the floor it sits on (object tier > ground tier)
R="$WORK/r.json"
tt new "$R" --size 6 6 --base-prefab House
tt fill "$R" --rect "0 0 6 6" --model Floor
tt place "$R" --at 2 2 --model Wall
wall_glyph=$(python3 "$TTMAP" render "$R" --json 2>/dev/null | \
  python3 -c "import sys,json;d=json.load(sys.stdin);print(d['rows'][2][2])")
assert_eq "$wall_glyph" "W" "render: Wall (object tier) shown over Floor (ground tier)"

echo ""
echo "== rotation-aware footprint (render / dump / move) =="
RT="$WORK/rt.json"
tt new "$RT" --size 16 16
tt fill "$RT" --rect "0 0 16 16" --model Grass
# shopSmall is 4x7; rotated 90 it occupies 7 wide x 4 tall on the grid.
tt place "$RT" --at 4 4 --model shopSmall --rotation 90
# render: the shop glyph's bounding box must be 7 wide x 4 tall (not the raw 4x7).
read shw shh < <(python3 "$TTMAP" render "$RT" --z 0 --json 2>/dev/null | python3 -c "
import sys,json
d=json.load(sys.stdin)
cells=[(x,y) for y,row in enumerate(d['rows']) for x,ch in enumerate(row) if ch in ('S','s')]
xs=[x for x,_ in cells]; ys=[y for _,y in cells]
print(max(xs)-min(xs)+1, max(ys)-min(ys)+1)")
assert_eq "$shw" "7" "render: rotated 4x7 shop draws 7 cells wide"
assert_eq "$shh" "4" "render: rotated 4x7 shop draws 4 cells tall"
# dump text shows the rotation-aware wxh (7x4), not the raw stored 4x7.
dwxh=$(python3 "$TTMAP" dump "$RT" --model shopSmall 2>/dev/null | grep -oE 'wxh=[0-9]+x[0-9]+' | head -1)
assert_eq "$dwxh" "wxh=7x4" "dump: text footprint is rotation-aware (7x4)"
# move bounds check uses the 7-wide footprint: to x=10 (10+7=17 > 16) is rejected.
if python3 "$TTMAP" move "$RT" --from "4 4" --to "10 4" --model shopSmall >/dev/null 2>&1; then
  moved_ok=yes; else moved_ok=no; fi
assert_eq "$moved_ok" "no" "move: rotated footprint bounds check rejects overflow"

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
