#!/usr/bin/env python3
"""Validate third-party art provenance before any tileset import."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = ROOT / "data/meridian_plans/landing_camp_asset_inventory.json"
data = json.loads(manifest.read_text())
assert data["schema_version"] == 1
assert len(data["candidates"]) > 0
ids = set()
for item in data["candidates"]:
    assert item["id"] not in ids, "Duplicate asset candidate ID"
    ids.add(item["id"])
    assert item["source"].startswith("https://")
    assert item["license_status"] in ("unverified", "index_only", "permission_granted", "licensed")
    if item["import_allowed"]:
        assert item["license_status"] in ("permission_granted", "licensed"), item["id"]
        assert item["visual_approval"] is True, item["id"]
        assert item.get("original_asset_url", "").startswith("https://"), item["id"]
        assert item.get("credit_line", "").strip(), item["id"]
        assert item.get("license_evidence_url", "").startswith("https://"), item["id"]
        assert item.get("local_asset_path", "").strip(), item["id"]
print(f"Asset provenance gate passed: {len(ids)} candidates; {sum(x['import_allowed'] for x in data['candidates'])} authorized imports.")
