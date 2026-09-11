<h1 align="center">Dev-Skills 1.0</h1>

<p align="center"><code>dev-skills</code></p>

<p align="center"><em>「一条流程，13 个阶段，从需求真源一路走到能不能上线」</em></p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/Skills-24-5aa524?style=for-the-badge">
  <img alt="Plugins" src="https://img.shields.io/badge/Plugins-4-c8a500?style=for-the-badge">
  <img alt="Stages" src="https://img.shields.io/badge/Lifecycle-13%20Stages-1888c8?style=for-the-badge">
  <img alt="Runtime" src="https://img.shields.io/badge/Runtime-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-7b2bd9?style=for-the-badge">
</p>

<p align="center"><strong>License MIT</strong></p>

---

## 项目归属

| 项 | 内容 |
| --- | --- |
| **项目** | `iDWong/dev-skills` **v1.0** |
| **作者** | Noah Wong |
| **规模** | **24 个技能**，打包成 **4 个 plugin**；**0 个 slash command**——靠 `description` 触发词自动路由（Claude Code 仍会把每个技能暴露为 `/<skill-name>`） |
| **语言** | 中文技能说明（每个 `description` 含触发词与「不适用」），产出语言跟随用户提问语言 |
| **实现** | 85 个 md（含 46 个 references）+ 1 份机器可读阶段目录 YAML + 41 个可执行脚本 + 37 张 CSV 数据表 + 26 个 json，共 272 个文件 / 6.3 MB |
| **入口** | 跟 Claude 说 **`dev-master`** 或「走完整研发流程」 |
| **安装** | plugin marketplace：`claude plugin marketplace add iDWong/dev-skills`；Codex / Cursor 用 `bash install.sh <目标>` |

> **和「纯 prompt 库」的区别**：本库带可执行组件——`ui-ux-pro-max` 的 37 张 CSV 是可检索的设计数据库
> （79 风格 / 192 配色 / 74 字体对 / 119 UX 规则 / 22 技术栈），`diagram-generator` 有 draw.io 渲染与校验脚本，
> `common/` 有 Word/xlsx 导出链，`pm-operation-manual` 有 Puppeteer 截图脚本。
> 这些是「产出可交付物」而不只是「给出建议」的前提。

---

## 一条流程，13 个阶段

```
[ 0] 项目初始化
[ 1] 规格真源 (SRS) ──── 不可跳过，登记 SPEC_SOURCE 供 2–8 读取
[ 2] 功能清单        ∥
[ 3] 概要设计        ∥ 可并行
[ 4] 详细设计 ───────── 表结构 + 接口 + 模块，返工成本最高的一份
[ 5] 交付规划
[ 6] 界面与设计稿
[ 7] 编码实现 ───────── 默认档 page-generator / 深度档 dev-fullstack-product
[ 8] 原型标注
[ 9] 测试 ──────────── 用例 + 真跑，只写真正执行过的结果
[10] 调试与验收
[11] 上线审计 ───────── AI 写的代码尤其要跑
[12] 文档与发版
```

**阶段的权威定义是机器可读的** —— [`dev-core/skills/dev-master/workflow-catalog.yaml`](dev-core/skills/dev-master/workflow-catalog.yaml)
写明每个阶段的技能（默认档/深度档）、细则文件、产出判定 glob、门禁条目、跳过条件和裁剪区间。
README 和 SKILL.md 里的表都是它的人读摘要，**不一致以 YAML 为准**，且 `validate-plugins.py` 会校验两者对得上。

**「快速开发」「只补文档」「上线体检」不是另一条流程，是同一条流程的裁剪** —— 阶段编号永不改变，
跳过的阶段在任务清单里标注「已跳过（理由）」，断点续跑靠这个判断。

| 裁剪 | 阶段区间 | 什么时候用 |
| --- | --- | --- |
| 全量 | 0 → 12 | 新项目，代码还没有 |
| 三端全栈 0-1 | 0,1,2,3,4,5,6,**7深**,9,10,11,12 | 移动端 + 管理端 + 后端一起做 |
| 有 SRS 直接开工 | 5 → 12 | 文档齐了只要实现 |
| 只要文档链 | 1,2,3,4 | 交付设计文档，不写代码 |
| 迭代 | 1,5,7,9,10,12 | 已有代码库加一批功能 |
| 单页面 / 小改 | 7,9,10 | 加一两个页面 |
| 上线体检 | 11 | 代码写完了（尤其 AI 写的） |
| 反向补文档 | 1,3,4 的反向同步模式 | 代码先行、文档缺失 |

---

## 4 个 plugin / 24 个技能

### `dev-core` — 研发总控与全栈实现

| 技能 | 干什么 |
| --- | --- |
| **`dev-master`** | **库的唯一入口**。13 阶段流程编排、单点路由、裁剪、默认/深度档换挡、断点续跑 |
| `dev-fullstack-product` | 三端全栈 0-1 SOP：技术栈逐项确认 → 模块化开发 → 三轮真跑测试 → 12 角色专家评审 → 交付 |
| `delivery-plan` | 交付计划、开发顺序、进度追踪、按计划连续实现 |
| `project-init` | 新项目脚手架与开发规范初始化 |
| `start-work` | 会话开头恢复上次的上下文 |

### `dev-docs` — 研发文档链

| 技能 | 干什么 |
| --- | --- |
| `req-doc` | **SRS 需求规格说明书**——研发侧唯一规格真源；含 PRD→SRS 转写（Step F）与从代码反向同步 |
| `feature-list` | 从 SRS 提取功能清单，导出 xlsx / Word |
| `hld-design` | 概要设计：分层、模块划分、技术选型、部署拓扑 |
| `lld-design` | 详细设计三合一：模块详细设计 + 数据库物理设计 + API 详细设计 |
| `annotation` | 原型标注：在页面上注入字段说明、业务规则、交互逻辑 |
| `diagram-generator` | 流程图/架构图/时序图/泳道图/ER图/UML/思维导图/BPMN，走 draw.io 渲染 |

### `dev-impl` — 实现与界面

| 技能 | 干什么 |
| --- | --- |
| `page-generator` | 在已有项目里按 SRS 实现业务页面，遵循项目规范/路由/Mock/组件约定 |
| `ui-ux-pro-max` | UI/UX 设计决策与评审（本地数据库检索）+ 设计稿与预览墙交付 |
| `ui-frosted-gradient-clear-sleeve` | 磨砂玻璃材质、深浅双主题令牌、层级契约与 backdrop-filter 降级；设计稿外壳直接内联它的 `assets/` |
| `frontend-design` | 直接编码交付有辨识度的前端界面 |

### `dev-quality` — 质量与上线

| 技能 | 干什么 |
| --- | --- |
| `pm-test-cases` | 功能/边界/异常/权限四类测试用例，导出 Word |
| `webapp-testing` | 真的把 Web 应用跑起来点一遍 |
| `test-driven-development` | 先写测试再写实现 |
| `systematic-debugging` | 系统化排障：复现 → 缩范围 → 定根因 → 修 → 回归 |
| `verification-before-completion` | 完工前验证：说做完的事是不是真做完了 |
| `pm-ai-ship-audit` | AI 生成代码的上线前审计：文档基线 + 意图 vs 实现 + 静态安全/性能审计 |
| `pm-operation-manual` | 操作手册 / 用户指南（含 Puppeteer 自动截图） |
| `pm-release-notes` | 发版说明 |
| `finishing-branch` | 分支收尾：验证 → merge / PR / 保留 / 丢弃 |

---

## 贯穿全程的三条铁律

1. **SRS 真源门禁**：阶段 2–8 的技能**不得以 PRD 为规格真源**。PRD 的产品视角描述缺字段、缺校验、缺状态流转，
   拿它当真源的结果是下游各自猜一套。只有 PRD 时走 `req-doc` **Step F** 转写。规则原文在 `skills/common/prd-to-srs-gate.md`。
2. **图一律走 `diagram-generator`**，禁止手绘；改过文案的图必须重渲（源与图片 mtime 对不上就是过期图）。
3. **Word 导出放在最后**：导出读的是启动那一刻的 md，任何编辑之后都要重新导出；
   导完验图 `unzip -l x.docx | grep -c 'word/media/'`，数字要等于图片张数。

---

## 安装

### Claude Code（plugin marketplace，推荐）

```bash
claude plugin marketplace add iDWong/dev-skills
claude plugin install dev-core dev-docs dev-impl dev-quality
```

**四个 bundle 是一套，建议一起装。** 拆分只为按需卸载，不是四个独立产品——
`dev-master` 编排的技能分布在全部四个 bundle 里，只装 `dev-core` 的话流程从阶段 1 就断。
单装某一个 bundle 的实际可用范围：

| 只装 | 还能用什么 | 用不了什么 |
| --- | --- | --- |
| `dev-core` | `dev-fullstack-product`（自足的三端 SOP）、`delivery-plan`、`project-init` | `dev-master` 的流程（阶段 1–12 的技能都不在） |
| `dev-docs` | SRS / 功能清单 / 概要 / 详细设计 / 图表，文档链完整 | 实现、测试、上线 |
| `dev-impl` | 页面实现、设计稿、玻璃材质 | 上游文档、下游质量 |
| `dev-quality` | 测试、排障、审计、手册、发版 | 上游全部 |

### Codex / Cursor / Claude 非 plugin 模式（平铺）

```bash
bash install.sh claude     # 或 codex / cursor / all
```

> `install.sh` **故意不设默认目标**：不带参数只打印用法。平铺安装会覆盖目标里的同名技能目录，
> 想先看效果就 `DEV_SKILLS_ROOT=$(mktemp -d) bash install.sh claude` 装到临时目录。

### 导出与渲染要配端点

Word/xlsx 导出与 draw.io 渲染需要在**技能根**（不是某个技能目录里）放 `config.json`：

```bash
cp dev-docs/skills/config.example.json ~/.claude/skills/config.json
# 填 apiBaseUrl（文档导出服务）与 diagramApiUrl（图表渲染服务）
```

不配也能用其余技能，只是不能一键导 Word/xlsx、不能渲染图表。

---

## 和 `pm-skills` 的关系

| | [`pm-skills`](https://github.com/iDWong/pm-skills) | `dev-skills`（本库） |
| --- | --- | --- |
| 管什么 | 产品侧：战略 → 调研 → 画像 → 优先级 → 路线图 → PRD | 研发侧：SRS → 设计 → 实现 → 测试 → 上线 |
| 入口 | `pm-master`（13 阶段） | `dev-master`（13 阶段） |
| 交接 | 它的阶段 5 产出需求文档 | 本库**阶段 1** 接手，把 PRD 转写成 SRS 真源 |

**两库有 13 个重叠技能**（`req-doc`、`page-generator`、`ui-ux-pro-max`、`pm-test-cases` 等）——
**是同一份技能的两处分发，不是两个版本**。两库都装时，平铺安装后同名目录只有一份；
plugin 模式下按 Claude Code 的技能去重规则生效。**不要同时起两个总控的任务清单**。

少数技能的文档里会引用姊妹库的技能（如 `pm-roadmap-planner`、`feasibility-report`），
引用处已注明来源，装了就能用，没装也不影响本库流程。

**只装 dev-skills 也完整**——本库不读 `pm-skills` 的任何文件。只有 5 处「细则见姊妹库某文档」的软指针，
自检会以警告列出，未装 pm-skills 时忽略即可：

| 位置 | 指向 | 没装的影响 |
| --- | --- | --- |
| `common/prd-to-srs-gate.md`（4 份） | `pm-master/references/stages/s5-spec.md` | 无——那是 pm-master 流程内的分支表，本库流程用 `dev-master` 自己的阶段 1 |
| `req-doc/SKILL.md` | 同上 | 无 |
| `req-doc/references/prd-to-srs-handoff.md` | `prd-writer/references/self-check.md` | PRD 定稿判据少一份参考，转写照跑 |
| `diagram-generator/examples/模板索引.md` | `pm-prd-spec/SKILL.md` | 少一条模板索引条目 |

**硬依赖（真去读文件的）一律打包在本库内**，自检里是**报错**不是警告——
`ui-frosted-gradient-clear-sleeve` 就是因此纳入 `dev-impl` 的：`ui-ux-pro-max` 的设计稿外壳要内联它的
`assets/frosted.css`、`tokens.json`、`glass-tier.js`。

反向也一样：`pm-skills` 单装完整，它对本库技能只有一处散文路由提及（`pm-ai-ship-audit` → `systematic-debugging`），不读任何文件。

---

## 工具权限

20 / 23 个技能在 frontmatter 里声明了 `allowed-tools`。**故意没声明的三个**：
`dev-master`（编排器，要调用其他技能）、`dev-fullstack-product` 和 `webapp-testing`
（要驱动浏览器与模拟器，工具名随宿主而变）—— 给它们写死白名单会在别的宿主上把自己锁死。

## 自检

```bash
python3 scripts/validate-plugins.py
```

检查五类问题：

| 检查 | 内容 |
| --- | --- |
| 清单一致性 | marketplace 与 plugin.json 互相对得上、技能 frontmatter 合规、技能名不重复 |
| 引用可解析 | 跨技能引用、references 自引用；引用姊妹库 `pm-skills` 的技能走白名单放行 |
| 图片路径 | md 里的图片引用不得带 `docs/` 前缀（会让 Word 导出丢图） |
| **硬依赖** | 文件级跨技能引用（`<技能>/references/…`）必须能在本仓解析；姊妹库软指针降级为警告 |
| **阶段目录** | `workflow-catalog.yaml` 的阶段号连续、每个阶段的技能在库内、细则文件存在、与 `dev-master/SKILL.md` 的阶段表逐行对得上 |
| **行为规格** | 跑 [`scripts/skill-specs/`](scripts/skill-specs) 里的 `[static]` 断言（当前 29 条）；`[behavior]` 断言留给人跑一遍技能后对照 |

CI 每次 push 跑一遍。加新技能规格见 [`scripts/skill-specs/README.md`](scripts/skill-specs/README.md)。
