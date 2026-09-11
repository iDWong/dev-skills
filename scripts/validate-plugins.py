#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dev-skills 仓库自检：marketplace / plugin.json / 技能 frontmatter / 跨技能引用 / 图片路径规则。

用法：python3 scripts/validate-plugins.py
零外部依赖。发现问题以非零码退出，可直接接进 CI。
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
errs, warns = [], []


def err(m): errs.append(m)
def warn(m): warns.append(m)


def main() -> int:
    mk_path = ROOT / ".claude-plugin" / "marketplace.json"
    if not mk_path.is_file():
        err("缺 .claude-plugin/marketplace.json"); return report()
    mk = json.loads(mk_path.read_text(encoding="utf-8"))

    declared = {p["name"] for p in mk.get("plugins", [])}
    on_disk = {d.name for d in ROOT.glob("dev-*") if (d / ".claude-plugin" / "plugin.json").is_file()}
    for miss in declared - on_disk:
        err(f"marketplace 声明了 {miss}，但磁盘上没有对应目录")
    for extra in on_disk - declared:
        err(f"磁盘上有 {extra}，但 marketplace 没声明")

    skills = {}
    for pj in sorted(ROOT.glob("dev-*/.claude-plugin/plugin.json")):
        plug = pj.parent.parent
        meta = json.loads(pj.read_text(encoding="utf-8"))
        for key in ("name", "description", "version", "license"):
            if not meta.get(key):
                err(f"{plug.name}/plugin.json 缺 {key}")
        if meta.get("name") != plug.name:
            err(f"{plug.name}/plugin.json 的 name={meta.get('name')} 与目录名不一致")
        sk_dir = plug / "skills"
        if not sk_dir.is_dir():
            err(f"{plug.name} 缺 skills/ 目录"); continue
        for sk in sorted(sk_dir.iterdir()):
            if not sk.is_dir() or sk.name == "common":
                continue
            f = sk / "SKILL.md"
            if not f.is_file():
                err(f"{plug.name}/skills/{sk.name} 缺 SKILL.md"); continue
            t = f.read_text(encoding="utf-8", errors="ignore")
            m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
            if not m:
                err(f"{sk.name}: frontmatter 结构异常"); continue
            fm = m.group(1)
            nm = re.search(r"^name: *(\S+)", fm, re.M)
            if not nm:
                err(f"{sk.name}: frontmatter 缺 name")
            elif nm.group(1).strip('"') != sk.name:
                err(f"{sk.name}: frontmatter name={nm.group(1)} 与目录名不一致")
            if "description:" not in fm:
                err(f"{sk.name}: frontmatter 缺 description")
            elif not re.search(r"[一-鿿]", fm):
                warn(f"{sk.name}: description 不含中文（本库约定中文说明）")
            if sk.name in skills:
                err(f"技能 {sk.name} 在 {skills[sk.name]} 和 {plug.name} 里重复")
            skills[sk.name] = plug.name

    # 跨技能引用可解析（排除子 Agent 名、风格名、参数值等已知假阳性）
    # 姊妹库 pm-skills 里的技能：本库不打包，引用处已注明「pm-skills 库」，装了就能用，没装也不影响本库流程
    external = {"pm-roadmap-planner", "pm-tracking-spec-writer", "pm-postmortem-writer",
                "feasibility-report", "ui-frosted-gradient-clear-sleeve", "pm-prd-spec",
                "pm-prd-writer", "prd-writer", "prototype-to-prd", "pm-master", "pm-review-board"}
    fp = external | {"delivery-plan-", "feature-priority-",
          "req-analyzer", "req-writer", "page-reviewer", "page-spec-loader", "design-analyzer",
          "design-reviewer", "design-writer", "diagram-drawer", "ui-wireframe", "required-indicators",
          "srs-writer", "feature-dev", "pm-skills", "pm-advisory-suite", "dev-skills",
          "pm-master", "pm-prd-spec", "pm-prd-writer", "prd-writer", "prototype-to-prd",
          "dve-master", "test-driven", "project-path", "dev-fullstack"}
    pat = re.compile(r"`((?:pm|ui|req|prd|page|feature|feasibility|delivery|annotation|"
                     r"brainstorming|hld|lld|prototype|diagram|dev|test|systematic|webapp|"
                     r"verification|finishing|project|start)-[a-z0-9-]+)`")
    for sk_name, plug in skills.items():
        base = ROOT / plug / "skills" / sk_name
        txt = "".join(f.read_text(encoding="utf-8", errors="ignore") for f in base.rglob("*.md"))
        for ref in sorted(set(pat.findall(txt))):
            if ref in fp or ref in skills:
                continue
            err(f"{sk_name} 引用了不存在的技能 `{ref}`")

    # references/ 自引用可解析
    for sk_name, plug in skills.items():
        base = ROOT / plug / "skills" / sk_name
        for f in base.rglob("*.md"):
            for ref in set(re.findall(r"`(references/[A-Za-z0-9_./-]+\.md)`", f.read_text(encoding="utf-8", errors="ignore"))):
                if not (base / ref).exists():
                    warn(f"{sk_name} :: {f.name} → {ref} 不存在")

    # 图片路径规则：md 里不该出现带 docs/ 前缀的图片引用
    for f in ROOT.rglob("dev-*/skills/**/*.md"):
        for bad in re.findall(r"!\[[^\]]*\]\((docs/[^)]+)\)", f.read_text(encoding="utf-8", errors="ignore")):
            err(f"{f.relative_to(ROOT)} 的图片引用带 docs/ 前缀：{bad}（Word 导出会丢图）")

    n_stages = check_catalog(skills)
    n_spec = check_specs(skills)

    print(f"检查 {len(declared)} 个 plugin / {len(skills)} 个技能 / {n_stages} 个阶段 / {n_spec} 条静态断言")
    return report()



# ---------- workflow-catalog.yaml：阶段目录 ----------

def parse_catalog(text):
    """只解析本仓库自己写出的 YAML 子集（零外部依赖，不做通用 YAML 解析）。"""
    stages, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^  - id: (\d+)\s*$", line)
        if m:
            cur = {"id": int(m.group(1))}
            stages.append(cur)
            continue
        if cur is None or not line.startswith("    "):
            continue
        m = re.match(r"^    (\w+): (.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if k == "skill":
            cur["skill"] = dict(
                re.findall(r"(default|deep): ([A-Za-z0-9_-]+)", v))
        elif k in ("key", "label", "detail", "required"):
            cur[k] = v
        elif k == "also":
            cur["also"] = re.findall(r"[A-Za-z0-9_-]+", v)
    return stages


def check_catalog(skills):
    base = ROOT / "dev-core" / "skills" / "dev-master"
    cat = base / "workflow-catalog.yaml"
    if not cat.is_file():
        err("dev-master 缺 workflow-catalog.yaml（阶段的权威定义）")
        return 0
    text = cat.read_text(encoding="utf-8")
    stages = parse_catalog(text)
    declared = re.search(r"^  stages: (\d+)$", text, re.M)
    if declared and int(declared.group(1)) != len(stages):
        err(f"catalog meta.stages={declared.group(1)}，实际解析出 {len(stages)} 个阶段")
    ids = [s["id"] for s in stages]
    if ids != list(range(len(ids))):
        err(f"catalog 阶段号不连续或未从 0 开始：{ids}")

    skill_md = (base / "SKILL.md").read_text(encoding="utf-8")
    for st in stages:
        sid = st["id"]
        for role, name in (st.get("skill") or {}).items():
            if name not in skills:
                err(f"catalog 阶段 {sid} 的 {role} 技能 `{name}` 不在本仓库")
            elif f"`{name}`" not in skill_md:
                err(f"catalog 阶段 {sid} 的技能 `{name}` 没出现在 dev-master/SKILL.md 的阶段表里")
        for name in st.get("also", []):
            if name not in skills:
                err(f"catalog 阶段 {sid} 的 also 技能 `{name}` 不在本仓库")
        d = st.get("detail")
        if not d:
            err(f"catalog 阶段 {sid} 缺 detail（阶段细则文件）")
        elif not (base / d).is_file():
            err(f"catalog 阶段 {sid} 的 detail 文件不存在：{d}")
        if not re.search(rf"^\| {sid} \|", skill_md, re.M):
            err(f"catalog 有阶段 {sid}，但 dev-master/SKILL.md 的阶段表里没有这一行")
        if "required" not in st:
            warn(f"catalog 阶段 {sid} 没写 required")
    for f in sorted((base / "references" / "stages").glob("s*.md")):
        sid = int(re.match(r"s(\d+)", f.name).group(1))
        if sid not in ids:
            err(f"有阶段细则 {f.name}，但 catalog 里没有阶段 {sid}")
    return len(stages)


# ---------- scripts/skill-specs：行为规格里的静态断言 ----------

def check_specs(skills):
    spec_dir = ROOT / "scripts" / "skill-specs"
    if not spec_dir.is_dir():
        return 0
    total = 0
    for spec in sorted(spec_dir.glob("*.md")):
        if spec.stem == "README":
            continue
        name = spec.stem
        if name not in skills:
            err(f"规格 {spec.name} 指向的技能 `{name}` 不在本仓库（技能改名了？）")
            continue
        base = ROOT / skills[name] / "skills" / name
        blob = "".join(f.read_text(encoding="utf-8", errors="ignore")
                       for f in sorted(base.rglob("*.md")))
        fm = re.match(r"^---\n(.*?)\n---\n", (base / "SKILL.md").read_text(encoding="utf-8"), re.S)
        fm = fm.group(1) if fm else ""
        text = spec.read_text(encoding="utf-8")
        found = re.findall(r"^- \[static\] (\w[\w-]*): (.+)$", text, re.M)
        if not found:
            warn(f"规格 {spec.name} 没有任何 [static] 断言")
        for directive, arg in found:
            total += 1
            arg = arg.strip()
            if directive == "contains":
                if not re.search(arg, blob):
                    err(f"[{name}] 静态断言失败 contains: {arg}")
            elif directive == "not-contains":
                if re.search(arg, blob):
                    err(f"[{name}] 静态断言失败 not-contains: {arg}")
            elif directive == "frontmatter-has":
                if not re.search(rf"^{re.escape(arg)}:", fm, re.M):
                    err(f"[{name}] frontmatter 缺 {arg}")
            elif directive == "file-exists":
                if not (base / arg).exists():
                    err(f"[{name}] 规格要求的文件不存在：{arg}")
            else:
                err(f"规格 {spec.name} 用了未知指令 [static] {directive}")
    return total


def report() -> int:
    for w in warns:
        print(f"  ⚠️  {w}")
    for e in errs:
        print(f"  ✗ {e}")
    if not errs:
        print(f"  ✓ 通过{f'（{len(warns)} 个警告）' if warns else ''}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
