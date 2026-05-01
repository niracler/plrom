# Changelog

所有值得注意的变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
版本号采用 `YYYY.MM[.PATCH]` 格式。

## [Unreleased]

## [2026.04] - 2026-04-29

### Added

- **[Simon Willison](https://simonwillison.net/)** (博主) - Django 共同作者，每天更 LLM 工具实测和踩坑笔记，海外 AI 工程视角的主要订阅源
- **[烤肉肉](https://www.lowbee.icu/)** (博主) - xLog 时期的笔友，周更生活向周记多年；从他这里悟出「平凡地记录下自己的生活，就已经足够吸引人」
- **[触乐](https://www.chuapp.com/)** (组织 / 游戏媒体) - 国内游戏媒体里少有还认真做长文专题的，跟 taste.md 里「带思考的游戏评论」对得上
- **[Anthropic News](https://www.anthropic.com/news)** (组织) - Claude Code 已经是日常工具，官方 News 应该单独列出来

### Changed

- **📚 技术博主** 标题改为 **📚 ~~技术~~博主**，呼应下面那句「其它深入一点的技术博主，我都是看不懂的」自嘲
- **订阅价格全面对账**（按 Apple/Stripe 真实账单）：
  - **Claude Code** — 标记 `公司付费, Max 5x $124.99/m`，不再计入个人订阅
  - **iCloud** — `¥24/m 淘宝车` → `¥68/m, 2TB` 官方
  - **1Password** — `¥248/y` → `¥498/y, Families` 升级
  - **Surge 5** — `$49.99` 一次性 → `$14.99/y` Feature Subscription
  - **熊猫吃短信 2** — `¥12/y` → `¥1/m`（Apple 显示按月 ¥1）
  - **Rond** — `¥98` 一次性 → `¥48/m, PLUS` 订阅
- **新增 7 个一直在订但 README 没标价的订阅**：Chatgpt App ($8/m)、Telegram ($36/y)、Apple Music (¥17/m, Family)、Evermusic ($9.99/y)、哔哩哔哩 App (¥15/m 充电)
- **从过期列表移回活跃**：Apple Music、哔哩哔哩漫画（畅读卡 ¥248/y）—— 这俩之前写「不订了」，结果又订回来了

## [2026.03] - 2026-03-26

### Added

- **[Nintendo Switch 2](https://www.nintendo.com/us/gaming-systems/nintendo-switch-2/)** (游戏娱乐设备) - 过年前入手，主力在玩 Pokopia
- **[Apifox](https://apifox.com/)** (软件 / 开发工具) - 工作中用于 API 调试
- **[Keka](https://apps.apple.com/us/app/keka/id470158793?mt=12)** (软件 / 生产力工具) - macOS 解压缩工具

### Changed

- **MacBook Air (M5)** - 补充国补价格 ¥9999 及以旧换新 3000 块的信息
- **iStat Menus** - 从过期列表恢复为活跃，退订 Setapp 后单独买断 ¥60
- **Nintendo Switch 续航版** - 移至不活跃列表（买了 Switch 2 后准备送人）

## [2026.02] - 2026-02-24

### Added

- **[宝玉](https://baoyu.io/)** (技术博主) - 国内 AI 资讯翻译，面向普通程序员的精华搬运
- **[skills CLI](https://github.com/vercel-labs/skills)** (大模型工具 / Agent Skills) - Vercel 出品的 Skills 管理命令行工具
- **[antfu/skills](https://github.com/antfu/skills)** (大模型工具 / Agent Skills) - Anthony Fu 的 Vue 生态技能集合（17 个技能）
- **[vercel-react-best-practices](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices)** (大模型工具 / Agent Skills) - Vercel 官方 React/Next.js 性能优化指南
- **[BuhoCleaner](https://www.drbuho.com/buhocleaner)** (软件 / 系统工具) - Mac 系统清理工具终身版，替代 CleanMyMac X

### Changed

- 重新组织 AI 工具 section，采用扁平列表结构替代分类嵌套
- iTerm2 恢复为主力终端

### Removed

- **ollama** → 过期列表（有了 Claude Code 之后本地模型基本不玩了）
- **Ghostty** → 过期列表（稳定性还有不少问题，暂时退役）
- **OpenCat Pro** → 补加删除线标记（订阅 Claude Pro 后完全不用）
- **Setapp 相关整理** - iStat Menus、Session、MindNode、CleanMyMac X、TouchRetouch 等移入过期列表，不再续订 Setapp

## [2026.01] - 2026-01-12

### Added

- **Claude Code 插件配置** (软件 / 大模型工具) - 新增完整的 Claude Code 插件配置列表：
  - 开发辅助类：code-review、code-simplifier、feature-dev、frontend-design、typescript-lsp、pyright-lsp、security-guidance
  - 文档与知识类：context7、[obsidian](https://github.com/nicholasrq/obsidian-skills)
  - 工作流增强：[superpowers](https://github.com/anthropics/claude-code-superpowers)、workflow-skills
  - 写作与学习类：writing-skills、learning-skills、learning-output-style
  - 趣味类：fun-skills

## [2025.12] - 2025-12-25

### Added

- **🤖 大模型工具** (软件 / 新分类) - 新增 AI 辅助开发工具分类：
  - [OpenSpec](https://github.com/Fission-AI/OpenSpec) - 规范驱动开发框架
  - [ccusage](https://github.com/ryoppippi/ccusage) - Claude Code 用量分析工具
  - [Context7](https://context7.com/) - LLM 文档 MCP 服务
  - [Playwright MCP](https://github.com/microsoft/playwright-mcp) - 浏览器自动化 MCP
  - [我的 Skill 仓库](https://github.com/niracler/skill) - 个人 Claude Code Skills
- **📊 演示工具** (软件 / 新分类) - 新增 [Slidev](https://sli.dev/) Markdown 演示框架
- **☁️ 云服务器** (软件 / 新分类) - 新增 [CloudCone](https://cloudcone.com/) VPS 提供商
- **[取伙](https://quhuo.com.cn/Home)** (组织) - Z 世代年轻人的活动聚集平台
- **[LG 27UQ850V 4K 显示器](https://item.jd.com/100081317949.html)** (物 / 电脑及配件) - 新增 4K 显示器
- **[Evermusic](https://everappz.com/products/evermusic/)** (软件 / 视频 & 音乐) - iOS 本地/云音乐播放器
- **[netease-cloud-music-dl](https://github.com/codezjx/netease-cloud-music-dl)** (软件 / 视频 & 音乐) - 网易云音乐下载工具

### Changed

- 更新 Claude Code 价格信息（$100/m）
- 更新 Folo 价格信息（$100/年）
- 修复网易云音乐描述中的乱码字符

### Removed

- 将 hurl 移至过期列表
- 将 Zoom 移至过期列表

## [2025.11] - 2025-11-05

### Added

- **[Pioneer BDR-XD07B](https://www.amazon.com/Pioneer-BDR-XD07B-Slim-Portable-Burner/dp/B07ZJX5HSH)** (物 / 电脑及配件) - 新增便携式蓝光刻录机，满足旅游购入光盘的读取需求。
- **[Magic Trackpad](https://support.apple.com/en-hk/111884)** (物 / 电脑及配件) - 补齐外接显示器场景下的触控操作体验。
- **[HomePod mini](https://www.apple.com/homepod-mini/)** (物 / 耳机及音箱) - 引入家庭音频设备，延续物联网设备尝试计划。
- **[OpenAI Codex CLI](https://openai.com/codex/)** (软件 / 命令行工具) - 新增终端 AI 助手，探索自然语言驱动的命令工作流。
- **[Zed](https://zed.dev/)** (软件 / 文本编辑 & IDE) - 试用高性能编辑器，评估替换 VS Code 的可行性。
- **[Ghostty](https://ghostty.org/)** (软件 / 开发工具) - 作为新的主力终端，追求更轻量的使用体验。
- **[Tachimanga](https://tachimanga.app/)** (软件 / 动画 & 漫画) - 切换到 iOS 端的漫画阅读主力工具。

### Changed

- 更新 README 前言：标签聚焦“社区 / 工具”、替换封面图片、`modified` 更新为 2025-11-05。
- 调整多项设备与服务状态：Redmi Pad、Boox Leaf 等转入“不活跃列表”；YouTube 改为非 Premium 使用；网易云音乐重新启用；Follow 更名为 Folo 并更新主页链接。
- 扩写多处软件说明：补充 Zed 的使用体验、Chrome 的保留理由、Obsidian 主题补充等内容，同时统一 Markdown 行尾格式。

### Removed

- 将 Warp、Applite、XLocker、TachiyomiSY 等从主列表移动至“过期列表”，并保留弃用原因说明。
- 清理 README 中过期描述和冗余换行，使内容结构更紧凑。

### Technical

- 添加 `.github/scripts/sync_to_bokushi.py` 与 `.github/workflows/sync-to-bokushi.yml`，现调整为仅在发布 release 时生成内容并同步到 `niracler/bokushi`。
- 引入 `.markdownlint.json`，关闭 MD013 与 MD033 规则，便于维护长行和内嵌 HTML。
- 新增 `AGENTS.md` 指向 `CLAUDE.md` 的符号链接，并在 `CLAUDE.md` 记录 Bokushi 同步工作流说明。

## [2025.10] - 2025-10-21

### Added

#### 人 (People)

- **[DIYgod](https://diygod.me/)** (技术博主) - RSSHub 作者，充满温度的开源项目创作者
- **[23.4ド(イチリ)](https://x.com/234itiri)** (漫画家) - 《堕天计画》系列作者

#### 组织/社区 (Organizations/Communities)

- **[AliceSoft](https://www.alicesoft.com/)** (游戏公司) - 成立于 1989 年的日本成人游戏公司，《兰斯》系列制作方
- **[Qruppo](https://qruppo.com/)** (游戏公司) - 新锐游戏公司，《抜きゲーみたいな島》系列开发商
- **[Intelligent Systems](https://www.intsys.co.jp/)** (游戏公司) - 任天堂第二方，《火焰纹章》系列制作方
- **[香草社 (Vanillaware)](https://mzh.moegirl.org.cn/Vanillaware)** (游戏公司) - 以精美 2D 美术著称，《圣兽之王》《十三机兵防卫圈》制作方

#### 物 (Things)

- **[MacBook Air M1](https://support.apple.com/kb/SP825?locale=zh_CN)** - 16G RAM 512G SSD 主力工作电脑
- **[Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)** (8G RAM) - 运行 Home Assistant OS
- **[Logitech MX Keys](https://www.logitech.com/zh-cn/products/keyboards/mx-keys-mac-wireless-keyboard.920-009559.html)** - 办公用机械键盘
- **[iPad Pro M1 11 寸](https://www.apple.com/cn/ipad-pro/)** (256G) - 用于看漫画和副屏
- **[Nintendo Switch 续航版](https://www.nintendo.com/switch/)** - 日版，主力游戏机
- **[Claude Code](https://claude.ai/code)** - AI 编程助手
- **[onefetch](https://github.com/o2sh/onefetch)** - Git 仓库信息展示工具
- **Setapp 相关应用** - CleanMyMac X, CleanShot X, Bartender 等多个实用工具

### Changed

- 更新 DIYgod 条目，标注 XLog 基本不可用状态
- 更新各设备使用状态（MacBook Air 移到宿舍、MX Master 3 连接 Windows 主机等）

### Removed

- **Arc 浏览器** - 移除，改用其他浏览器方案

### Technical

- 添加 CHANGELOG.md 维护变更历史
- 添加月度更新工作流程到 CLAUDE.md
- 添加 GitHub Actions 自动发布到 XLog
- 添加 GitHub Actions 链接检查
- 规范化版本发布流程（PR + Tag + Release）

[Unreleased]: https://github.com/niracler/plrom/compare/v2026.02...HEAD
[2026.02]: https://github.com/niracler/plrom/compare/v2026.01...v2026.02
[2026.01]: https://github.com/niracler/plrom/compare/v2025.12...v2026.01
[2025.12]: https://github.com/niracler/plrom/compare/v2025.11...v2025.12
[2025.11]: https://github.com/niracler/plrom/compare/v2025.10...v2025.11
[2025.10]: https://github.com/niracler/plrom/releases/tag/v2025.10
