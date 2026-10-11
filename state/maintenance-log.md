# 来源清单维护日志

## 2026-10-11（TECH-4 · 首次维护）

- **变更类型**：使用规则修正（首次同步 2026-10-11 生效的运行授权）+ 版本行新增；来源表未改动。
- **修正内容**：
  - 旧规则2「去重对照固定Issue已发布评论」→ 改为对照 `state/processed-urls.json` 持久台账；
  - 旧规则4「自动化永不修改本文件/日报含来源健康段」→ 改为每日运行自动维护（GuoHui 已确认授权），健康与维护信息保存在 `state/`，简报为纯新闻内容；
  - 补充降级/恢复阈值、备份流程与新来源纳入门槛。
- **旧版本信息**：原文件无内部版本日期，取文件 mtime `2026-09-14 16:05:42 +0800` 为旧版最后更新时间。
- **备份**：`backup/科技情报来源清单-20261011.md`（同日首份备份）；sha256 `9dc7dad9b6bbec4b158c958ea9898555a52ef257e17922fd118447794adaf033`，与原文件字节一致校验通过（cmp 通过）。原文件替换前 hash 复核一致，无并发编辑。
- **替换方式**：同目录临时文件原子替换（edit 工具写入后落盘）。
- **新来源评估**：无符合「T2 中 ≥3 条独立热点引用」门槛的候选（Oxide Computer、TypeSafe AI、Microsoft Command Line 本期各出现 1 次，继续观察，暂不纳入）。
- **降级/待观察/恢复**：无（首次运行，无连续失败计数基础；blocked 源见 source-health.json，失败计数 1/3）。
- **替代入口发现**（记录待下次运行采用）：
  - Anthropic News/Research：无官方 RSS（rss.xml/feed.xml 404），可用入口 `sitemap.xml`（含 lastmod）+ HTML；
  - Shopify Engineering：无 RSS（404），HTML 可用；
  - a16z：`a16z.com/feed/` 404，HTML 可用；
  - Sequoia：`/rss/` 与 `/articles/` 均 404，需人工确认新地址（暂计 blocked 1/3）。
- **付费墙**：The Information 维持付费墙状态，仅作标题级热度参考。

### 本期采集证据摘要

- 采集窗口：2026-10-09T04:34Z → 2026-10-11T04:34Z（48h）；采集执行 2026-10-11T04:34–04:50Z。
- 31 个在册来源全部尝试：23 个可达（RSS/Atom/API/HTML/sitemap），7 个 blocked（meta_ai、xai、perplexity、uber、doordash、linear 为 TLS 层拦截或拒绝，sequoia 入口 404，详见 source-health.json），The Information 为付费墙（可达但仅作热度参考）。
- 窗口内候选：T1 共 12 条（Cloudflare 3、Anthropic 3、OpenAI 2、GitHub 1、Vercel 3），T2 供给 60+13 条，T3 供给 50 条（论文）。
- 发布 10 条（13 个 URL 入台账）；评估后明确排除 14 条（窗口外 4、密度不足 7、非新事件 2、未入选 1——见 processed-urls.json）。
- 未采集成功不计为 0 产出：blocked 源不计产出数，仅记失败状态。
