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

## 2026-10-12（TECH-13 · 例行采集维护）

- **变更类型**：仅健康台账更新；`config/sources.json` 本轮无改动，未重写、未生成备份（规则：无改动不重写）。
- **采集执行**：2026-10-12T00:01–00:28 UTC，窗口 2026-10-10T00:01:53Z 起 48 小时；31 个在册启用来源全部尝试。
- **可达性**：25 源 ok（含 linear 恢复），The Information 维持付费墙，6 源 blocked：meta_ai(400)、xai(403)、perplexity(403)、uber(406/404)、doordash(403)、sequoia(404)。
- **连续失败计数滚动**：上述 6 源均为 2/3；替代入口本轮全部验证失败（meta blog/feed 400、xai /news 403、perplexity hub/rss/blog 403、uber eng.uber.com/feed 404、doordash blog/feed 403、sequoia /rss/ 与 /news/ 404）。按阈值，下轮若第 3 次探测仍失败且替代入口仍不可达，将降为待观察；sequoia 已连续两轮 404，建议成员人工确认新地址。
- **恢复记录**：linear 上轮 TLS 层被拒（1/3），本轮 HTML 入口恢复 200（验证恢复第 1 次，RSS blog/rss.xml 为 404 不存在，入口以 HTML 为准）；按规则待连续 2 次验证可达后计数清零。
- **降级/删除**：无（单次不可达或 0 产出不降级；无源达到降级阈值）。
- **新来源评估**：无新增。TECH-4 记录的候选线索（Oxide、TypeSafe、Microsoft Command Line）本轮窗口内未出现，继续观察。
- **入口变更**：无（deepmind 需 gzip 解压抓取为抓取方式备注，非入口变更）。
- **T3 说明**：arXiv 三频道周末空批次、HF Daily Papers 窗口内无新批次（最新 10-08，最高赞 38），未达收录门槛，不凑数。
- **产出**：发布 10 条（14 个 URL 入 published 台账），评估后明确排除 21 条（窗口外 3、重复/已发布事件 2、密度或相关性不足 12、付费墙不可核验 1、活动宣传 2、其他 1），见 state/processed-urls.json。

## 2026-10-13（TECH-17）例行维护：meta_ai 入口迁移；5 源降为待观察

- 触发：TECH-17 采集轮（窗口 2026-10-11T00:00Z～2026-10-13T00:00Z）。
- 阈值动作：xai、perplexity、uber、doordash、sequoia 连续第 3 次真实探测失败（TECH-4/13/17 三轮；403/406/404），替代入口复验全部失败，按 rules/collection.md 降为候选待观察（status=candidate，tier=null），未删除任何来源；恢复需连续 2 次验证可达。sequoia 新地址待人工确认。
- 入口迁移：meta_ai 原入口 ai.meta.com/blog 及 /feed/ 连续 3 轮 400 反爬；官方研究博客 research.meta.ai/blog 验证 200 并在本窗口产出一手内容（Muse Wonder），入口迁移至该地址，原地址保留于 notes。
- 备份：config/sources.json 旧版本（updated_at 2026-10-11，7593 字节，sha256 977a4e3a99b7d493…前16位，完整值见备份校验）→ backup/sources-20261013.json（字节/hash 一致校验通过）；同日无同名历史备份。替换经 config/sources.json.tmp 原子完成，替换前复核原文件 hash 未变化。
- 展示版：python3 scripts/validate.py --generate-md 重新生成根部只读展示版；全量校验通过。
- 其余来源：本轮无入口/状态改动（shopify 官方 atom feed 验证有效但原入口可达，未改配置；linear 连续第 2 次验证可达）。

## 2026-10-14（TECH-20）例行维护：无清单改动

- 触发：TECH-20 采集轮（窗口 2026-10-12T00:01Z～2026-10-14T00:01Z，采集执行 2026-10-14T00:01–00:55 UTC）。
- 可达性：26 个启用来源全部尝试，25 源 ok，1 源 blocked：airbnb（medium.com/feed 本机 TLS 握手被中断，curl×3 + python urllib 均失败，非 HTTP 状态码）；The Information 维持付费墙。
- 连续失败计数：airbnb 1/3，单次不可达不降级，下轮复测。其余启用源无失败。
- 恢复记录：linear 连续第 3 次验证可达（2026-10-13 起恢复计数已完成，保持 ok）。
- 降级/删除/入口变更：无。config/sources.json 本轮无改动，未重写、未生成备份（规则：无改动不重写）。
- 采集与筛选证据：发布 10 条事件（22 个 URL 入 published 台账），评估后明确排除 21 条（窗口外 1——Anthropic 酶系统文原发 2026-09-23、sitemap lastmod 2026-10-13 误导；位次不足 13；密度不足 5；非新事件/非新闻 2；另有 3 条与既有排除台账重复自动跳过），见 state/processed-urls.json。
- T3 说明：arXiv 三频道 RSS 空批次（lastBuildDate 2026-10-13T04:00Z）、HF Daily Papers 窗口内无新批次（最新 10-08/09）；本期 T3 入选 1 条为 HN 高热论文（arXiv 2610.13928，提交 10-09，HN 271 分讨论 10-13），按"高热度/广泛讨论"门槛收录。
- 候选来源线索：无新增（未发现 T2 中 ≥3 条独立热点引用同一新来源）。
