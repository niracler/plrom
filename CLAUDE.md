# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal inventory repository (plrom - People, Communities, Things) that maintains a curated list of favorite content creators, companies, tools, and products. The content is written in Chinese and automatically published to XLog (a decentralized blogging platform on Crossbell) when changes are pushed to the main branch.

## Publishing System

### Core Publishing Script

The [publish.sh](publish.sh) script is the heart of the publishing system. It:

1. **Parses metadata** from the frontmatter in [README.md](README.md) (between `<!--` and `-->` markers)
2. **Extracts fields**: `title`, `summary`, `cover`, `slug`, `tags`, `note_id`
3. **Publishes to XLog** via the Crossbell API:
   - If `note_id` exists: **Updates** the existing note (POST to `/notes/{note_id}/metadata`)
   - If `note_id` is empty: **Creates** a new note (PUT to `/notes`)

### Metadata Format

The README.md must have frontmatter structured like:

```markdown
<!--
title: 人 X 社区 X 物 - $(date +%Y-%m-%d)
tags: [ "life", "software", "hardware", "community", "people", "tools", "xlog" ]
cover: https://ipfs.crossbell.io/ipfs/QmR5AtZLDJqXUgn9gcYLKbcnRtGA6QtA14Xrzh6PuTsM9c
slug: plrom
summary: 关于我关注的人和物。这个主题很个人化...
note_id: 273
date: 2024-09-26
modified: 2024-09-30
-->
```

**Important**: All fields except `note_id` are required for publishing to succeed.

### Character ID

The Crossbell character ID (`57410`) is hardcoded in [publish.sh:3](publish.sh#L3). This identifies the blog owner on the Crossbell network.

## Common Commands

### Manual Publishing

```bash
# Requires XLOG_TOKEN environment variable
export XLOG_TOKEN="your-token-here"
./publish.sh
```

### Link Checking

The repository uses linkspector to validate URLs in README.md:

```bash
# Check all links (runs automatically via GitHub Actions)
npx linkspector .
```

Configuration is in [.linkspector.yml](.linkspector.yml) which ignores certain domains that frequently timeout or block bots.

## GitHub Actions Workflow

### Auto-Publish Workflow

[.github/workflows/auto-publish.yml](.github/workflows/auto-publish.yml):

- **Trigger**: Pushes to `main` branch
- **Process**: Installs `jq`, runs [publish.sh](publish.sh)
- **Secret Required**: `XLOG_TOKEN` must be set in repository secrets

### Link Checker Workflow

[.github/workflows/check-links.yml](.github/workflows/check-links.yml):

- Validates all links in README.md on pushes and PRs

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

```
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

```
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

- The repository contains **no traditional code** - it's purely content and publishing automation
- Shell script uses **POSIX-compatible syntax** (dash) for maximum portability
- JSON processing relies on `jq` being available
- The publishing script uses curl to interact with Crossbell API
- Authentication is via Bearer token in the Authorization header
