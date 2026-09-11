# Skill Spec: dev-master

## 摘要

研发链的唯一编排器。判断单点/流程/排障三类诉求；流程类按 `workflow-catalog.yaml` 裁剪出阶段区间，
逐阶段调用对应技能，保证上一阶段产出是下一阶段的合法输入。它**不亲自产出内容**。

## 静态断言

- [static] file-exists: workflow-catalog.yaml
- [static] file-exists: references/flow-engine.md
- [static] file-exists: references/tailoring.md
- [static] file-exists: references/stages/s1-srs.md
- [static] file-exists: references/stages/s7-implement.md
- [static] contains: 阶段的权威定义在 `workflow-catalog.yaml`
- [static] contains: prd-to-srs-gate\.md
- [static] contains: 阶段 1 不可跳过
- [static] contains: 别名：dve-master
- [static] contains: pm-master
- [static] not-contains: 我来直接写这份文档

## 行为断言

- [behavior] 用户只要一份产出（如「写个详细设计」）时，直接路由到 `lld-design`，**不建任务清单、不起流程**
- [behavior] 用户说「从需求到上线」时，先问 Step 0 四问（起点/裁剪/阶段7档位/交付模式），再建任务清单
- [behavior] 用户已经说明了起点和范围时，不再把四问原样问一遍
- [behavior] 项目里只有 `docs/PRD/` 没有 `docs/SRS/` 时，阶段 1 必须给出门禁话术并停下，不得继续跑阶段 2
- [behavior] 用户说「三端」「整套系统」时，阶段 7 直接挂深度档 `dev-fullstack-product`，不再问档位
- [behavior] 阶段 7 走了深度档后，阶段 9 输出的是「校验它的三轮测试报告」，不是重新跑一轮测试
- [behavior] 每个阶段结束按 SKILL.md 末尾的八行格式汇报，且「门禁检查」一栏写清下一阶段输入是否齐备
- [behavior] 已存在 `docs/dev-master-*.md` 时，先念进度摘要并问「续跑/重来/改裁剪」，不从 Step 0 重问

## 已知不测

- 阶段技能自身的产出质量（由各技能自己的规格覆盖）
- 与 `pm-master` 同时起流程时的冲突（约定是不要同时起，未做机制防护）
