# 采集与维护规则

> 本文为 TechNews 每日采集与来源维护的执行规则。2026-10-11 修订（TECH-4 首次维护，替代旧版「固定 Issue 去重」与「自动化永不修改」规则）；2026-10-12（TECH-11）自科技情报来源清单.md 移入 rules/，规则内容仅更新文件引用，未改变授权与阈值。来源清单权威文件为 `config/sources.json`。

1. 只按 `config/sources.json` 已启用来源采集，不凭记忆添加来源；根部 科技情报来源清单.md 仅为只读展示版，不作为采集依据。

2. 去重以规范化 URL（去跟踪参数、保留语义参数）为准，对照持久台账 `state/processed-urls.json`；同一事件的一手与转述合并为一条。

3. T1 一手内容优先级高于 T2 转述；T3 只取高热度/被广泛讨论的论文与模型发布，不做全量论文列表。

4. `config/sources.json` 由每日运行自动维护（2026-10-11 起，经 GuoHui 确认授权）：
   - 健康状态记录于 `state/source-health.json`，维护决定与证据记录于 `state/maintenance-log.md`；简报为纯新闻内容，不含来源健康段。
   - 单次不可达或当天 0 产出不删除、不降级；连续 3 次真实探测失败且替代入口验证失败降为待观察；连续 30 个成功采集日无产出降级，不永久删除；恢复需连续 2 次验证可达。
   - 有验证有效的官方 RSS 或迁移地址可更新入口，保留原地址和原因；新来源需在已启用 T2 中被至少 3 条独立热点条目引用并验证后纳入。
   - 任何修改前先在 `backup/` 保存旧文件（`backup/sources-YYYYMMDD.json`；同日已有同名备份且内容不同时用 `backup/YYYYMMDD-HHmmss/` 子目录，禁止覆盖任何历史版本）并校验字节一致，再原子替换；备份失败不得修改 `config/sources.json`。
   - 修改 `config/sources.json` 后运行 `python3 scripts/validate.py --generate-md` 重新生成只读展示版并校验一致性。

5. 候选待观察来源不纳入常规采集。
