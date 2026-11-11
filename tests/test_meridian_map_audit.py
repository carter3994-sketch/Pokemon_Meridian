"""Exercise the audit CLI against isolated Porymap registry fixtures."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

AUDIT = Path(__file__).resolve().parents[1] / "tools/meridian_map_audit.py"


class MapRegistryAuditTests(unittest.TestCase):
    def run_audit(self, connection=None, warps=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            shutil.copyfile(AUDIT, root / "tools/meridian_map_audit.py")
            (root / "data/maps/Camp").mkdir(parents=True)
            (root / "data/layouts").mkdir(parents=True)
            fixtures = {
                "data/maps/map_groups.json": {"group_order": ["g"], "g": ["Camp"]},
                "data/layouts/layouts.json": {"layouts": [{"id": "LAYOUT_CAMP", "width": 8, "height": 8}]},
                "data/maps/Camp/map.json": {"id": "MAP_CAMP", "layout": "LAYOUT_CAMP", "connections": connection, "warp_events": warps or []},
            }
            for name, content in fixtures.items():
                (root / name).write_text(json.dumps(content))
            result = subprocess.run([sys.executable, str(root / "tools/meridian_map_audit.py")], capture_output=True, text=True)
            report = json.loads((root / "build/meridian_map_audit/report.json").read_text())
            return result, report

    def test_null_connections_produce_successful_report(self):
        result, report = self.run_audit(None)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["total_connections"], 0)
        self.assertEqual(report["errors"], [])

    def test_registered_connection_is_resolved_by_map_id(self):
        result, report = self.run_audit([{"map": "MAP_CAMP"}])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["total_connections"], 1)

    def test_unknown_connection_fails_with_report(self):
        result, report = self.run_audit([{"map": "MAP_MISSING"}])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["errors"], ["MAP_CAMP: connection references unregistered map MAP_MISSING"])

    def test_warp_destination_accepts_string_and_integer_indexes(self):
        for index in ("0", 0):
            with self.subTest(index=index):
                result, report = self.run_audit(warps=[{"dest_map": "MAP_CAMP", "dest_warp_id": index}])
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(report["total_warps"], 1)

    def test_dynamic_warp_is_explicitly_not_resolved(self):
        result, report = self.run_audit(warps=[{"dest_map": "MAP_DYNAMIC", "dest_warp_id": "-1"}])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["dynamic_warps_not_statically_resolved"], 1)

    def test_missing_warp_destination_fails(self):
        result, report = self.run_audit(warps=[{"dest_map": "MAP_MISSING", "dest_warp_id": "0"}])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("references unregistered map MAP_MISSING", report["errors"][0])

    def test_invalid_destination_indexes_fail_with_report(self):
        for index in ("-1", "1", "oops", None, True, 0.5):
            with self.subTest(index=index):
                result, report = self.run_audit(warps=[{"dest_map": "MAP_CAMP", "dest_warp_id": index}])
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(len(report["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
