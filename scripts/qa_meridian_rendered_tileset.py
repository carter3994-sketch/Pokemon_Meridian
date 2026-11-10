#!/usr/bin/env python3
"""Hard release gate: inspect *rendered* Landing Camp and registered tileset.

Runs after the engine-accurate map preview is generated. Exits nonzero on
repeated visual cells, blank tiles, or excessively low artwork diversity.
"""
from collections import Counter
from pathlib import Path
import json
import struct
from PIL import Image

root = Path(__file__).resolve().parents[1]
out = root / "build/meridian_candidate_review"
out.mkdir(parents=True, exist_ok=True)
plan = json.loads((root / "data/meridian_plans/landing_camp_arrival.json").read_text())
w, h = plan["width"], plan["height"]
preview = Image.open(out / "landing_camp_actual_engine_tiles_preview.png").convert("RGB")
assert preview.size == (w * 16, h * 16), "Rendered map dimensions incorrect"
raw = (root / "data/layouts/MeridianLandingCampPrototype/map.bin").read_bytes()
assert len(raw) == w * h * 2, "Map binary size mismatch"
ids = [v & 1023 for v in struct.unpack("<" + str(w * h) + "H", raw)]
metas = (root / "data/tilesets/secondary/meridian_shady_forest/metatiles.bin").read_bytes()
assert len(metas) == 512 * 16, "Secondary metatile bank must have exactly 512 entries"
tile_path=root/"data/tilesets/secondary/meridian_shady_forest/tiles.4bpp"
if not tile_path.exists(): tile_path=root/"build/meridian_shady_forest_staging/tiles.4bpp"
tiles=tile_path.read_bytes()
assert len(tiles) == 512 * 32, "Secondary graphics bank must have 512 8x8 tiles"
# A repeated-looking metatile with a different ID still hashes identically.
cells = [preview.crop((x*16,y*16,(x+1)*16,(y+1)*16)).tobytes()
         for y in range(h) for x in range(w)]
counts = Counter(cells)
blank = []
for i, pix in enumerate(cells):
    colors = set(preview.crop(((i%w)*16,(i//w)*16,(i%w+1)*16,(i//w+1)*16)).getdata())
    if len(colors) <= 1:
        blank.append([i%w, i//w, ids[i]])
blocks = []
for y in range(h-1):
    for x in range(w-1):
        i = y*w+x
        if cells[i] == cells[i+1] == cells[i+w] == cells[i+w+1]:
            blocks.append([x,y,ids[i]])
runs = []
for y in range(h):
    x = 0
    while x < w:
        start = x
        while x < w and cells[y*w+x] == cells[y*w+start]:
            x += 1
        if x-start >= 4:
            runs.append(["horizontal",start,y,x-start,ids[y*w+start]])
for x in range(w):
    y = 0
    while y < h:
        start = y
        while y < h and cells[y*w+x] == cells[start*w+x]:
            y += 1
        if y-start >= 4:
            runs.append(["vertical",x,start,y-start,ids[start*w+x]])
# Report tile-bank duplicates, but reject only duplicates actually creating
# unacceptable repetition in the assembled map.
definitions = [metas[i*16:(i+1)*16] for i in range(512)]
duplicates = sum(n-1 for n in Counter(definitions).values() if n > 1)
report = {
    "gate": "rendered-pixel-tileset-and-map",
    "total_cells": w*h,
    "distinct_rendered_cells": len(counts),
    "distinct_metatile_ids": len(set(ids)),
    "secondary_duplicate_metatile_definitions": duplicates,
    "solid_color_cells": len(blank),
    "solid_color_examples": blank[:30],
    "identical_2x2_blocks": len(blocks),
    "identical_2x2_examples": blocks[:30],
    "identical_runs_length_4_plus": len(runs),
    "identical_run_examples": runs[:30],
    "max_identical_cell_coverage_percent": round(max(counts.values())*100/(w*h),2),
    "limits": {
        "min_distinct_rendered_cells": 16,
        "max_identical_2x2_blocks": 0,
        "max_identical_runs_length_4_plus": 0,
        "max_solid_color_cells": 0,
        "max_single_cell_coverage_percent": 20
    },
}
reasons = []
if len(counts) < 16: reasons.append("Too few distinct rendered metatiles")
if blocks: reasons.append("Repeated 2x2 visual blocks")
if runs: reasons.append("Repeated visual runs of four or more")
if blank: reasons.append("Solid-color/blank visual metatiles")
if report["max_identical_cell_coverage_percent"] > 20:
    reasons.append("One visual metatile covers more than 20% of the map")
report["pass"] = not reasons
report["rejection_reasons"] = reasons
report["scope"] = "Exact RGB pixel equality; similar-looking nonidentical textures and poor artistic transitions still need visual review"
(out / "rendered_tileset_quality_gate.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
if reasons:
    raise SystemExit("REJECTED: " + "; ".join(reasons))
