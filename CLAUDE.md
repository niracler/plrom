# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal inventory repository (plrom - People, Communities, Things) that maintains a curated list of favorite content creators, companies, tools, and products. The content is written in Chinese and synced to the personal blog (bokushi) via GitHub Actions when a release is published.

## Common Commands

### Link Checking

The repository uses linkspector to validate URLs in README.md:

```bash
# Check all links (runs automatically via GitHub Actions)
npx linkspector .
```

Configuration is in [.linkspector.yml](.linkspector.yml) which ignores certain domains that frequently timeout or block bots.

### 体量盘点 (FOMO Limits Dashboard)

[.github/scripts/audit.py](.github/scripts/audit.py) renders a single MECE-ish limits table inside `## 维护说明` between `<!-- AUDIT:START -->` / `<!-- AUDIT:END -->` sentinels. Each row shows a domain (e.g. 月订阅¥, 关注的人, AI 工具数), its current value, the user-set upper limit, and a status (留白 / 持平 / 超额).

**Limits 配置在 [audit/limits.toml](audit/limits.toml)**——这是单一权威源，编辑这里加/减/调上限。支持的 metric 见配置文件头部注释。

```bash
# Print full audit report (per-H3 detail) to stdout for deep dive
python3 .github/scripts/audit.py

# Refresh the inline AUDIT block in README based on limits.toml
python3 .github/scripts/audit.py --update README.md
```

The pre-commit hook (`.pre-commit-config.yaml`) auto-runs `--update` whenever README.md, audit.py, or limits.toml is staged. First-time setup on a fresh clone:

```bash
pre-commit install
```

If the hook modifies README.md, the commit fails — re-stage and re-commit.

## GitHub Actions Workflow

### Link Checker Workflow

[.github/workflows/check-links.yml](.github/workflows/check-links.yml):

- Validates all links in README.md on pushes and PRs

### Bokushi Sync Workflow

[.github/workflows/sync-to-bokushi.yml](.github/workflows/sync-to-bokushi.yml):

- **Trigger**: Release `published` events on this repository, or manual `workflow_dispatch`
- **Process**: Renders README metadata with [.github/scripts/sync_to_bokushi.py](.github/scripts/sync_to_bokushi.py), updates `niracler/bokushi`'s `src/content/blog/plrom.md`, and opens a PR via `peter-evans/create-pull-request`
- **Secret Required**: `BOKUSHI_SYNC_TOKEN` (Classic PAT with `repo` scope) so the workflow can push branches to `niracler/bokushi`

## Content Structure

The [README.md](README.md) is organized into three main sections:

1. **人 (People)**: Content creators categorized by type
   - 技术博主 (Tech bloggers)
   - 作家 (Writers)
   - 漫画家 (Manga artists)
   - 导演 (Directors)
   - UP 主 & 油管主 (Video creators)
   - 播客 (Podcasters)
   - 歌手 & 音乐制作人 (Musicians)

2. **组织或社区 (Organizations/Communities)**
   - 组织 (Organizations)
   - 游戏 & 动画公司 (Game & animation companies)
   - 技术新闻 (Tech news)

3. **物 (Things)**: Hardware, software, and tools
   - 电脑及配件 (Computers & accessories)
   - 软件工具 (Software tools)
   - Various personal devices

## Editing Guidelines

When making changes to README.md:

1. **Preserve metadata structure**: Always keep the frontmatter format intact
2. **Update modified date**: Change the `modified:` field to current date when making content changes
3. **Maintain consistency**: Follow the existing format with emojis, links, and commentary style
4. **Use details tags**: Deprecated or sensitive content goes in `<details>` sections
5. **Test links**: Run link checking before committing to avoid broken URLs

## Development Workflow

### Update Cycle

This repository follows a **monthly update cycle**:

- **Frequency**: Once per month
- **Versioning**: `YYYY.MM` format (e.g., 2025.10, 2025.11)
- **Process**: Each monthly update gets a PR, version tag, and changelog entry

### Branch Naming

```text
feature/update-YYYY-MM    # Monthly updates
feature/add-game-companies # Feature additions
fix/broken-links          # Bug fixes
docs/update-guide         # Documentation updates
```

### Monthly Update Process

1. **Create branch**: `git checkout -b feature/update-2025-10`

2. **Update content** in [README.md](README.md):
   - Add new people/communities/things
   - Remove items no longer followed
   - Update `modified` date in frontmatter

3. **Update [CHANGELOG.md](CHANGELOG.md)**:

   ```markdown
   ## [2025.10] - 2025-10-21

   ### Added
   - **[Name](link)** (category) - Reason for adding

   ### Removed
   - **Name** (category) - Reason for removal
   ```

4. **Check links**: `npx linkspector .`

5. **Create PR**:

   ```bash
   git add README.md CHANGELOG.md
   git commit -m "feat: 2025年10月月度更新"
   git push origin feature/update-2025-10
   gh pr create --title "月度更新: 2025年10月"
   ```

6. **After merge, create release**:

   ```bash
   git checkout main && git pull
   git tag -a v2025.10 -m "2025.10"
   git push origin v2025.10
   ```

### Commit Message Format

```text
feat: add new items or monthly update
fix: fix broken links or errors
docs: documentation updates
chore: releases, maintenance
```

### Versioning

- **Monthly releases**: `YYYY.MM` (e.g., v2025.10)
- **Hotfixes**: `YYYY.MM.PATCH` (e.g., v2025.10.1)

### Changelog Maintenance

[CHANGELOG.md](CHANGELOG.md) follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format with sections:

- **Added**: New people/communities/things with reasons
- **Removed**: Removed items with reasons
- **Changed**: Description or category updates
- **Fixed**: Link fixes, error corrections

Each entry should explain **why** the change was made, not just what changed.

## Technical Notes

- The repository contains **no traditional code** - it's purely content and automation
- Blog sync uses [sync_to_bokushi.py](.github/scripts/sync_to_bokushi.py) to render metadata and open a PR to `niracler/bokushi`
