#!/usr/bin/env python3
"""TechNews 配置与数据契约校验。

用法:
  python3 scripts/validate.py                                # 全量校验（配置、来源、state 契约、展示一致性）
  python3 scripts/validate.py --generate-md                  # 从 config/sources.json 重新生成只读展示版
  python3 scripts/validate.py --migrated-from <原Markdown>    # 迁移无损交叉核验
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISPLAY_MD = ROOT / "科技情报来源清单.md"
TIERS = ("T1", "T2", "T3")
URL_RE = re.compile(r"https?://[^\s（）()，、|]+")
ID_RE = re.compile(r"^[a-z0-9_]+$")


def fail(errors, msg):
    errors.append(msg)


def load_json(path, errors):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        fail(errors, f"{path.name}: JSON 解析失败: {e}")
        return None


# ---------- 生成只读展示版 ----------

def generate_display(src: dict) -> str:
    lines = [
        "<!-- 由 config/sources.json 自动生成的只读展示版；请勿手工编辑。 -->",
        "",
        "# 科技情报来源清单（只读展示版）",
        "",
        "> **权威来源：[`config/sources.json`](config/sources.json)** —— 本文件为脚本生成的只读展示版，禁止手工编辑或双份维护。",
        "> 生成命令：`python3 scripts/validate.py --generate-md`",
        "> 迁移记录：TECH-11（2026-10-12）自原 Markdown 无损迁移；原文件完整备份路径与 hash 见 `config/sources.json` → `migrated_from`。",
        "",
        "「每日科技情报扫描」Autopilot 的唯一来源依据为权威 JSON 文件。采集窗口默认 48 小时，每日筛选 Top 10，一手性优先，不足则少留、不凑数（见 `config/project.json`）；执行规则见 [`rules/collection.md`](rules/collection.md)。",
        "",
    ]
    sources = src["sources"]
    for tier in TIERS:
        tier_src = [s for s in sources if s.get("tier") == tier]
        if not tier_src:
            continue
        meta = src["tiers"][tier]
        lines.append(f"## {tier} · {meta['name']}（{meta['purpose']}）")
        lines.append("")
        groups = []
        for s in tier_src:
            g = s.get("group")
            if g and g not in groups:
                groups.append(g)
        for g in groups or [None]:
            if g:
                lines.append(f"### {g}")
                lines.append("")
            lines.append("| 名称 | 地址 |")
            lines.append("|---|---|")
            for s in tier_src:
                if (g is None and s.get("group")) or (g and s.get("group") != g):
                    continue
                addr = s["url"] if s["url"] else "（清单未给出 URL）"
                if s.get("notes"):
                    addr += f" （{s['notes']}）"
                lines.append(f"| {s['name']} | {addr} |")
            lines.append("")
    cands = [s for s in sources if s.get("status") == "candidate"]
    if cands:
        lines.append("## 候选待观察（暂不纳入）")
        lines.append("")
        for s in cands:
            head = f"- {s['name']}"
            if s["url"]:
                head += f" {s['url']}"
            if s.get("notes"):
                head += f" —— {s['notes']}"
            lines.append(head)
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"来源配置版本：v{src.get('version', 1)}（updated_at {src.get('updated_at', '未知')}）；"
        "本文件为生成产物，内容以 `config/sources.json` 为准。"
    )
    lines.append("")
    return "\n".join(lines)


# ---------- 迁移交叉核验 ----------

def parse_old_markdown(text: str):
    """解析旧版科技情报来源清单.md，返回 [(tier, group, name, url), ...] 与候选 [(name, url)]。"""
    entries, candidates = [], []
    tier = group = None
    for raw in text.splitlines():
        line = raw.strip()
        m = re.match(r"^## (T[123]) ·", line)
        if m:
            tier, group = m.group(1), None
            continue
        if line.startswith("## "):
            tier = "CAND" if line.startswith("## 候选待观察") else None
            if tier is None:
                break  # 进入使用规则等后续章节，候选解析结束
            continue
        m = re.match(r"^### (.+)$", line)
        if m and tier == "T1":
            group = m.group(1).strip()
            continue
        if tier in TIERS and line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) == 2 and cells[0] not in ("名称", ":---", "---", "---:"):
                urls = URL_RE.findall(cells[1])
                if urls:
                    entries.append((tier, group, cells[0], urls[0]))
        elif tier == "CAND" and raw.startswith("- "):  # 仅顶格条目，rule 4 缩进子弹不算
            head = line[2:].split(" —— ")[0]
            urls = URL_RE.findall(head)
            names = [n.strip() for n in URL_RE.sub("", head).split("、") if n.strip()]
            for i, name in enumerate(names):
                candidates.append((name, urls[i] if i < len(urls) else None))
    return entries, candidates


def verify_migration(md_path: Path, src: dict, errors):
    entries, candidates = parse_old_markdown(md_path.read_text(encoding="utf-8"))
    enabled = [s for s in src["sources"] if s["status"] == "enabled"]
    cands = [s for s in src["sources"] if s["status"] == "candidate"]

    md_set = {(t, g, n, u) for t, g, n, u in entries}
    js_set = {(s["tier"], s.get("group"), s["name"], s["url"]) for s in enabled}
    for item in sorted(md_set - js_set):
        fail(errors, f"迁移缺失: Markdown 有而 sources.json 无 → {item}")
    for item in sorted(js_set - md_set):
        fail(errors, f"迁移多余: sources.json 有而 Markdown 无 → {item}")

    md_c = sorted(candidates)
    js_c = sorted((s["name"], s["url"]) for s in cands)
    if md_c != js_c:
        fail(errors, f"候选映射不一致: markdown={md_c} json={js_c}")

    if len(enabled) != len(entries):
        fail(errors, f"启用来源数量不一致: markdown={len(entries)} json={len(enabled)}")
    if not errors or all("数量不一致" not in e for e in errors):
        print(f"迁移交叉核验: 启用 {len(entries)}/{len(enabled)}，候选 {len(candidates)}/{len(cands)}")


# ---------- 常规校验 ----------

def validate(project, src, errors):
    # project.json
    if project:
        if project.get("version") != 1:
            fail(errors, "project.json: version 必须为 1")
        for key, rel in (project.get("authority") or {}).items():
            if not (ROOT / rel).exists():
                fail(errors, f"project.json: authority.{key} 指向不存在的 {rel}")
        for key in ("window_hours", "top_n", "timezone"):
            if key not in (project.get("collection") or {}):
                fail(errors, f"project.json: collection.{key} 缺失")

    # sources.json
    ids = set()
    if src:
        if src.get("version") != 1:
            fail(errors, "sources.json: version 必须为 1")
        for t in TIERS:
            if t not in (src.get("tiers") or {}):
                fail(errors, f"sources.json: tiers.{t} 缺失")
        for s in src.get("sources") or []:
            sid = s.get("id", "<无id>")
            where = f"sources[{sid}]"
            if not ID_RE.match(s.get("id", "")):
                fail(errors, f"{where}: id 不合法")
            if sid in ids:
                fail(errors, f"{where}: id 重复")
            ids.add(sid)
            if not s.get("name"):
                fail(errors, f"{where}: name 缺失")
            status = s.get("status")
            if status not in ("enabled", "candidate"):
                fail(errors, f"{where}: status 非法 {status!r}")
            url = s.get("url")
            if url is not None and not url.startswith(("http://", "https://")):
                fail(errors, f"{where}: URL 非法 {url!r}")
            if status == "enabled":
                if s.get("tier") not in TIERS:
                    fail(errors, f"{where}: 启用来源 tier 非法 {s.get('tier')!r}")
                if not url:
                    fail(errors, f"{where}: 启用来源缺少 URL")
            elif status == "candidate" and s.get("tier") is not None:
                fail(errors, f"{where}: 候选来源 tier 应为 null")

    # state 契约
    pu = load_json(ROOT / "state/processed-urls.json", errors)
    if pu:
        required = {
            "published": ("url", "title", "issue", "published_on", "status", "role", "event"),
            "excluded": ("url", "title", "issue", "status", "reason", "evaluated_on"),
        }
        seen = set()
        for i, e in enumerate(pu.get("entries") or []):
            status = e.get("status")
            if status not in required:
                fail(errors, f"processed-urls[{i}]: status 非法 {status!r}")
            else:
                for k in required[status]:
                    if k not in e:
                        fail(errors, f"processed-urls[{i}]: {status} 条目缺字段 {k}")
            if e.get("url") in seen:
                fail(errors, f"processed-urls[{i}]: URL 重复 {e.get('url')}")
            seen.add(e.get("url"))

    sh = load_json(ROOT / "state/source-health.json", errors)
    if sh and src:
        unknown = set(sh.get("sources") or {}) - ids
        if unknown:
            fail(errors, f"source-health: 存在 sources.json 未定义的 id: {sorted(unknown)}")

    dr = load_json(ROOT / "state/daily-runs.json", errors)
    if dr:
        dates = set()
        for r in dr.get("runs") or []:
            for k in ("date", "issue", "status", "briefing_file"):
                if k not in r:
                    fail(errors, f"daily-runs: 缺字段 {k}")
            if r.get("date") in dates:
                fail(errors, f"daily-runs: 同日多条成功记录 {r.get('date')}")
            dates.add(r.get("date"))
            bf = r.get("briefing_file")
            if bf and not (ROOT / bf).exists():
                fail(errors, f"daily-runs: briefing_file 不存在 {bf}")

    # 展示一致性
    if src and DISPLAY_MD.exists():
        if generate_display(src) != DISPLAY_MD.read_text(encoding="utf-8"):
            fail(errors, "展示版不一致: 科技情报来源清单.md 与 config/sources.json 生成结果不同，运行 --generate-md 更新")
    elif src:
        fail(errors, "展示版缺失: 科技情报来源清单.md 不存在")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--generate-md", action="store_true", help="重新生成只读展示版")
    ap.add_argument("--migrated-from", type=Path, help="旧版 Markdown 路径，做无损迁移交叉核验")
    args = ap.parse_args()

    errors = []
    src = load_json(ROOT / "config/sources.json", errors)
    project = load_json(ROOT / "config/project.json", errors)

    if args.generate_md and src:
        DISPLAY_MD.write_text(generate_display(src), encoding="utf-8")
        print(f"已生成 {DISPLAY_MD.name}")
    if args.migrated_from and src:
        verify_migration(args.migrated_from, src, errors)
    if not args.generate_md:
        validate(project, src, errors)

    if errors:
        print(f"校验失败，{len(errors)} 个问题:")
        for e in errors:
            print(f"  - {e}")
        return 1
    if not args.generate_md:
        print("校验通过: 配置、来源标识、字段、启用状态、URL 与持久数据契约均符合 data-contract。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
