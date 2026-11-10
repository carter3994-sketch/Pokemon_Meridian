#!/usr/bin/env python3
"""Audit Landing Camp geography before replacing the placeholder metatiles."""
from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "data/meridian_plans/landing_camp_arrival.json").read_text())
W, H = PLAN["width"], PLAN["height"]
rows = PLAN["rows"]
assert len(rows) == H and all(len(row) == W for row in rows)
classes = {
    "forest": "T", "cliffs": "^", "ruins": "R",
    "water": "~", "dock": "D", "path": "=+12345AF",
    "open_ground": ".", "medical": "M", "research": "L",
    "headquarters": "H", "cave": "C", "supply": "S", "quarters": "Q",
}
reverse = {}
for role, chars in classes.items():
    for c in chars:
        assert c not in reverse, (c, role, reverse.get(c))
        reverse[c] = role
unknown = set("".join(rows)) - set(reverse)
assert not unknown, f"Unclassified terrain: {unknown}"
counts = Counter(reverse[c] for row in rows for c in row)
assert sum(counts.values()) == W*H
landmarks = {}
for name, coords in PLAN["landmarks"].items():
    x,y = coords
    assert 0 <= x < W and 0 <= y < H, (name, coords)
    landmarks[name] = {"x": x, "y": y, "symbol": rows[y][x], "terrain": reverse[rows[y][x]]}
edges = Counter()
for y in range(H):
    for x in range(W):
        for xx,yy in ((x+1,y),(x,y+1)):
            if xx >= W or yy >= H: continue
            a,b = reverse[rows[y][x]],reverse[rows[yy][xx]]
            if a != b:
                edges[" / ".join(sorted((a,b)))] += 1
report = {
    "source": "data/meridian_plans/landing_camp_arrival.json",
    "map_size_metatiles": [W,H],
    "terrain_metatile_counts": dict(sorted(counts.items())),
    "landmarks": landmarks,
    "terrain_adjacency_edges": dict(sorted(edges.items(), key=lambda p:(-p[1],p[0]))),
    "art_direction": {
        "base": "Shady Forest as atmospheric reference, subject to approval and artist permissions",
        "accent": "Autumn Ruins stonework as reference only; recolor to match cool woodland palette",
        "harbor": "Separate coastal and vessel art needed; no approved source",
        "resolution": "16x16 metatile map / GBA 8x8 4bpp source tiles",
        "critical_transitions": ["forest / open_ground", "cliffs / open_ground", "water / open_ground", "dock / water", "ruins / cliffs"],
        "visual_review_required": True,
        "third_party_art_imported": False
    }
}
OUT = ROOT / "build/meridian_candidate_review/landing_camp_terrain_audit.json"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps({"counts":report["terrain_metatile_counts"],"top_edges":list(report["terrain_adjacency_edges"].items())[:8]},indent=2))
