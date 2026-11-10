#!/usr/bin/env python3
"""Download publicly visible example images for review, never install into the game."""
from io import BytesIO
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build/meridian_candidate_review"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://raw.githubusercontent.com/TeamAquasHideout/Team-Aquas-Asset-Repo/master/Tilesets/The Great Tileset Exchange/Full Tilesets/"
CANDIDATES = ("Shady Forest Secondary", "Autumn Ruins Secondary")
panels = []
results = []
for name in CANDIDATES:
    url = quote(BASE + name + "/example.png", safe=":/")
    record = {"name": name, "source_url": url, "approved_for_import": False}
    try:
        req = Request(url, headers={"User-Agent": "Meridian-Art-Review/1.0"})
        with urlopen(req, timeout=30) as response:
            payload = response.read(12 * 1024 * 1024 + 1)
        if len(payload) > 12 * 1024 * 1024:
            raise ValueError("Image exceeds 12MB review limit")
        img = Image.open(BytesIO(payload))
        img.load()
        record["source_size"] = list(img.size)
        img = img.convert("RGBA")
        img.thumbnail((640, 420), Image.Resampling.NEAREST)
        img.save(OUT / (name.lower().replace(" ", "_") + "_example.png"))
        panels.append((name, img.convert("RGB")))
        record["status"] = "downloaded"
    except Exception as exc:
        record["status"] = "download_failed"
        record["error"] = str(exc)
    results.append(record)
(OUT / "source_report.json").write_text(json.dumps(results, indent=2) + "\n")
if not panels:
    raise SystemExit("No candidate examples downloaded; see source_report.json")
sheet = Image.new("RGB", (720, 480 * len(panels)), (245, 245, 245))
draw = ImageDraw.Draw(sheet)
for index, (name, img) in enumerate(panels):
    y = index * 480
    draw.text((20, y + 14), name + " — REFERENCE ONLY / NOT CLEARED FOR IMPORT", fill=(20, 20, 20))
    sheet.paste(img, (20, y + 45))
sheet.save(OUT / "candidate_contact_sheet.png")
print(json.dumps(results, indent=2))
