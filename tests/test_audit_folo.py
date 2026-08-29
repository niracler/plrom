from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path
from subprocess import TimeoutExpired
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/folo"
SPEC = importlib.util.spec_from_file_location(
    "audit_folo", ROOT / ".github/scripts/audit_folo.py"
)
assert SPEC and SPEC.loader
audit_folo = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit_folo
SPEC.loader.exec_module(audit_folo)


def fixture(name: str):
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


class AuditFoloTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = {
            "subscriptions": fixture("subscriptions"),
            "lists": fixture("lists"),
            "unread": fixture("unread"),
            "collections": fixture("collections"),
            "analytics": fixture("analytics"),
            "analytics_failures": 0,
        }

    def test_snapshot_aggregates_and_normalizes_stars(self) -> None:
        snapshot = audit_folo.build_snapshot(
            self.data, now=datetime(2026, 6, 15, tzinfo=UTC)
        )

        self.assertEqual(snapshot["totals"]["direct_subscriptions"], 7)
        self.assertEqual(snapshot["totals"]["private_sources"], 1)
        self.assertEqual(snapshot["totals"]["uncategorized_sources"], 0)
        self.assertEqual(snapshot["totals"]["abnormal_sources"], 1)
        self.assertEqual(snapshot["totals"]["timeline_visible_sources"], 2)
        self.assertEqual(snapshot["totals"]["timeline_hidden_sources"], 5)
        self.assertEqual(snapshot["attention"]["budgeted_minutes_per_week"], 180)
        self.assertEqual(snapshot["star_signals"]["sample_size"], 3)
        self.assertEqual(snapshot["star_signals"]["sample_window_days"], 15)
        self.assertEqual(snapshot["lanes"]["core"]["source_count"], 2)
        self.assertEqual(snapshot["lanes"]["core"]["unread_entries"], 3)
        self.assertEqual(
            snapshot["lanes"]["core"]["max_source_share_percent"], 83.3
        )

    def test_snapshot_contains_no_source_metadata(self) -> None:
        snapshot = audit_folo.build_snapshot(
            self.data, now=datetime(2026, 6, 15, tzinfo=UTC)
        )
        rendered = json.dumps(snapshot, ensure_ascii=False).lower()

        for forbidden in ("feed-a", "list-core", "entry-1", "http://", "https://"):
            self.assertNotIn(forbidden, rendered)
        audit_folo.validate_snapshot_privacy(snapshot)

    def test_privacy_validator_rejects_url_and_identifier_fields(self) -> None:
        with self.assertRaises(ValueError):
            audit_folo.validate_snapshot_privacy({"source": {"url": "redacted"}})
        with self.assertRaises(ValueError):
            audit_folo.validate_snapshot_privacy({"source": "https://invalid.example"})

    @patch.object(audit_folo.subprocess, "run")
    def test_cli_timeout_is_sanitized(self, run) -> None:
        run.side_effect = TimeoutExpired(cmd="redacted", timeout=120)
        with self.assertRaisesRegex(audit_folo.AuditError, "timed out"):
            audit_folo.run_cli("subscription", "list")


if __name__ == "__main__":
    unittest.main()
