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

## 2026-10-15（TECH-23）

- 采集窗口：2026-10-13T00:03Z 至 2026-10-15T00:03Z（48h）。26 个启用源全部执行采集：22 源 ok，theinformation 403（付费墙持续，维持 paywall），netflix feed 200 但时间戳异常（见下）。
- Netflix feed 时间戳异常：10 篇文章 pubDate 集中于 2026-10-14T19:48–20:02Z，逐篇外部核验均为旧文（Integrating FM 原发 2025-11-17、DataJunction 2026-02-24、Conductor 2026-08-17、LLM-as-a-Judge 2026-09-09 等），全部按窗口外排除。后续 Netflix 窗口判定须逐篇核验原发时间，不得依赖 Medium feed pubDate（已记入 source-health notes）。
- airbnb：上轮本机 SSL 层不可达计失败 1 次；本轮 medium feed 200 + airbnb.tech 200 恢复可达（CASTLE 原发 2026-10-13 入选），失败连击中断，保持 enabled（状态 ok）。linear RSS 三入口均 200 但 0 条，HTML 入口正常，最新 changelog 2026-10-08 窗口外。
- 技术备注：deepmind RSS 与页面为 gzip 编码，抓取需解压；fetch 工具受本机 fake-IP 代理限制，HTML 源改用脚本直抓。
- 降级/删除/入口变更：无。config/sources.json 本轮无改动，未重写、未生成备份（规则：无改动不重写）。
- 候选来源线索：无新增（未发现 T2 中 ≥3 条独立热点引用同一新来源）。
- 台账与发布：10 事件 15 URL 入 published（含同事件前报 yandex-dc-drone/yandex-bot-traffic-collapse 的关联标注；d1-control-plane 为 TECH-20 评排后本轮复评首次发布，历史评排记录保留于条目 note），评估后明确排除 29 条（窗口外 11——Netflix 旧文重刷 10 与 linear changelog 1；位次不足 16；T3 位次不足 2；另有 6 条与既有排除台账重复自动跳过），见 state/processed-urls.json。
- 发布：reports/digest-2026-10-15.md，10 条事件；提交分支 main。

## 2026-10-16（TECH-26）

- 采集窗口：2026-10-14T00:02Z 至 2026-10-16T00:02Z（48h）。26 个启用源全部执行采集：25 源 ok，theinformation 403（付费墙持续，维持 paywall）。
- Netflix feed 时间戳重刷再现：10 篇 pubDate 集中于 2026-10-14T19:47–20:02Z；抽样核验 Ads Event Pipeline Part II 原发 2026-08-17（Medium 页面），全部按旧文重刷排除。本机直抓 netflixtechblog 被 Cloudflare 拦截（"Attention Required"），未能逐篇独立复核原发时间；上轮确立的"逐篇核验"要求维持，待可核验环境复核。
- Anthropic sitemap lastmod 误导再现：three-branches-of-government 页面 datePublished 2025-08-12，按窗口外排除（与上轮酶系统文同型）。
- 各源窗口概况：airbnb/shopify/anthropic_research 窗口内 0 新文（feed 正常）；a16z HTML 未提取到窗口内链接（连续两轮）；cursor 最新仍为 2026-09-23；sierra 最新 2026-10-06；linear 最新 changelog 2026-10-08；meta_ai 窗口内新增仅 muse-spark-open（其余逐条核验为 10-02 及更早）；scale 窗口内 2 条均密度不足。
- 降级/删除/入口变更：无。config/sources.json 本轮无改动，未重写、未生成备份（规则：无改动不重写）。
- 候选来源线索：无新增（未发现 T2 中 ≥3 条独立热点引用同一新来源）。
- 台账与发布：10 事件 20 URL 入 published；评估后明确排除 88 条（窗口外 15、位次不足约 40、密度/领域不符及评论约 20、活动促销 3、Netflix 旧文重刷 6），见 state/processed-urls.json。
- T3 说明：HF Daily Papers 10-14/15 两批次各 50 条，最高 ATAS 2610.20571（323 赞）入选；Player-1（255）等 7 条位次不足排除，其余 <120 赞未逐一入账。arXiv 三频道仅作筛选输入。
- 发布：reports/digest-2026-10-16.md，10 条事件；提交分支 main。

## 2026-10-17（TECH-38）维护记录

- 采集窗口：2026-10-15T00:02Z ~ 2026-10-17T00:02Z（48h）；26 个启用源全部按既定入口探测，无采集失败（theinformation 维持 paywall 状态，非本轮新增异常）。
- **config/sources.json 无改动**：无来源降级/恢复/入口变更；按规则未重写清单、未生成备份、未重新生成展示版。
- 健康要点（计入连续计数，见 state/source-health.json）：
  - netflix：feed 时间戳重刷再现（第2轮发现）。ontology-driven-observability pubDate 10-16，外部核验（Medium 官方列表页）原发 2026-09-25、内容为 2026-03 QCon London 演讲，按旧文重刷排除；netflixtechblog.com 直抓 403，维持逐篇核验要求。
  - a16z：连续第 3 轮页面 200 但 0 条窗口内链接（JS 渲染列表）；未达降级阈值（单次/连续少产出不降级，30 个成功采集日无产出才降级），继续观察。
  - vercel：atom feed link 字段缺失（href 形态未解析），URL 经 slug 验证补全；且同日两次抓取返回不同内容集合（一次含2024旧条目），feed 不稳定，下轮可评估改用 blog 专用 RSS。
  - theinformation：403 付费墙持续。
  - xai/perplexity/uber/doordash/sequoia：候选待观察沿用，未探测（不纳入常规采集）。
- 本轮入选 10 条（4 条 T1 一手、2 条 T2 一手报道主体、2 条 T2 转述+6 条 HN secondary、2 条 T3 高热论文），无凑数；排除 57 条并入台账（详见 state/processed-urls.json，issue=TECH-38）。

## 2026-10-18（TECH-43）维护记录

- 采集窗口：2026-10-16T00:02Z ~ 2026-10-18T00:05Z（48h）；26 个启用源全部按既定入口探测，无采集失败（theinformation 维持 paywall 状态，非本轮新增异常）。
- **config/sources.json 无改动**：无来源降级/恢复/入口变更；按规则未重写清单、未生成备份、未重新生成展示版。
- 健康要点（计入连续计数，见 state/source-health.json）：
  - arxiv_cscl/cs.LG：RSS 返回周末空批（skipDays Sat/Sun，lastBuildDate 10-17），属正常排程而非故障；cs.AI 内容与上轮周五批次一致，无新增。
  - hf_papers：10-17 批次 API 返回空数组（周末批次未发布）；10-16 批次 50 条为上轮已评估条目复核。另记录：昨日按 T3 位次排除的 FLUX 3 Image Klein 热度升至 HN 206分（昨 91分），事件已明确排除入账，不重开。
  - vercel：atom feed 本轮 link 字段解析正常（上轮缺失问题未复现）；feed 不稳定观察项延续。
  - a16z：连续第 4 轮页面 200 但 0 条窗口内链接（JS 渲染列表），未达降级阈值，继续观察。
  - theinformation：403 付费墙持续。xai/perplexity/uber/doordash/sequoia：候选待观察沿用，未探测。
- 周末因素：新闻产出偏少。本轮入选 6 条（DeepSeek 模型发布、OpenCode 凭据泄露、OpenAI 智能体事件披露、Meta 条款调整、MapQuest/Flock、Amazon 工会监控 AI），无凑数；Tesla Roadster（HN 1600分）延续 TECH-38"领域不符：汽车产品营销"口径排除。
- 台账与发布：6 事件 17 URL 入 published，评估后明确排除 99 条（窗口外 8、旧文/旧仓库回热 8、领域不符 41、位次不足 30、Show HN/非新闻 12，详见 state/processed-urls.json，issue=TECH-43）。
- 发布：reports/digest-2026-10-18.md，6 条事件；提交分支 main。

## 2026-10-19（TECH-46）维护记录

- config/sources.json：无改动（未备份、未重写展示版——规则：无改动不重写）。
- 采集健康：22 个常规源中 19 个本轮实际探测（RSS/Atom/API/sitemap 为主），全部可达；theinformation 403（付费墙持续）；meta_ai/sierra/scale/linear/cursor/a16z 本轮未复检，沿用上轮结论（无窗口内新文迹象）。
- arXiv 周末空批（lastBuildDate 2026-10-18T04:00Z）、HF Daily Papers 10-17/10-18 空批次：均属发布节奏而非故障，不降级。
- deepmind feed 首轮 gzip 解码失败，属抓取端编码处理问题，补 Accept-Encoding 后 200，不计为源失败。
- 候选待观察（xai/perplexity/uber/doordash/sequoia）：未探测，记录沿用。
- 新来源评估：无满足"已启用 T2 中 ≥3 条独立热点引用"条件的新来源。

## 2026-10-20（TECH-49）维护记录

- config/sources.json：无改动（未备份、未重写展示版——规则：无改动不重写）。
- 采集健康：26 个启用源全部按既定入口探测。25 源 ok（RSS/Atom/API/sitemap/HTML），theinformation 首页本轮 200 但内容付费墙（仅标题可见），维持 paywall；未采集成功为 0 源。
- mistral 入口 301 → 跟随重定向 200（ mistral.ai/rss.xml），不计为源失败。
- arXiv：周一 10-19T04:00Z 批次正常到达；cs.AI RSS 批次 0 条目（批次为空，非抓取失败），cs.CL/cs.LG 共 617 条作为筛选输入。
- HF Daily Papers：10-18 批次空数组（延续周末节奏）；10-19 批次 50 条，HexaShell（284 赞当日最高）按 T3 高热度口径入选。
- 旧文回热提示：Timestral（TECH-26 已发布）、CERN×Mistral（原发 10-15）、NVIDIA Nemotron 3.5（官方 10-15）、employment-at-anthropic / ai-expectations-gap（TECH-38 已并入研究日条目）、HybridAgents（同 HN id 50145337 回热至 502 分）均按"已发布/窗口外原发不重开"口径排除。
- a16z：连续第 6 轮页面 200 但 0 条窗口内链接（JS 渲染），未达降级阈值（30 个成功采集日无产出），继续观察。
- vercel：atom feed link 解析正常（上轮问题未复现）。
- 候选待观察（xai/perplexity/uber/doordash/sequoia）：未探测，记录沿用。
- 新来源评估：无满足"已启用 T2 中 ≥3 条独立热点引用"条件的新来源。
- 台账与发布：10 事件 24 URL 入 published（含 secondary 链接核验），评估后明确排除 57 条（窗口外原发 3、已发布事件跟进 5、位次不足 24、领域不符 14、项目展示/Show HN 6、观点随笔/教程 4、旧文回热 5 等，详见 state/processed-urls.json，issue=TECH-49）。
- 发布：reports/digest-2026-10-20.md，10 条事件；提交分支 main。

## 2026-10-21（TECH-52）例行维护

- 采集窗口：2026-10-19T00:00Z – 2026-10-21T00:05Z（48h）。26 个启用来源全量采集，全部成功返回（其中 theinformation 为首页 200/正文付费墙，维持 paywall；linear 为 SPA 渲染无可解析条目，与上轮一致）。
- 产出：Top10 全部 10 条发布（见 reports/digest-2026-10-21.md）；健康与逐条排除证据见 state/source-health.json 与 state/processed-urls.json。
- 特别核验：anthropic sitemap lastmod 出现站点级批量刷新（含 2024 年旧研究页），不作为发布时间依据；/news/claude-code-on-the-web 经页面核验为旧页 HN 重提，排除。openai feed 中 introducing-chatgpt-atlas pubDate 为周年刷新产物（产品已弃用），排除。hn 中 GlassWorm（koi.ai）自述原事件为 2025-12，排除。
- config/sources.json：无改动（无来源触发连续 3 次探测失败或连续 30 日无产出条件；无新增入口；未发现满足纳入标准的新来源），故不创建备份、不重新生成展示版。
- 候选待观察（xai/perplexity/uber/doordash/sequoia）沿用，不纳入常规采集。

## 2026-10-22（TECH-55）例行维护

- 采集窗口：2026-10-20T00:00Z – 2026-10-22T00:55Z（48h）。26 个启用来源全部按既定入口探测，全部成功返回（theinformation 首页 200/正文付费墙，维持 paywall；linear 重定向 /now SPA 与 sierra/scale/shopify 无可解析带日期条目，与上轮一致）。
- 产出：Top10 全部 10 条发布（见 reports/digest-2026-10-22.md）；10 事件 30 URL 入 published，评估后明确排除 59 条并入台账（详见 state/processed-urls.json，issue=TECH-55）。
- 特别核验：Mistral Large 4 官方原发 2026-10-06，HN 315 分为旧文回热，按窗口外原发排除；eMudhra（含 Scott Helme 822 分）与 Meta Muse 下载破千万均为 TECH-52 已发布事件回热/跟进，不重开；anthropic sitemap lastmod 延续站点级批量刷新现象，新增页以页面 datePublished 核验（attack-surface-reduction 与 scorpion-toxin-binder 均 10-20 发布）。OpenAI「Patch the Planet」与 PHP 双 RCE（Wiz/php.net/PHP Foundation）合并为同一事件条目。
- T3 口径：10-22 批次未发布（API 400，正常节奏）；10-20 批次最高 Matrix-Game 4.0（178 赞）与 PAR（147）按位次不足排除；Focused Omni-Modal GUI Agents（224 赞）为 10-19 批次窗口外原发；本轮 T1/T2 供给充足，T3 不凑数。
- config/sources.json：无改动（无来源触发连续 3 次探测失败或连续 30 日无产出条件；无新增入口；未发现满足纳入标准的新来源），故不创建备份、不重新生成展示版。
- 健康要点：a16z 连续第 7 轮页面 200 但 0 条窗口内链接（JS 渲染），未达降级阈值，继续观察；vercel atom 本轮解析正常；mistral 301→/news/rss 沿用（不计失败）；arXiv 周一批次正常到达（cs.AI 473/cs.CL 239/cs.LG 408 条，作筛选输入）；deepmind/netflix/airbnb/stripe feed 200 无窗口内条目。
- 候选待观察（xai/perplexity/uber/doordash/sequoia）：未探测，记录沿用。
- 新来源评估：无满足"已启用 T2 中 ≥3 条独立热点引用"条件的新来源。
- 发布：reports/digest-2026-10-22.md，10 条事件；提交分支 main。

## 2026-10-23（TECH-58）来源维护

- **shopify 入口迁移**：`https://shopify.engineering` → `https://shopify.engineering/blog.atom`。原因：原 HTML 入口为 JS 渲染页不可解析（TECH-4 起多轮如此），`/rss`、`/feed` 本轮实测 404；本轮验证官方 Atom feed（HTTP 200，436 条目，feed 内 self 声明 `blog.atom`）可用并产出 2 条窗口内条目。原地址按规则保留于 notes。
- **备份**：`backup/sources-20261023.json`（sha256 `6380c5f6c3a93ece84e58307490bfd2e9eab4b24b6aead85921ae3339f597a7d`，与修改前原文件字节一致，已核验）；清单 `updated_at` → 2026-10-23；展示版已由 `validate.py --generate-md` 重新生成。
- **其余 25 个启用来源**：无清单改动（入口与状态均不变）；meta_ai RSS 探测 /feed 404 为单次失败（页面 200 正常），linear rss 0 条目、hf_papers 10-22 批次 API 抓取失败均为单次异常，均记录于 state/source-health.json，未达任何降级阈值，不降级不删除。
- 候选待观察来源（xai/perplexity/uber/doordash/sequoia 等）本轮未探测，状态不变。

## 2026-10-24（TECH-61）例行维护

- 采集窗口：2026-10-22T01:16Z – 2026-10-24T01:16Z（48h）。26 个启用来源全部按既定入口探测并成功返回（theinformation 首页 403 反爬/正文付费墙维持，linear feed 解析 0 条目为 SPA 既有状况，均不计为新故障）。
- 抓取端异常（非源故障）：deepmind feed 返回 gzip 压缩体（Accept-Encoding: identity 被忽略），本地解压后解析正常；arxiv_csai 首轮 SSL EOF 瞬时失败，重试 200；meta_ai /rss 与 /blog/rss.xml 404（与上轮一致的单次失败，页面 200 正常）。
- 产出：Top10 全部 10 条发布（见 reports/digest-2026-10-24.md）；15 URL 入 published（含 Part I 背景链接 secondary），71 条评估后明确排除入台账（详见 state/processed-urls.json，issue=TECH-61）。
- 特别核验：MIT「Agent 玩耍」研究（TechCrunch 10-22 报道、HN 热议）经 arXiv API 核验原发 2026-10-05，按"窗口外原发不重开"口径排除（同 Mistral Large 4 先例）；Calif iPhone（HN 740 分）原发 2026-10-16、Crystal 1.22 原发 10-12，均按窗口外原发排除；CVE-2026-111943/eMudhra 系列与 PHP embargo/AWS PHP2Shell 情报均为 TECH-52 已发布事件跟进，不重开；anthropic sitemap lastmod 延续站点级批量刷新（81k-economics 页面核验原发 2026-04-22）；openai decisions-api 上轮已发布。
- T3 口径：HF 10-23/10-22 批次共 100 条（10-24 周六批次未发布，正常节奏），最高 StreamEval 431 赞，本轮 T1/T2 供给充足，T3 不凑数。
- 健康要点：a16z 连续第 8 轮页面 200 但 0 条窗口内链接（JS 渲染），未达降级阈值，继续观察；vercel atom 解析正常（10 条窗口内）；mistral 301→/rss.xml 沿用不计失败。
- config/sources.json：无改动（无来源触发连续 3 次探测失败或连续 30 日无产出条件；无新增入口；未发现满足纳入标准的新来源），故不创建备份、不重新生成展示版。
- 候选待观察（xai/perplexity/uber/doordash/sequoia）：未探测，状态不变。
- 新来源评估：无满足"已启用 T2 中 ≥3 条独立热点引用"条件的新来源。
- 发布：reports/digest-2026-10-24.md，10 条事件；提交分支 main。

## 2026-10-25（TECH-65）例行维护

- 采集窗口：2026-10-23T00:05Z – 2026-10-25T00:05Z（48h）。26 个启用来源全部按既定入口探测（theinformation 首页 403 反爬/付费墙维持 paywall，不计新故障）。
- 周末节奏（非故障）：arxiv_csai / arxiv_cslg 返回空频道（rss 200，skipDays Sat/Sun，892 字节仅频道头）；hf_papers 10-24（周六）批次 0 条（10-23 批次 49 条已于 TECH-61 评估入账，不重开）。
- 入口异常：linear feed.xml 本轮返回 SPA HTML（200，不可解析）；此前 TECH-55/61 为可解析但 0 条目。站点主服务正常，单源入口问题记录观察，未达降级阈值。
- 健康要点：a16z 连续第 9 轮页面 200 但 0 条窗口内链接（JS 渲染），未达降级阈值，继续观察；anthropic sitemap lastmod 站点级批量刷新现象延续（大量 2026-10-23T20:56Z 同戳），新增/变更页一律以页面 datePublished 核验；meta_ai 列表页所列 Muse Spark 系列经页面核验均为旧文（1.1=07-09、1.2=08-05）；cursor self-driving-codebases 核验为 2026-02-05 旧页；github feed 最新条目 10-22（窗口前）。
- 产出：Top10 全部 10 条发布（见 reports/digest-2026-10-25.md）；18 URL 入 published（10 主源 + 8 secondary）、31 条评估后明确排除入台账（详见 state/processed-urls.json，issue=TECH-65）。
- 特别核验：anthropic alignment-assessment-ukaisi 页面 datePublished 2026-10-23（与 AISI 独立报告同步发布），为窗口内真实新研究页并入选；Dream-1（页面标注 10-18）、丹麦政府 MS Office（原文 10-20T06:33Z）、Samsung TV root（推文 10-21T21:06Z）、Roku→GitLab（gitlab.com/rokudev 仓库批量创建 10-15）均为窗口外原发、HN 10-24 回热，按「窗口外原发不重开」排除；Apple Security Research Device 页面无发布日期无法核验，排除。Brotli CVE-2026-111497 以 10-23「HTTP2Shell 扩散 + 补丁铺开」为窗口内事件入选（Node 首披 10-21 作时间线背景，此前未入账）。PHP 基金会资金报道（Reuters 10-23）为 TECH-52 已发布漏洞事件之后的独立后续报道，按新事件收录。
- T3 口径：HF 10-24 批次 0 条；T3 入选 1 条（arXiv 2610.29162，提交 10-21、cs.CL 10-24 批次、HN 146 分/143 评，热度达标，提交时间透明标注）。
- config/sources.json：无改动（无来源触发连续 3 次探测失败或连续 30 日无产出条件；无新增入口；未发现满足纳入标准的新来源），故不创建备份、不重新生成展示版。
- 候选待观察（xai/perplexity/uber/doordash/sequoia/jiqizhixin/qbitai 等）：未探测，状态不变。
- 新来源评估：无满足「已启用 T2 中 ≥3 条独立热点引用」条件的新来源。
- 发布：reports/digest-2026-10-25.md，10 条事件；提交分支 main。
