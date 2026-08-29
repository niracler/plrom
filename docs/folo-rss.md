# Folo RSS 阅读体系

本文记录 Folo 的订阅组织、阅读预算、筛选规则和维护流程。README 只保留公开的「心头好」清单，不展示 Folo 阅读规则或账户聚合指标。

阅读原则见[《Feed 阅读的正确姿势》](https://niracler.com/feed-reading-posture/)：Feed 是甜点而非主食。每周最多投入 180 分钟；到点即停，不把未读数当成必须还清的债务。

## 组织方式

- View 管媒介形态。
- Category 管主题。
- List 管阅读场景。
- Action 和 Spotlight 管筛选与提醒，不替代源头减量。
- Star 是月度升降级信号，不是稍后读队列。

Category 统一为：

- 🪶 个人博客与朋友
- 🧠 AI 与软件工程
- 🏠 IoT 与智能家居
- 🏢 组织与产品
- 📰 新闻与精选摘要
- 🎮 ACG 与娱乐
- 🔒 私密内容
- 🧊 冷冻观察

只维护以下 3 个公开 List：

- `⚡ 每日核心`：不超过 15 个源，预计不超过 35 条/周。
- `🧁 周六甜点`：深度内容，平时无需即时阅读。
- `🛠 Changelog`：目标 25 个、上限 30 个核心软件源。

私密源不加入公开 List。私密源保留在「🔒 私密内容」，并从总时间线隐藏。异常私密源不移动到「🧊 冷冻观察」，避免打破私密分类边界。

## 阅读预算

| 入口 | 每周预算 | 处理方式 |
|------|----------|----------|
| ⚡ 每日核心 | 60 分钟 | 保留未读 |
| 🧁 周六甜点 | 75 分钟 | 周六集中阅读 |
| 🛠 Changelog | 15 分钟 | 普通更新周六阅读，关键变化即时提醒 |
| 娱乐 | 30 分钟 | 主动进入，结束后不保留未读债务 |

总时间线只显示每日核心。其他内容从 View、Category 或 List 主动进入。

## Folo 设置

通用设置：

- 开启「启动时仅显示未读」「隐藏已读」「隐藏私密订阅」「按日期分组」。
- 开启「滚动离开后标记为已读」。
- Social、Pictures 等单项内容进入视图后标记为已读。
- 关闭「自动按域名分组」「悬停时标记为已读」「自动展开长社交内容」和 Dock 未读徽章。
- 顶部常驻标签保留 Articles 与 Notifications。

「隐藏已读」会让零未读的 List 和 Category 暂时从侧边栏消失，但不会删除内容。

## 内容治理

高流量源按以下顺序处理：

1. 替换为官方 changelog、日报、Newsletter 或精选 Feed。
2. 没有合适替代时，隐藏到对应 Category。
3. 最后才使用 Action Rule 屏蔽明确噪声。

NGA、Pixiv、网盘和论坛流作为不积累未读的娱乐入口。429、5xx、抓取故障和疑似休眠源进入「🧊 冷冻观察」，观察 30 天后再决定恢复或退订。低频不是删除理由；删除前必须备份并生成候选预览。

月度升降级使用以下信号：

- 每周超过 25 条且 90～180 天零 Star：检查是否需要替换或隐藏。
- 低频且收藏命中率高：候选提升到每日核心。
- 高频但偶有精品：放入周六甜点。
- Changelog 不按 Star 命中率淘汰。

## Changelog 与提醒

来源优先级：

1. 官方产品 RSS。
2. GitHub Releases Atom。
3. 官方 release notes。
4. 产品专属博客。

Spotlight 关注以下变化：

- 安全：`CVE-|security|vulnerability|breach|漏洞|安全更新|泄露`
- 兼容性：`breaking|deprecated|deprecation|EOL|migration|弃用|下线|迁移`
- 商业与隐私：`pricing|price change|terms|privacy|涨价|价格|条款|隐私`

Action Rule 使用 changelog Feed URL 正则限定来源。只有安全、Breaking、弃用、迁移、价格或隐私变化执行「通知 + Star」；普通更新留到周六阅读。

AI Timeline Prompt 使用既定阅读原则。AI 排序只作为第二层排序，不代替隐藏和源头减量。

## 每月维护

操作前先备份。原始备份只能保存在 Git 忽略的 `.tmp/`，不得提交到仓库。

1. 导出 OPML 和 Action Rules。
2. 生成匿名快照：

   ```bash
   python3 .github/scripts/audit_folo.py --output audit/folo-snapshot.json
   ```

3. 运行审计测试：

   ```bash
   python3 -m unittest discover -s tests -v
   ```

4. 复核每日核心、Changelog、未分类、异常源和核心单源流量占比。
5. 观察 7 天的核心流量；观察 30 天后处理冷冻源。

匿名快照只保存生成时间、聚合计数、各入口流量、Star 命中率和预计注意力。快照不得包含账号、Feed 或 List ID、标题、URL、凭据和私密明细。pre-commit 与 CI 只读取快照，不登录 Folo。
