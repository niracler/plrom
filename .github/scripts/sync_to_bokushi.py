#!/usr/bin/env python3
"""Generate Bokushi blog post content from README metadata."""

from __future__ import annotations

import ast
import datetime as dt
import json
import os
import re
import sys
from typing import Any, Dict, Tuple


FRONTMATTER_PATTERN = re.compile(r"<!--(.*?)-->", re.DOTALL)
DATE_PLACEHOLDER = re.compile(r"\$\((?:date \+%Y-%m-%d)\)")


def parse_frontmatter(readme_text: str) -> Tuple[Dict[str, Any], str]:
    match = FRONTMATTER_PATTERN.search(readme_text)
    if not match:
        raise ValueError("README.md missing expected HTML comment frontmatter block.")

    frontmatter_raw = match.group(1)
    metadata: Dict[str, Any] = {}
    for line in frontmatter_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not value:
            metadata[key] = ""
            continue

        if value.startswith("["):
            # Parse list-based values like tags.
            metadata[key] = ast.literal_eval(value)
        else:
            metadata[key] = value

    body = readme_text[match.end() :].lstrip()
    return metadata, body


def format_date(date_str: str) -> Tuple[str, str]:
    if not date_str:
        today = dt.date.today()
        return today.isoformat(), today.strftime("%b %d, %Y")
    try:
        parsed = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # Leave unparsed value as-is for ISO and display.
        return date_str, date_str
    return parsed.isoformat(), parsed.strftime("%b %d, %Y")


def resolve_title(raw_title: str, metadata: Dict[str, Any]) -> str:
    if raw_title and DATE_PLACEHOLDER.search(raw_title):
        replacement = (
            metadata.get("modified")
            or metadata.get("date")
            or dt.date.today().isoformat()
        )
        raw_title = DATE_PLACEHOLDER.sub(replacement, raw_title)
    return raw_title


def build_frontmatter(metadata: Dict[str, Any]) -> Dict[str, Any]:
    title = resolve_title(metadata.get("title", ""), metadata)
    tags = metadata.get("tags", [])
    if not isinstance(tags, list):
        tags = [str(tags)]

    cover = metadata.get("cover", "")

    pub_iso, pub_display = format_date(metadata.get("date", ""))
    mod_iso, mod_display = format_date(metadata.get("modified", "") or pub_iso)

    return {
        "title": title,
        "tags": tags,
        "socialImage": cover,
        "pubDate": pub_display,
        "updatedDate": mod_display,
    }


def render_frontmatter(frontmatter: Dict[str, Any]) -> str:
    lines = ["---"]
    lines.append(f"title: {frontmatter['title']}")
    lines.append(f"tags: {json.dumps(frontmatter['tags'], ensure_ascii=False)}")
    if frontmatter["socialImage"]:
        lines.append(f"socialImage: {frontmatter['socialImage']}")
    lines.append(f'pubDate: "{frontmatter["pubDate"]}"')
    lines.append(f'updatedDate: "{frontmatter["updatedDate"]}"')
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def write_output(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: sync_to_bokushi.py <README.md> <output.md>")

    readme_path, output_path = sys.argv[1:]
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_text = f.read()

    metadata, body = parse_frontmatter(readme_text)
    frontmatter = build_frontmatter(metadata)

    rendered_frontmatter = render_frontmatter(frontmatter)
    content = f"{rendered_frontmatter}{body}"

    write_output(output_path, content)


if __name__ == "__main__":
    main()
