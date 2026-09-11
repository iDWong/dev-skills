# Skill Spec: dev-fullstack-product

## 摘要

三端（移动端 + 运营管理端 + 后端）0-1 全栈交付 SOP。七个阶段：输入前置检查 → 技术栈确认 →
开发规范 → 分模块开发 → 测试与验收（≥3 轮真跑）→ 12 角色专家评审 → 交付。

## 静态断言

- [static] file-exists: references/tech-stack-matrix.md
- [static] file-exists: references/dev-standards.md
- [static] file-exists: references/test-protocol.md
- [static] file-exists: references/expert-review.md
- [static] contains: prd-to-srs-gate\.md
- [static] contains: 禁止跳步
- [static] contains: 至少 3 轮|三轮
- [static] contains: 12 类角色|12 角色
- [static] contains: docs/dev-fullstack-
- [static] contains: 1:1
- [static] frontmatter-has: name
- [static] frontmatter-has: description

## 行为断言

- [behavior] 阶段 0 先跑真源门禁：只有 PRD 时给出门禁话术并中止，不得直接开工
- [behavior] 阶段 0 的文档清点表逐项标 ✅/❌/⚠️ 并写出实际文件路径，不是空表
- [behavior] 阶段 0 的澄清问题只问文档里查不到的，且每条带默认建议（不是开放式提问）
- [behavior] 阶段 1 提案前先探测本机环境（node/java/go/python/docker/数据库），推荐项不含装不上的东西
- [behavior] 阶段 1 每行带版本号与一句选型理由，用户逐项确认后写进进度存档且不再擅自更换
- [behavior] 上游已有概要设计时，阶段 1 是「确认已定选型」，不是推翻重选
- [behavior] 每个模块完成后先自检七项再汇报，自检不过不汇报
- [behavior] 测试报告里没跑的用例标「未执行」，跑挂的标「失败」并贴报错——不得写成「通过」
- [behavior] Web 端测试用 Browser 工具真跑，移动端用模拟器工具真跑；不能驱动的端明确标注「未执行」
- [behavior] 专家评审每个角色至少 3 条意见，每条指到 file:line / 页面 / 接口，不出现「代码质量尚可」这类空话
- [behavior] 评审不符合项当场整改并回填闭环状态，全部闭环才进交付阶段
- [behavior] 交付阶段给出的运行/部署命令是实跑验证过的，不是照抄模板

## 已知不测

- 生成代码本身的质量（交给阶段 9/10/11 与 `pm-ai-ship-audit`）
- 真实生产环境部署（只产脚本与清单）
