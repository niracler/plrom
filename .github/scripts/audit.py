#!/usr/bin/env python3
"""Audit plrom README content count and subscription cost.

Counts every bullet item per category, splits active vs deprecated by
<details> blocks, and totals recurring subscription cost normalized to ¥/month.

Usage:
    python3 .github/scripts/audit.py [path/to/README.md]    # print full report
    python3 .github/scripts/audit.py --update README.md     # rewrite AUDIT block in place
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

SENTINEL_START = "<!-- AUDIT:START -->"
SENTINEL_END = "<!-- AUDIT:END -->"
LIMITS_PATH = Path("audit/limits.toml")

USD_TO_CNY = 7.2  # rough April 2026 rate

# Subscription patterns: capture amount, then convert to ¥/month
PRICE_PATTERNS: list[tuple[re.Pattern[str], float]] = [
    (re.compile(r"\$(\d+(?:\.\d+)?)/m\b"), USD_TO_CNY),
    (re.compile(r"\$(\d+(?:\.\d+)?)/y\b"), USD_TO_CNY / 12),
    (re.compile(r"\$(\d+(?:\.\d+)?)/年"), USD_TO_CNY / 12),
    (re.compile(r"¥(\d+(?:\.\d+)?)/m\b"), 1.0),
    (re.compile(r"¥(\d+(?:\.\d+)?)/y\b"), 1.0 / 12),
    (re.compile(r"¥(\d+(?:\.\d+)?)/年"), 1.0 / 12),
]

LINK_LABEL = re.compile(r"\[([^\]]+)\]")
BOLD_LABEL = re.compile(r"\*\*([^*]+)\*\*")

# H2 sections that are meta/maintenance, not content
SKIP_H2 = {"维护说明"}


@dataclass
class Subscription:
    label: str
    raw: str
    yuan_per_month: float


@dataclass
class Category:
    h2: str
    h3: str
    active: int = 0
    deprecated: int = 0
    subs: list[Subscription] = field(default_factory=list)


def extract_label(line: str) -> str:
    line = line.lstrip("- ").strip()
    line = line.lstrip("~")  # drop leading ~~strikethrough markers
    if (m := LINK_LABEL.match(line)) is not None:
        return m.group(1)
    if (m := BOLD_LABEL.match(line)) is not None:
        return m.group(1)
    return (line[:40] + "…") if len(line) > 40 else line


SUBSCRIPTION_SKIP_KEYWORDS = ("公司付费",)


def parse_subscription(line: str) -> Subscription | None:
    if any(kw in line for kw in SUBSCRIPTION_SKIP_KEYWORDS):
        return None
    for pattern, factor in PRICE_PATTERNS:
        if (m := pattern.search(line)) is not None:
            amount = float(m.group(1))
            return Subscription(
                label=extract_label(line),
                raw=m.group(0),
                yuan_per_month=amount * factor,
            )
    return None


def audit(readme: Path) -> list[Category]:
    cats: dict[tuple[str, str], Category] = {}
    h2 = h3 = ""
    in_details = 0  # depth, in case of nested <details>

    for raw in readme.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.lstrip()

        if "<details>" in line:
            in_details += 1
            continue
        if "</details>" in line:
            in_details = max(in_details - 1, 0)
            continue
        if line.startswith("<!--") or line.startswith("-->"):
            continue
        if stripped.startswith(">"):
            continue

        if line.startswith("## ") and not line.startswith("### "):
            h2 = line[3:].strip()
            h3 = ""
            continue
        if line.startswith("### "):
            h3 = line[4:].strip()
            if h2 not in SKIP_H2:
                cats.setdefault((h2, h3), Category(h2, h3))
            continue

        if not stripped.startswith("-"):
            continue
        if not h3 or h2 in SKIP_H2:
            continue

        cat = cats.setdefault((h2, h3), Category(h2, h3))
        if in_details:
            cat.deprecated += 1
            continue  # skip subscription parsing for deprecated items
        cat.active += 1

        if (sub := parse_subscription(stripped)) is not None:
            sub.label = f"{sub.label} ({h3})"
            cat.subs.append(sub)

    return list(cats.values())


def render_full(cats: list[Category]) -> str:
    """Full standalone report (for stdout / one-off check)."""
    total_active = sum(c.active for c in cats)
    total_deprecated = sum(c.deprecated for c in cats)
    all_subs = [s for c in cats for s in c.subs]
    monthly = sum(s.yuan_per_month for s in all_subs)

    out: list[str] = []
    out.append("# plrom 体量盘点\n")
    out.append("## 总览\n")
    out.append(f"- 活跃条目：**{total_active}** 个")
    out.append(f"- 过期/不活跃条目：**{total_deprecated}** 个")
    out.append(f"- 月订阅烧钱：**¥{monthly:.0f} / 月**（年度 ¥{monthly * 12:.0f}）")
    out.append(f"- 在订订阅条目数：**{len(all_subs)}** 个\n")

    out.append("## 按分类（活跃数降序）\n")
    out.append("| H2 | H3 | 活跃 | 不活跃 | 月订阅 ¥ |")
    out.append("|----|-----|------|--------|----------|")
    for c in sorted(cats, key=lambda x: (-x.active, -x.deprecated)):
        sub_total = sum(s.yuan_per_month for s in c.subs)
        sub_cell = f"{sub_total:.0f}" if sub_total > 0 else ""
        out.append(f"| {c.h2} | {c.h3} | {c.active} | {c.deprecated} | {sub_cell} |")

    if all_subs:
        out.append("\n## 月订阅明细（¥/月 降序）\n")
        out.append("| 条目 | 原价 | ¥/月 |")
        out.append("|------|------|------|")
        for s in sorted(all_subs, key=lambda x: -x.yuan_per_month):
            out.append(f"| {s.label} | `{s.raw}` | {s.yuan_per_month:.1f} |")

    out.append("\n## TOP 10 最胖分类\n")
    for i, c in enumerate(sorted(cats, key=lambda x: -x.active)[:10], 1):
        out.append(f"{i}. **{c.h3}** ({c.h2}) — 活跃 {c.active}，不活跃 {c.deprecated}")

    return "\n".join(out) + "\n"


METRICS: dict[str, Callable[..., float]] = {
    "subscription_total": lambda cats: sum(s.yuan_per_month for c in cats for s in c.subs),
    "subscription_count": lambda cats: sum(len(c.subs) for c in cats),
    "total_active": lambda cats: sum(c.active for c in cats),
    "total_deprecated": lambda cats: sum(c.deprecated for c in cats),
    "h2_active": lambda cats, h2: sum(c.active for c in cats if c.h2 == h2),
    "h3_active": lambda cats, h3: sum(c.active for c in cats if c.h3 == h3),
}


def load_limits(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("rb") as f:
        data = tomllib.load(f)
    return data.get("items", [])


def compute_metric(item: dict[str, Any], cats: list[Category]) -> float:
    name = item["metric"]
    fn = METRICS.get(name)
    if fn is None:
        raise ValueError(f"unknown metric: {name!r} in item {item.get('name', '?')}")
    if "arg" in item:
        return fn(cats, item["arg"])
    return fn(cats)


def format_value(value: float) -> str:
    return str(round(value))


def status_cell(current: float, limit: float | None) -> str:
    if limit is None:
        return "—"
    diff = current - limit
    if diff > 0:
        return f"🚨 超 {format_value(diff)}"
    if diff == 0:
        return "🟡 持平"
    return f"✅ 留白 {format_value(-diff)}"


def render_inline(cats: list[Category], limits: list[dict[str, Any]]) -> str:
    """Compact limits dashboard for embedding in README.md between sentinels."""
    out: list[str] = []
    out.append("### 📊 体量盘点")
    out.append("")
    out.append(
        "> 由 [.github/scripts/audit.py](.github/scripts/audit.py) "
        "依据 [audit/limits.toml](audit/limits.toml) 自动生成，pre-commit hook 刷新。"
    )
    out.append("")

    if not limits:
        out.append("_未配置 [audit/limits.toml](audit/limits.toml)，无可对照的上限_。")
        return "\n".join(out)

    out.append("| # | 维度 | 当前 | 上限 | 状态 | 备注 |")
    out.append("|---|------|------|------|------|------|")
    for i, item in enumerate(limits, 1):
        current = compute_metric(item, cats)
        limit = item.get("limit")
        limit_cell = format_value(float(limit)) if limit is not None else "—"
        status = status_cell(current, float(limit) if limit is not None else None)
        note = item.get("note", "")
        out.append(
            f"| {i} | {item['name']} | {format_value(current)} | "
            f"{limit_cell} | {status} | {note} |"
        )

    return "\n".join(out)


def update_in_place(readme: Path, limits_path: Path) -> bool:
    """Rewrite the AUDIT block between sentinels. Returns True if file changed."""
    content = readme.read_text(encoding="utf-8")
    if SENTINEL_START not in content or SENTINEL_END not in content:
        sys.stderr.write(
            f"[audit] sentinel markers not found in {readme}; "
            f"add {SENTINEL_START} ... {SENTINEL_END} block first\n"
        )
        sys.exit(2)

    cats = audit(readme)
    limits = load_limits(limits_path)
    inline = render_inline(cats, limits)
    new_block = f"{SENTINEL_START}\n\n{inline}\n\n{SENTINEL_END}"

    pattern = re.compile(
        re.escape(SENTINEL_START) + r".*?" + re.escape(SENTINEL_END),
        re.DOTALL,
    )
    new_content = pattern.sub(new_block, content)

    if new_content == content:
        return False
    readme.write_text(new_content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", nargs="?", default="README.md", type=Path)
    parser.add_argument(
        "--update",
        action="store_true",
        help="rewrite the AUDIT:START/END block in README in place",
    )
    args = parser.parse_args()

    if args.update:
        changed = update_in_place(args.readme, LIMITS_PATH)
        if changed:
            print(f"[audit] updated AUDIT block in {args.readme}")
        else:
            print(f"[audit] AUDIT block already current in {args.readme}")
    else:
        cats = audit(args.readme)
        print(render_full(cats))


if __name__ == "__main__":
    main()
