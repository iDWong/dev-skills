# Changelog

## Unreleased

### 落盘根收敛：研发链 `dev/`、产品链 `prd/`

- 研发链 13 阶段产出统一落 **`dev/`**：`SRS/`（规格真源）、`design/`（功能清单 · 概要/详细设计 · 错误码表）、
  `plan/`（交付计划）、`test/`（用例 · 测试报告 · 缺陷闭环）、`reports/`（上线审计 · 12 角色评审）、
  `release/`（操作手册 · 发版说明），进度存档 `dev/dev-master-{项目名}.md`。
- 产品链（姊妹库 [`pm-skills`](https://github.com/iDWong/pm-skills)）落 **`prd/`**，本库只读它的 PRD。
- **`docs/**` 整棵树降级为只读兼容**，不再往里写。读取端一律保留旧根兼容行，
  存量项目的老文档**原地续用不搬家**（搬家会断图片相对路径与交叉引用），只在进度存档里记真实路径。
- `workflow-catalog.yaml` 新增 `meta.doc_root` / `meta.doc_layout`；九处 `artifact.glob` 改成 `dev/` 在前、`docs/` 兜底。
- `scripts/skill-specs` 的三条静态断言同步改到新根。

### 文档署名

- 文档模板的编制人/作者/客户单位统一为 `Wong`，编制单位 `Wong's Development Team`；
  技能 frontmatter 的 `author` 由 `iDWong` 改为 `Wong`（上游 claudekit 的第三方署名不动）。

## v1.0.0 — 2026-09-11

首个发布版本。23 个技能 / 4 个 plugin / 13 阶段单一流程。

### 架构

- **单一编排器**：`dev-master` 是唯一入口，管 13 阶段流程（0 项目初始化 → 12 文档与发版）。
  与产品侧的 [`pm-skills`](https://github.com/iDWong/pm-skills) 对接：它的阶段 5 产出需求文档，本库**阶段 1** 接手转成 SRS 真源。
- **阶段定义机器可读**：`dev-core/skills/dev-master/workflow-catalog.yaml` 写明每阶段的技能（默认/深度档）、
  细则文件、产出判定 glob、门禁条目、跳过条件、裁剪区间。SKILL.md 的阶段表是它的人读摘要，
  **不一致以 YAML 为准**，自检会校验两者对得上。
- **裁剪而非多流程**：「三端全栈 0-1」「只要文档链」「上线体检」等 8 种裁剪是同一条流程的阶段区间，
  编号永不改变；跳过的阶段标注「已跳过（理由）」，断点续跑靠它判断。
- **阶段 7 双档**：`page-generator`（在已有项目加页面）／ `dev-fullstack-product`（三端 0-1 全栈，
  自带技术栈确认、三轮真跑测试、12 角色专家评审）。走深度档时阶段 9–11 退化为**校验它的产出**，不重复跑。
- **SRS 真源门禁贯穿全程**：阶段 2–8 的技能不得以 PRD 为规格真源，规则在 `common/prd-to-srs-gate.md`，
  按**内容角色**校验（功能清单／页面清单／字段级详细设计），不死认章节号。
- **渐进披露**：11 个技能拆了 `references/`，进哪个阶段读哪一份，不一次性灌进上下文。

### 自检

`scripts/validate-plugins.py` 零外部依赖，CI 每次 push 跑：

| 检查 | 抓什么 |
| --- | --- |
| 清单一致性 | marketplace 与 plugin.json、技能 frontmatter、技能名重复 |
| 引用可解析 | 跨技能引用、references 自引用 |
| **硬依赖** | 文件级引用（`<技能>/references/…`）必须能在本仓解析；姊妹库软指针降级为警告 |
| **绝对路径** | 公开仓不得出现任何 `/Users/xxx`、`/home/xxx` |
| **阶段目录** | catalog 与 `dev-master/SKILL.md` 的阶段表逐行对齐 |
| **裁剪名** | catalog / SKILL.md / tailoring.md 三处命名一致 |
| **编排器覆盖** | 库里每个技能都必须出现在 `dev-master/SKILL.md` |
| **行为规格** | `scripts/skill-specs/` 里的 `[static]` 断言（当前 29 条） |
| 图片路径 | md 里的图片引用不得带 `docs/` 前缀（会让 Word 导出丢图） |

### 已知约束（使用前值得知道）

- **四个 bundle 是一套**。`dev-master` 编排的技能分布在全部四个 bundle 里，只装 `dev-core`
  流程从阶段 1 就断。单装各 bundle 的实际可用范围见 README。
- **图表渲染与 Word/xlsx 导出需要自配端点**（技能根的 `config.json`，从 `config.example.json` 复制）。
  没配不阻断流程：图改 mermaid 代码块内嵌、Word 改交付 md，降级路径写在 `dev-master` 的铁律里。
- **7 处软指针指向姊妹库文档**（如「细则见 `pm-master/references/stages/s5-spec.md`」），
  自检以警告列出，只装本库时忽略即可——本库不读 `pm-skills` 的任何文件。
- **14 个技能与 `pm-skills` 重叠**，是同一份技能的两处分发、逐字一致，不是两个版本。
- **`[behavior]` 断言尚未逐条实跑验证**。`scripts/skill-specs/` 里的 31 条行为断言需要拿真实项目
  从阶段 0 跑到 12 才验得了；当前保证的是文档契约对得上，不是跑过了。
