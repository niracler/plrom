#!/usr/bin/env python3
"""Generate a privacy-safe aggregate snapshot of the signed-in Folo account.

The live command uses the repo-local Folo CLI session. The resulting JSON is
safe to commit: it contains only aggregate counts and rates, never account
metadata, source/list identifiers, source titles, URLs, or credentials.

Usage:
    python3 .github/scripts/audit_folo.py --output audit/folo-snapshot.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

CLI = ("npx", "--yes", "folocli@latest")
CORE_LIST = "⚡ 每日核心"
DESSERT_LIST = "🧁 周六甜点"
CHANGELOG_LIST = "🛠 Changelog"
ENTERTAINMENT_CATEGORY = "🎮 ACG 与娱乐"

ATTENTION_BUDGET = {
    "core": 60,
    "dessert": 75,
    "changelog": 15,
    "entertainment": 30,
}


class AuditError(RuntimeError):
    """A sanitized live-data collection failure."""


def run_cli(*args: str) -> Any:
    """Run Folo CLI without exposing its stored session or raw error output."""
    command = [*CLI, *args]
    label = " ".join(args[:2])
    try:
        proc = subprocess.run(command, text=True, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired as exc:
        raise AuditError(f"Folo CLI command timed out: {label}") from exc
    if proc.returncode:
        raise AuditError(f"Folo CLI command failed: {label}")
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AuditError(f"Folo CLI returned invalid JSON: {label}") from exc
    if not result.get("ok"):
        raise AuditError(f"Folo API request failed: {label}")
    return result.get("data")


def fetch_live_data(workers: int = 8) -> dict[str, Any]:
    """Collect the minimum live payload needed to build aggregate metrics."""
    subscriptions = run_cli("subscription", "list")["subscriptions"]
    owned_lists = run_cli("list", "ls")
    unread = run_cli("unread", "list")
    collections = run_cli("collection", "list", "--limit", "100")

    direct_ids = {
        row["feedId"] for row in subscriptions if isinstance(row.get("feeds"), dict)
    }
    list_ids = {
        feed_id
        for row in owned_lists
        for feed_id in (row.get("feedIds") or [])
    }
    analytics_ids = sorted(direct_ids | list_ids)

    analytics: dict[str, float] = {}
    failures = 0

    def fetch_one(feed_id: str) -> tuple[str, float]:
        data = run_cli("feed", "analytics", feed_id)
        record = (data.get("analytics") or {}).get(feed_id) or {}
        return feed_id, max(float(record.get("updatesPerWeek") or 0), 0)

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(fetch_one, feed_id): feed_id for feed_id in analytics_ids}
        for future in as_completed(futures):
            try:
                feed_id, updates = future.result()
                analytics[feed_id] = updates
            except AuditError:
                failures += 1
                analytics[futures[future]] = 0

    return {
        "subscriptions": subscriptions,
        "lists": owned_lists,
        "unread": unread,
        "collections": collections,
        "analytics": analytics,
        "analytics_failures": failures,
    }


def _as_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _deduplicated_stars(entries: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for row in entries:
        entry_id = str((row.get("entries") or {}).get("id") or "")
        if not entry_id or entry_id in seen:
            continue
        seen.add(entry_id)
        result.append(row)
    return result


def _lane_snapshot(
    feed_ids: set[str],
    analytics: dict[str, float],
    unread_by_feed: dict[str, int],
    stars_by_feed: Counter[str],
    star_window_days: int,
) -> dict[str, int | float]:
    updates = {feed_id: analytics.get(feed_id, 0) for feed_id in feed_ids}
    updates_per_week = sum(updates.values())
    max_share = (
        max(updates.values(), default=0) / updates_per_week * 100
        if updates_per_week > 0
        else 0
    )
    starred = sum(stars_by_feed.get(feed_id, 0) for feed_id in feed_ids)
    expected_entries = updates_per_week * max(star_window_days, 1) / 7
    hit_rate = starred / max(expected_entries, starred, 1) * 100
    return {
        "source_count": len(feed_ids),
        "estimated_entries_per_week": round(updates_per_week, 1),
        "unread_entries": sum(unread_by_feed.get(feed_id, 0) for feed_id in feed_ids),
        "starred_entries_in_sample": starred,
        "estimated_star_hit_rate_percent": round(hit_rate, 1),
        "max_source_share_percent": round(max_share, 1),
    }


def build_snapshot(data: dict[str, Any], *, now: datetime | None = None) -> dict[str, Any]:
    """Normalize raw CLI payloads into a privacy-safe aggregate snapshot."""
    now = (now or datetime.now(UTC)).astimezone(UTC)
    subscriptions = data.get("subscriptions") or []
    direct = [row for row in subscriptions if isinstance(row.get("feeds"), dict)]
    owned_lists = data.get("lists") or []
    analytics = {str(k): float(v or 0) for k, v in (data.get("analytics") or {}).items()}

    list_feed_ids = {
        str(row.get("title")): {str(feed_id) for feed_id in (row.get("feedIds") or [])}
        for row in owned_lists
    }
    core_ids = list_feed_ids.get(CORE_LIST, set())
    dessert_ids = list_feed_ids.get(DESSERT_LIST, set())
    changelog_ids = list_feed_ids.get(CHANGELOG_LIST, set())
    entertainment_ids = {
        str(row.get("feedId"))
        for row in direct
        if row.get("category") == ENTERTAINMENT_CATEGORY and not row.get("isPrivate")
    }

    unread_data = data.get("unread") or {}
    unread_by_feed = {
        str(row.get("feedId")): int(row.get("unreadCount") or 0)
        for row in (unread_data.get("items") or [])
        if row.get("feedId")
    }

    raw_stars = (data.get("collections") or {}).get("entries") or []
    stars = _deduplicated_stars(raw_stars)
    stars_by_feed: Counter[str] = Counter()
    star_dates: list[datetime] = []
    for row in stars:
        feed_id = str((row.get("feeds") or {}).get("id") or "")
        if feed_id:
            stars_by_feed[feed_id] += 1
        created = _as_datetime((row.get("collections") or {}).get("createdAt"))
        if created:
            star_dates.append(created)
    star_window_days = (
        max(1, (max(star_dates) - min(star_dates)).days + 1) if star_dates else 1
    )

    direct_ids = {str(row.get("feedId")) for row in direct}
    total_updates = sum(analytics.get(feed_id, 0) for feed_id in direct_ids)
    high_volume_zero_star = sum(
        1
        for feed_id in direct_ids
        if analytics.get(feed_id, 0) > 25 and stars_by_feed.get(feed_id, 0) == 0
    )
    low_frequency_starred = sum(
        1
        for feed_id in direct_ids
        if analytics.get(feed_id, 0) <= 2 and stars_by_feed.get(feed_id, 0) > 0
    )

    lanes = {
        "core": _lane_snapshot(
            core_ids, analytics, unread_by_feed, stars_by_feed, star_window_days
        ),
        "dessert": _lane_snapshot(
            dessert_ids, analytics, unread_by_feed, stars_by_feed, star_window_days
        ),
        "changelog": _lane_snapshot(
            changelog_ids, analytics, unread_by_feed, stars_by_feed, star_window_days
        ),
        "entertainment": _lane_snapshot(
            entertainment_ids, analytics, unread_by_feed, stars_by_feed, star_window_days
        ),
    }

    snapshot = {
        "schema_version": 1,
        "generated_at": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "window_days": 7,
        "status": "ok" if not data.get("analytics_failures") else "partial",
        "totals": {
            "direct_subscriptions": len(direct),
            "owned_lists": len(owned_lists),
            "timeline_visible_sources": sum(
                not bool(row.get("hideFromTimeline")) for row in direct
            ),
            "timeline_hidden_sources": sum(
                bool(row.get("hideFromTimeline")) for row in direct
            ),
            "private_sources": sum(bool(row.get("isPrivate")) for row in direct),
            "uncategorized_sources": sum(not row.get("category") for row in direct),
            "abnormal_sources": sum(
                bool((row.get("feeds") or {}).get("errorMessage")) for row in direct
            ),
            "unread_entries": int(unread_data.get("total") or 0),
            "estimated_entries_per_week": round(total_updates, 1),
            "analytics_failures": int(data.get("analytics_failures") or 0),
        },
        "attention": {
            "budgeted_minutes_per_week": sum(ATTENTION_BUDGET.values()),
            "core_minutes": ATTENTION_BUDGET["core"],
            "dessert_minutes": ATTENTION_BUDGET["dessert"],
            "changelog_minutes": ATTENTION_BUDGET["changelog"],
            "entertainment_minutes": ATTENTION_BUDGET["entertainment"],
        },
        "lanes": lanes,
        "star_signals": {
            "sample_size": len(stars),
            "sample_window_days": star_window_days,
            "starred_source_count": len(stars_by_feed),
            "high_volume_zero_star_sources": high_volume_zero_star,
            "low_frequency_starred_sources": low_frequency_starred,
        },
    }
    validate_snapshot_privacy(snapshot)
    return snapshot


def validate_snapshot_privacy(snapshot: dict[str, Any]) -> None:
    """Reject fields or values that could disclose Folo source metadata."""
    forbidden_keys = {"account", "feed_id", "feedid", "list_id", "listid", "title", "url"}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in forbidden_keys:
                    raise ValueError(f"privacy-unsafe snapshot key: {key}")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, str) and ("http://" in value or "https://" in value):
            raise ValueError("privacy-unsafe URL in snapshot")

    walk(snapshot)


def write_snapshot(snapshot: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("audit/folo-snapshot.json"))
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    try:
        snapshot = build_snapshot(fetch_live_data(args.workers))
        write_snapshot(snapshot, args.output)
    except (AuditError, ValueError) as exc:
        print(f"[audit-folo] {exc}", file=sys.stderr)
        return 1
    print(f"[audit-folo] wrote privacy-safe snapshot to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
