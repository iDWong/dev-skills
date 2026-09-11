# Skill Spec: req-doc

## 摘要

SRS 需求规格说明书的生成/细化/审查/反向同步，以及 **PRD→SRS 转写（Step F）**。
它是整条研发链的规格真源提供者——`dev-master` 阶段 1 与六个下游技能的门禁都指向它。

## 静态断言

- [static] contains: Step F
- [static] contains: docs/SRS/
- [static] contains: 反向
- [static] frontmatter-has: name
- [static] frontmatter-has: description
- [static] frontmatter-has: allowed-tools

## 行为断言

- [behavior] 用户只有 PRD 且要求「进开发」时，默认直接转写，不反问「是否需要转写」
- [behavior] 转写产出含三个内容角色：功能清单、页面清单、字段级功能详细设计
- [behavior] 章节定位先读文档目录，不因为「没有 3.1/3.3/3.5 这个号」就判一份合格 SRS 不合格
- [behavior] 文档里的流程图/架构图/ER 图交给 `diagram-generator`，不手绘 ASCII 或手写 mermaid 充数
- [behavior] 导出 Word 放在所有编辑之后，导完验 `word/media/` 图片数与图片张数一致
- [behavior] 反向同步模式下，从现有页面/接口回写的章节标注来源，不与人工撰写内容混淆

## 已知不测

- 需求内容本身的业务正确性
- Word 导出端点未配置时的降级路径（属 `common/` 的职责）
