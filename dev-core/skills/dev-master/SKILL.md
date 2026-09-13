---
name: dev-master
description: |
  研发全生命周期单一流程（13 阶段）。管理 26 个研发链技能：规格真源 → 功能清单 → 概要设计（含威胁建模）→ 详细设计
  → 交付规划 → 界面设计 → 编码实现 → 原型标注 → 测试 → 调试验收 → 上线审计 → 文档发版 → 分支收尾。
  能力：(1) 单点需求直接路由到最合适的技能 (2) 多步需求按同一条流程裁剪出阶段区间并编排
  (3) 保证上一步产出是下一步的合法输入（SRS 真源门禁贯穿全程）(4) 支持默认/深度档换挡、断点续跑。
  触发词：「dev-master」「研发总控」「开发总控」「技术总控」「我该用哪个开发技能」「帮我把这个需求做出来」
  「从需求到上线」「完整开发流程」「走完整研发流程」「一键开发」「从0到1开发」「整套系统开发」
  「三端开发」「全栈开发」，或者用户描述了一个研发场景但没指明用哪个技能、或任务明显需要多个研发技能接力时。
  别名：dve-master（笔误也能命中本技能）。
  不适用：产品侧的战略/调研/画像/优先级/PRD（那条链走 `pm-master`）。
metadata:
  author: Wong
  version: "1.7"
  reviewed: "2026-09-14"
---

# dev-master：研发全生命周期总控

> 定位：**研发侧的入口 + 唯一流程**。你不亲自产出内容，你的工作是：判断这是单点还是多步 →
> 单点直接路由，多步按同一条流程裁剪出阶段区间 → 保证上一步产出是下一步的合法输入。
>
> **库里只有一条流程。** 所谓「快速开发」「只补文档」「上线体检」都是同一条流程的裁剪，**阶段编号永不改变**。

## 与 pm-master 的边界

| | `pm-master` | `dev-master`（本技能） |
|---|---|---|
| 管什么 | 产品侧：战略 → 调研 → 画像 → 优先级 → 路线图 → PRD | 研发侧：SRS → 设计 → 实现 → 测试 → 上线 |
| 交接点 | 它的阶段 5 产出需求文档 | 本流程的**阶段 1** 接手，把 PRD 转写成 SRS 真源 |
| 重叠技能 | `req-doc` / `page-generator` / `pm-test-cases` 等在两条链上都出现 | **同一份技能，不是两份**；谁在跑就由谁编排，不要两个总控同时起流程 |

用户从 `pm-master` 一路跑到需求文档后说「开始开发」→ 交给本技能，从阶段 1 的门禁检查接手。

## 分诊（三类，先判这个）

| 类型 | 特征 | 怎么办 |
|---|---|---|
| **单点类** | 要的是一份可交付物，且只要这一份（「写个详细设计」「生成测试用例」） | 按下方路由表选 1 个技能，**不要起流程** |
| **流程类** | 横跨多步、说了「从需求到上线 / 完整开发 / 三端全做 / 从 0 到 1」 | 起流程：定裁剪 → 建任务清单 → 逐阶段执行 |
| **排障类** | 现成代码出了问题、要定位（「这个 bug 怎么回事」「为什么跑不起来」） | 直接 `systematic-debugging`，**不要起流程** |

判不清单点还是流程：**问一句「只要这一份，还是要往后接着做？」** 不要自己假设。

## 一条流程，13 个阶段

**阶段的权威定义在 `workflow-catalog.yaml`**（机器可读：每阶段的技能、细则文件、产出 glob、门禁条目、跳过条件、裁剪区间）。
下表是它的人读摘要，**两者不一致时以 YAML 为准**；改阶段必须改 YAML，只改表会被自检拦下。

**档位在入口就问定**（见 `references/flow-engine.md` Step 0），不是等用户嫌浅了再换。

| # | 阶段 | 默认档 | 深度档 | 产出 |
|---|---|---|---|---|
| 0 | 项目初始化 | `project-init`（CI/钩子/定时任务配 `workflow-automator`） | — | 仓库骨架 + `README-DEV.md` + CI 配置 |
| 1 | **规格真源** | `req-doc`（SRS） | — | `dev/SRS/*.md` ← **不可跳过**，登记 `SPEC_SOURCE` |
| 2 | 功能清单 | `feature-list` | — | `dev/design/*功能清单*.md`/`.xlsx` |
| 3 | 概要设计 | `hld-design`（安全侧配 `threat-model`） | — | `dev/design/*概要设计*.md` + `dev/design/威胁模型-*.md` |
| 4 | 详细设计 | `lld-design` | — | `dev/design/*详细设计*.md`（表结构 + 接口 + 模块） |
| 5 | 交付规划 | `delivery-plan` | — | `dev/plan/delivery-plan-*.md` |
| 6 | 界面与设计稿 | `ui-ux-pro-max`（设计系统 + 材质层 + 多端规则，一个技能全包） | — | `design-system/<项目slug>/` |
| 7 | **编码实现** | `page-generator`（页面级／单端） | `dev-fullstack-product`（三端全栈 0-1，带三轮测试与 12 角色评审） | `dev/code/` |
| 8 | 原型标注 | `annotation` | — | 页面内标注层 |
| 9 | 测试 | `pm-test-cases`（用例）+ `webapp-testing`（真跑） | `test-driven-development`（先写测试驱动实现） | `dev/test/*测试用例*.md` + 测试报告 |
| 10 | 调试与验收 | `dev-code-review`（评审）+ `verification-before-completion`（终检） | `systematic-debugging`（有具体故障时） | `dev/reports/代码评审-*.md` + 缺陷闭环记录 |
| 11 | 上线审计 | `pm-ai-ship-audit` | — | `dev/reports/` |
| 12 | 文档与发版 | `pm-operation-manual` + `pm-release-notes` + `release-rollout` + `finishing-branch` | — | `dev/release/` 手册 / 发版说明 / **发布与回滚预案** + 分支收尾 |

> **产出路径一律按 glob 匹配**：各技能的实际命名带项目名／日期／版本号，写死精确文件名门禁永远过不了。
> 落盘根一律是 `dev/`，见下方「落盘目录」一节；`docs/` 只做只读兼容。

> **阶段 7 的档位有硬区别**：`page-generator` 是「在已有项目里加页面」，`dev-fullstack-product` 是
> 「移动端 + 管理端 + 后端三端 0-1 全栈交付」，后者**自带阶段 9/10/11 的等价环节**（三轮真跑测试 +
> 12 角色专家评审）。选了深度档时，阶段 9–11 改为**校验它的产出是否达标**，不要重复跑一遍。

**阶段 1 对阶段 2–8 是硬前置**——它们全部依赖 `SPEC_SOURCE`，有这几个阶段就必须先过阶段 1。
裁剪区间**完全不含 2–8** 时（「上线体检」只跑 11、「单页面/小改」7,9,10、「热修复」）才可以不跑阶段 1，
且要在进度存档里标明「本次裁剪不依赖 SPEC_SOURCE」。其余阶段的跳过判据见 `references/tailoring.md`。

**读这几个文件再动手（不要凭记忆跑流程）：**
- `workflow-catalog.yaml` — 阶段、产出 glob、门禁、裁剪的**权威定义**；起流程时先读它
- `references/flow-engine.md` — Step 0 初始化四问、任务清单规范、阶段间传递门禁、并行规则、确认节点、进度汇报格式、目录规范、断点续跑
- `references/tailoring.md` — 裁剪表与逐阶段跳过判据、默认档／深度档换挡规则
- `references/stages/s<N>-*.md` — 每个阶段的执行细则，**进入该阶段时只读那一个**，不要一次全读
- `references/delivery-review.md` — **开发交付闭环验收检查机制**（五阶段：设计稿 1:1 还原 → 三端页面覆盖
  → 接口连通 → 数据落库 → 测试闭环，外加五方对齐、问题分级与证据留存、准入准出与禁止上线清单）。
  **阶段 9–11 的判据以它为准**；与 `dev-fullstack-product` 下的同名文件是**同一份**，改一处必须同步另一处

## 落盘目录：研发链产出一律进 `dev/`

**唯一落盘根是 `dev/`**（记作 `DEV_DOC_ROOT`）。13 个阶段的文档产出全部落这儿，与产品侧的 `prd/` 彻底分开——
`prd/` 由 `pm-master` 那条链写（战略/调研/画像/优先级/路线图/PRD/可研），本流程**只读**；
`docs/**` 是旧根，也**只读兼容**（存量项目的老文档）。

```
dev/
├─ SRS/                     阶段 1   规格真源（SPEC_SOURCE 指这儿）
├─ design/                  阶段 2/3/4  功能清单 · 概要设计 · 详细设计 · error-codes.md · 数据字典
├─ plan/                    阶段 5   delivery-plan-{项目名}.md
├─ test/                    阶段 9/10  测试用例 · 测试报告 · 缺陷清单与闭环记录
├─ reports/                 阶段 11  上线审计报告（阶段 7 深度档的 12 角色评审报告也落这儿）
├─ release/                 阶段 12  操作手册 · 发版说明
├─ code/                    阶段 7   **应用代码**：各端子项目（`admin/ mobile/ h5-app/ server/ backend/ web/ shared/`）；
│                                    单端项目直接是 `dev/code/src/`
└─ dev-master-{项目名}.md    流程进度存档
```

**`dev/code/` 只放应用代码**：仓库级基建（`docker-compose*.yml`、`Caddyfile`、CI 配置、`hooks/`、
`scripts/`、部署文档）留在**仓库根**；子项目自己的 `README-DEV.md`、`.env.example`、lint 配置、
`migrations/` 跟着子项目走，即在 `dev/code/<子项目>/` 下。

四条规则：

1. **写一律 `dev/`，读 `dev/` 优先，再看 `prd/`（上游产品文档）、`docs/**` 兜底（存量项目）。**
   `req-doc` / `feature-list` / `hld-design` / `lld-design` / `delivery-plan` 的默认落点已经是 `dev/` 下对应目录，
   直接调即可；`pm-test-cases` / `pm-operation-manual` / `pm-release-notes` / `pm-ai-ship-audit` 两条链共用
   （产品链落 `prd/`），**在本流程里要显式指到 `dev/test|release|reports/`**。写完再搬会断图片相对路径与交叉引用。
2. **图片放各文档同级 `images/`**（如 `dev/design/images/`），不要集中到一个目录，跨目录引用在 Word 导出时会丢图。
3. **老项目命中 `docs/` 里的历史产出：原地续用，不主动搬家**，在进度存档里登记真实路径即可。
   用户明确要求迁移才迁；迁移时同级 `images/` 一起搬，并回改 md 里的相对引用与全部交叉链接。
4. `prd/`（旧项目 `docs/PRD/`）是上游产物**只读不写**；`design-system/`（设计稿与设计令牌同树）、
   `tools/`（生图与一次性脚本）不在 `dev/` 下，保持各自约定。存量项目的代码在仓库根（`src/`、
   `admin/`、`server/` …）时**原地续用不搬家**，除非用户要求迁到 `dev/code/`。

## 常用裁剪（细则见 tailoring.md）

| 裁剪 | 阶段区间 | 什么时候用 |
|---|---|---|
| 全量（从 0 到 1） | 0 → 12 | 新项目，代码还没有 |
| 三端全栈 0-1 | 0,1,2,3,4,5,6,**7深度档**,9,10,11,12 | 移动端 + 管理端 + 后端一起做 |
| 有 SRS 直接开工 | 5 → 12 | 文档齐了，只要实现 |
| 只要文档链 | 1,2,3,4 | 交付设计文档，不写代码 |
| 迭代（老项目加功能） | 1,5,7,9,10,12 | 已有代码库，加一批功能 |
| 单页面 / 小改 | 7,9,10 | 加一两个页面 |
| 上线体检 | 11 | 代码已经写完（尤其 AI 写的），只要审计 |
| 热修复（线上出事） | 10 → 7 → 9 → 12 | 线上有故障。入口是阶段 10 的 `systematic-debugging` 先定位，改完只回归受影响范围 |
| 反向补文档 | 1,3,4（各技能的反向同步模式） | 代码先行，文档缺失 |

## 单点路由表

用户只要一份产出时用这张表，**不要起流程**。

| 用户在说什么 | 路由到 | 备注 |
|---|---|---|
| 要 SRS / 需求规格说明书 / PRD 转 SRS | `req-doc` | 研发侧唯一规格真源 |
| 功能清单 / 功能列表 | `feature-list` | 从 SRS+可研提取 |
| 概要设计 / 系统架构 / 分层与模块划分 | `hld-design` | |
| 详细设计 / 表结构 / 接口设计 / 类图 | `lld-design` | 三合一，不要拆成三份文档 |
| 威胁建模 / 安全设计评审 / STRIDE / 攻击面 / 越权设计 | `threat-model` | 阶段 3 之后、阶段 4 之前做；写完代码再查是 `pm-ai-ship-audit` |
| 交付计划 / 开发顺序 / 下一步做什么 | `delivery-plan` | 也管进度追踪与自动连跑 |
| 设计稿 / 高保真原型 / 可点原型 / 预览墙 | `ui-ux-pro-max` | 需 PRD+SRS 齐备 |
| 前端界面实现 / 组件 / 落地页要好看 | `frontend-design` | 只要设计建议不写码 → `ui-ux-pro-max` |
| 磨砂玻璃 / 深浅双主题 / 材质与层级 | `ui-ux-pro-max` | 材质层已并入该技能：规则见 `ui-ux-pro-max/references/design-system.md` 第四节，可内联实现在其 `assets/surface/` |
| 加一个页面 / 实现某个功能页 | `page-generator` | 在**已有项目**里加 |
| 整套系统做出来（三端 + 测试 + 评审） | `dev-fullstack-product` | 0-1 全栈 SOP |
| 原型标注 / 给页面加需求说明 | `annotation` | |
| 流程图 / 架构图 / 时序图 / ER 图 | `diagram-generator` | 文档里所有图一律走它，禁止手绘 |
| 测试用例 / 验收标准 | `pm-test-cases` | |
| 真的把 Web 应用跑起来点一遍 | `webapp-testing` | 要出正式用例文档 → `pm-test-cases` |
| 先写测试再写实现 | `test-driven-development` | |
| 这个 bug 怎么回事 / 为什么跑不起来 | `systematic-debugging` | |
| 代码评审 / 看看这个 PR / 合并前把关 | `dev-code-review` | 评「这次改动」；Claude Code 里要快评不留档用内置 `/code-review` |
| 做完了，帮我确认真的做完了 | `verification-before-completion` | |
| AI 写的代码能不能上线 / 安全性能审计 / 代码和文档对不上 | `pm-ai-ship-audit` | |
| 操作手册 / 用户指南 | `pm-operation-manual` | |
| 发版说明 / release notes | `pm-release-notes` | 面向用户的文案 |
| 发布方案 / 灰度 / 回滚预案 / 出事怎么退回去 | `release-rollout` | 面向自己人的操作手册，落 `dev/release/` |
| 分支做完了怎么收尾（合并/PR/丢弃） | `finishing-branch` | |
| 新项目脚手架 / 初始化 | `project-init` | |
| CI/CD 配置 / Git Hooks / 定时任务 / 自动化脚本 | `workflow-automator` | 阶段 0 落基建，阶段 12 补发布流水线 |
| 产品侧的事（战略/调研/画像/优先级/PRD） | `pm-master` | 不在本流程内 |

路由后说明选择理由（一句话），确认后加载执行。用户明显着急或指令明确时**直接执行，不要多问**。

## 贯穿全程的三条铁律

1. **SRS 真源门禁**：阶段 2–8 的技能**不得以 PRD 为规格真源**。只有 PRD 时走 `req-doc` **Step F** 转写。
   规则原文在 `../common/prd-to-srs-gate.md`，**进流程前读一遍**，不要凭记忆执行。
2. **图一律走 `diagram-generator`**：所有阶段产出的文档里的流程图/架构图/时序图/ER 图都由它生成，禁止手绘。
   改过文案的图**必须重渲**（`mermaid`/`drawio` 源与图片 mtime 对不上就是过期）。
3. **Word 导出放在最后**：导出读的是**启动那一刻的 md**，任何编辑之后都要重新导出，否则 docx 静默过期。
   导完必须验图：`unzip -l x.docx | grep -c 'word/media/'` 要等于图片张数。

### 没配端点时怎么办（新装的库默认没配，别卡在这儿）

图表渲染与 Word/xlsx 导出都要技能根的 `config.json`（`diagramApiUrl` / `apiBaseUrl`），
从 `config.example.json` 复制后自己填。**没配不阻断流程**，按下面降级并在产出里标一行：

| 能力 | 没配时 | 降级做法 |
|---|---|---|
| 图表渲染 | `render-diagram.*` 明确报错（不是静默失败） | 图改用 **mermaid 代码块内嵌 md**（Claude Code 与 GitHub 都能渲染），文档里标注「图为 mermaid 源码，未出 PNG」；drawio XML 仍可用 `validate-diagram.*` 本地校验 |
| Word / xlsx 导出 | `export-word.*` 报「无法读取 apiBaseUrl」 | 交付 md，阶段 12 的交付清单里注明「Word 未导出（未配端点）」 |

**降级不等于可以手绘 ASCII 流程图**——mermaid 源码仍是结构化的，手画的框线图不是。

## 工具层（不占阶段，按需调用）

| 技能 | 什么时候用 |
|---|---|
| `diagram-generator` | 任何阶段要出图 |
| `common/export-word.*` | 文档类阶段要交 Word（阶段 1/2/3/4/9/12） |

## 输出格式（每阶段固定）

```
【阶段 N：名称】
- 本阶段目标：
- 调用技能：（默认档/深度档）
- 已完成内容：
- 产出文件：（真实路径）
- 门禁检查：（下一阶段需要的输入是否齐备）
- 待用户确认事项：
- 下一步计划：
```
