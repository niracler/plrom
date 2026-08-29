from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit", ROOT / ".github/scripts/audit.py"
)
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


class AuditSnapshotTest(unittest.TestCase):
    def write_snapshot(self, generated_at: str) -> Path:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        path = Path(tempdir.name) / "snapshot.json"
        path.write_text(
            json.dumps(
                {
                    "generated_at": generated_at,
                    "attention": {"budgeted_minutes_per_week": 180},
                    "lanes": {
                        "core": {"source_count": 15, "max_source_share_percent": 18},
                        "changelog": {"source_count": 25},
                    },
                    "totals": {"uncategorized_sources": 0, "abnormal_sources": 4},
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_fresh_snapshot_is_loaded(self) -> None:
        path = self.write_snapshot("2026-08-01T00:00:00Z")
        snapshot = audit.load_folo_snapshot(
            path, now=datetime(2026, 8, 15, tzinfo=UTC)
        )
        self.assertIsNotNone(snapshot)

    def test_stale_snapshot_is_na_not_zero(self) -> None:
        path = self.write_snapshot("2026-06-01T00:00:00Z")
        snapshot = audit.load_folo_snapshot(
            path, now=datetime(2026, 8, 15, tzinfo=UTC)
        )
        self.assertIsNone(snapshot)
        item = {"metric": "folo_uncategorized_count", "name": "test"}
        self.assertIsNone(audit.compute_metric(item, [], snapshot))
        self.assertEqual(audit.status_cell(None, 0), "⚪ N/A")

    def test_inline_render_uses_units(self) -> None:
        snapshot = json.loads(self.write_snapshot("2026-08-01T00:00:00Z").read_text())
        limits = [
            {
                "name": "Feed 注意力",
                "metric": "folo_attention_minutes",
                "limit": 180,
                "unit": "minutes",
            }
        ]
        rendered = audit.render_inline([], limits, snapshot)
        self.assertIn("180 分钟", rendered)
        self.assertNotIn("N/A", rendered)


if __name__ == "__main__":
    unittest.main()
