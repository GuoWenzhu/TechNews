# TechNews 数据契约

本文描述 TechNews 的目录结构、配置文件 schema 与持久数据契约。多轮运行（自动化、人工、其他任务）必须遵守本契约，避免重复发布、覆盖台账或双份维护。

## 目录结构

```text
TechNews/
├── README.md                  # 项目说明（读者入口）
├── .gitignore                 # 忽略 old/、backup/、data/ 内容、.DS_Store 与运行时文件
├── config/
│   ├── project.json           # 项目级配置：采集参数、权威文件指针、输出目录
│   └── sources.json           # 唯一权威来源清单（来源配置）
├── rules/
│   └── collection.md          # 采集与维护执行规则（含备份流程、降级/恢复阈值）
├── docs/
│   └── data-contract.md       # 本文
├── scripts/
│   └── validate.py            # 配置与数据契约校验、展示版生成、迁移交叉核验
├── state/                     # 持久运行台账（版本化 JSON + 维护日志，禁止清空重建）
│   ├── processed-urls.json    # 已处理 URL 台账（去重依据）
│   ├── source-health.json     # 来源健康（可达性、失败计数、替代入口）
│   ├── daily-runs.json        # 每日发布台账（同日去重发布依据）
│   └── maintenance-log.md     # 来源维护日志（决定与证据）
├── reports/                   # 简报归档 digest-YYYY-MM-DD.md
├── data/                      # 原始抓取临时文件（本地，不入 Git；不存在时可创建）
├── backup/                    # 配置/清单修改前的字节备份（本地，不入 Git，禁止覆盖历史）
├── old/                       # 2026-10-10 前历史简报归档（本地，不入 Git）
└── 科技情报来源清单.md          # 只读展示版：由 config/sources.json 生成，禁止手工编辑
```

## 职责分离

| 域 | 位置 | 说明 |
| --- | --- | --- |
| 来源配置 | `config/sources.json` | 名称、入口 URL、层级、分组、启用/候选状态、适用范围备注 |
| 来源健康 | `state/source-health.json` | 可达性、HTTP 证据、连续失败/成功计数、替代入口；不回写来源配置 |
| 执行规则 | `rules/collection.md` | 采集、去重、优先级、维护阈值与备份流程 |

## config/sources.json

- `version`：文件 schema 版本（当前 1）。结构演进必须向后兼容，并在 `docs/data-contract.md` 记录。
- `tiers`：T1/T2/T3 层级定义与优先级；启用来源必须引用合法层级，候选来源 `tier` 为 `null`。
- `sources[]`：扁平数组。每个条目必有 `id`（稳定 source_id，`^[a-z0-9_]+$`，全局唯一，一旦发布不重命名）、`name`、`tier`、`group`、`url`、`status`（`enabled` / `candidate`）、可选 `notes`。
- `url` 仅收录清单明示的入口；候选条目原清单未给出 URL 时为 `null`。
- 来源健康不入本文件；改入口、改状态按 `rules/collection.md` 备份流程执行，并同步重新生成展示版。

### source_id 映射

31 个启用来源的 `id` 沿用 `state/source-health.json` 既有键名（如 `anthropic_news`、`hn`、`arxiv_csai`），健康记录与来源配置通过同一 `id` 关联。2026-10-12（TECH-11）迁移前后来源数、URL、层级、启用状态一一对应，交叉核验命令：`python3 scripts/validate.py --migrated-from <原Markdown路径>`。新增来源沿用该 id 进入健康台账；删除或降级不改 id。

## state/ 持久台账

所有 JSON 均带 `version` 与说明性 `note`；损坏时保留原文件并报告，不得当空台账重新初始化。

### processed-urls.json（v1）

`entries[]` 按状态分两种形状，均含 `url`（规范化，全局唯一）、`title`、`issue`、`status`：

- `published`（已发布简报）：另含 `published_on`、`role`（`primary` / `secondary`）、`event`、`source_pub_time`。
- `excluded`（已评估并明确排除）：另含 `reason`（排除原因）、`evaluated_on`（评估日期）。

仅这两种状态入账；临时抓取失败不入账。每日去重对照本文件。

### source-health.json（v1）

`sources{}`：键为 source_id，与 `config/sources.json` 启用来源一一对应；值含 `tier`、`status`（`ok` / `blocked` / `paywall`）、`method`、`entry_used`、窗口内计数与证据。每次运行覆盖为最新一次采集结果，连续计数按维护规则滚动。

### daily-runs.json（v1）

`runs[]`：每条含 `date`（Asia/Shanghai 日期，至多一条成功发布）、`issue`、`issue_id`、`status`、`briefing_file`（自仓库根的相对路径，2026-10-12 起位于 `reports/`）、`items_published`、`git_branch`。同日重复运行对照本文件跳过，确保不重复发布。

### maintenance-log.md

按时间追加的维护决定与证据；只追加不重写历史条目。

## 简报与发布

- 简报写入 `reports/digest-YYYY-MM-DD.md`（纯新闻内容）；`old/` 保留 2026-10-10 前历史归档，不为整齐而迁移。
- 展示版生成：`python3 scripts/validate.py --generate-md`；一致性校验随默认校验执行（重新生成的文本必须与现存文件字节一致）。

## 校验

```bash
python3 scripts/validate.py                 # 全量校验：配置、来源、state 契约、展示一致性
python3 scripts/validate.py --generate-md   # 从 config/sources.json 重新生成只读展示版
python3 scripts/validate.py --migrated-from backup/.../科技情报来源清单-YYYYMMDD.md  # 迁移交叉核验
```

任何校验失败必须先修复再进入 Git 提交或发布流程。
