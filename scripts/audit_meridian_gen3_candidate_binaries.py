#!/usr/bin/env python3
"""Validate a complete Gen 3 community secondary tileset before engine staging.

Read-only: downloads candidate binaries to build/, never changes engine assets.
"""
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build/meridian_candidate_review"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://raw.githubusercontent.com/TeamAquasHideout/Team-Aquas-Asset-Repo/master/Tilesets/The Great Tileset Exchange/Full Tilesets/"
SETS = ("Shady Forest Secondary", "Autumn Ruins Secondary")
MAX_BYTES = 8 * 1024 * 1024

def fetch(name, path):
    url = quote(BASE + name + "/" + path, safe=":/")
    with urlopen(Request(url, headers={"User-Agent": "Meridian-Compatibility-Audit/1.0"}), timeout=35) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"Oversized asset: {name}/{path}")
    return data

def inspect(name):
    files = {f: fetch(name, f) for f in ("tiles.4bpp", "metatiles.bin", "metatile_attributes.bin")}
    sizes = {k: len(v) for k,v in files.items()}
    assert sizes["tiles.4bpp"] % 32 == 0, (name, "4bpp tile alignment", sizes)
    assert sizes["metatiles.bin"] % 16 == 0, (name, "metatile alignment", sizes)
    count = sizes["metatiles.bin"] // 16
    attr_len = sizes["metatile_attributes.bin"]
    assert attr_len % 2 == 0 and attr_len <= count * 4, (name, "attribute data invalid", attr_len, count)
    tile_count = sizes["tiles.4bpp"] // 32
    # Each metatile contains 8 tile references; low ten bits index 8x8 tiles.
    import struct
    refs = struct.unpack("<" + "H" * (len(files["metatiles.bin"]) // 2), files["metatiles.bin"])
    max_ref = max((v & 0x3FF) for v in refs) if refs else 0
    # Secondary tilesets may reference tiles from the primary bank; report, do not reject.
    report = {"name": name, "source": BASE + name, "sizes_bytes": sizes,
              "tile_8x8_count": tile_count, "metatile_16x16_count": count,
              "attribute_file_bytes": attr_len,
              "attribute_entries_if_2_bytes": attr_len // 2,
              "attribute_entries_if_4_bytes": attr_len // 4,
              "attributes_cover_all_metatiles": attr_len in (count * 2, count * 4),
              "maximum_8x8_tile_reference": max_ref,
              "may_reference_primary_tiles": max_ref >= tile_count,
              "status": "binary_structure_checked_not_engine_imported",
              "permission_and_visual_approval": "pending"}
    return report

reports = [inspect(name) for name in SETS]
(OUT / "gen3_binary_compatibility.json").write_text(json.dumps(reports, indent=2) + "\n")
print(json.dumps(reports, indent=2))
