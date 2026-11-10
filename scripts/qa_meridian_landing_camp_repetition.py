#!/usr/bin/env python3
"""Fail a Landing Camp ROM test if the *actual compiled map* repeats metatiles.

This is a structural gate, not a substitute for pixel-level visual review.
"""
import json
import struct
from collections import Counter
from pathlib import Path

root=Path(__file__).resolve().parents[1]
plan=json.loads((root/"data/meridian_plans/landing_camp_arrival.json").read_text())
w,h=plan["width"],plan["height"]
path=root/"data/layouts/MeridianLandingCampPrototype/map.bin"
words=struct.unpack("<"+str(w*h)+"H",path.read_bytes())
ids=[v&1023 for v in words]
counts=Counter(ids)
primary_path=root/"data/tilesets/primary/meridian_camp_environment/metatiles.bin"
if not primary_path.exists(): primary_path=root/"data/tilesets/primary/general/metatiles.bin"
primary=primary_path.read_bytes()
secondary=(root/"data/tilesets/secondary/meridian_shady_forest/metatiles.bin").read_bytes()
def signature(tile_id):
    source=primary if tile_id<512 else secondary
    index=tile_id if tile_id<512 else tile_id-512
    return source[index*16:(index+1)*16]
sig=[signature(v) for v in ids]
visual_counts=Counter(sig)
# Detect the exact visible checkerboard/repeated-solid problems from the last test.
solid_2x2=[]
runs=[]
for y in range(h-1):
 for x in range(w-1):
  i=y*w+x
  if sig[i]==sig[i+1]==sig[i+w]==sig[i+w+1]:
   solid_2x2.append([x,y,ids[i]])
for y in range(h):
 x=0
 while x<w:
  start=x
  while x<w and sig[y*w+x]==sig[y*w+start]:
   x+=1
  if x-start>=4:runs.append(["horizontal",start,y,x-start,ids[y*w+start]])
for x in range(w):
 y=0
 while y<h:
  start=y
  while y<h and sig[y*w+x]==sig[start*w+x]:
   y+=1
  if y-start>=4:runs.append(["vertical",x,start,y-start,ids[start*w+x]])
report={
 "map_metatile_count":w*h,
 "unique_metatile_count":len(counts),
 "unique_rendered_metatile_signatures":len(visual_counts),
 "top_metatile_counts":counts.most_common(12),
 "solid_2x2_count":len(solid_2x2),
 "solid_2x2_examples":solid_2x2[:20],
 "runs_4_or_more_count":len(runs),
 "runs_examples":runs[:20],
 "pass":len(visual_counts)>=16 and not solid_2x2 and not runs,
 "limitations":"Checks identical 2-layer metatile definitions; not visually similar textures or seams"
}
out=root/"build/meridian_candidate_review"
out.mkdir(parents=True,exist_ok=True)
(out/"repetition_gate_report.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
if not report["pass"]:
 raise SystemExit("REPETITION GATE FAILED: do not release another ROM with repeated solid terrain")
