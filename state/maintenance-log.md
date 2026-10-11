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

## 2026-10-12（TECH-11 · 结构迁移，非采集维护）

- **变更类型**：项目结构统一（GuoHui 授权 Issue TECH-11），不改变来源表内容与维护授权。
- **迁移**：权威来源清单由根部 科技情报来源清单.md 无损迁移至 `config/sources.json` v1；31 个启用来源 + 4 个候选逐一对应（`python3 scripts/validate.py --migrated-from` 交叉核验通过：名称、URL、层级、分组、状态一致）。
- **source_id 映射**：启用来源全部沿用 `state/source-health.json` 既有 id；新增候选 id：jiqizhixin、qbitai、stratechery、benevans。
- **备份**：迁移前原字节备份 `backup/20261012-000118/科技情报来源清单-20261012.md`，sha256 `a0d73c383fd493969dccd952cbaba113a273fd8582bd1c7861848ab38ce25b36`，cmp 校验一致；未覆盖既有历史备份 `backup/科技情报来源清单-20261011.md`。
- **展示版**：根部 科技情报来源清单.md 转为只读展示版（`python3 scripts/validate.py --generate-md` 生成），权威来源与生成命令已在文首注明。
- **执行规则**：使用规则（2026-10-11 修订版，含阈值）原样移入 `rules/collection.md`，仅更新文件引用；未恢复任何已替代的旧规则。
- **简报目录**：本次及后续简报归档于 `reports/digest-YYYY-MM-DD.md`；`state/daily-runs.json` 的 briefing_file 已同步为相对路径（2026-10-11 记录键值与计数不变，同日去重逻辑不受影响）。`old/` 保持既有归档策略不动。
- **数据契约**：新增 `docs/data-contract.md`；校验脚本 `scripts/validate.py`（配置、来源 id 唯一性、字段、启用状态、URL、state 契约、展示一致性）。
- **来源表改动**：无（本条目仅为结构迁移记录，非来源维护）。
