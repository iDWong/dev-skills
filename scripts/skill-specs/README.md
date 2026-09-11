# 技能行为规格（skill specs）

每份 `<技能名>.md` 描述这个技能**应该怎么表现**，分两类断言：

| 前缀 | 谁来验 | 说明 |
|---|---|---|
| `- [static]` | `scripts/validate-plugins.py` **自动跑**，CI 里也跑 | 结构性、可机器判定 |
| `- [behavior]` | 人或模型**手动跑一遍技能**后对照 | 行为性，机器判不了 |

## `[static]` 支持的指令

```
- [static] contains: <正则>            技能目录下任一 .md 必须匹配
- [static] not-contains: <正则>        任一 .md 都不得匹配
- [static] frontmatter-has: <键名>     SKILL.md 的 frontmatter 必须有这个键
- [static] file-exists: <相对路径>     技能目录下必须存在这个文件
```

正则用 Python 语法，**整行原样取**（冒号后第一个空格之后的全部内容），所以可以带空格和中文。

## 加一份新规格

1. 建 `scripts/skill-specs/<技能名>.md`
2. 照下面三份的结构写：摘要 / 静态断言 / 行为断言 / 已知不测
3. `python3 scripts/validate-plugins.py` —— 静态断言会自动纳入校验

规格文件里的技能名必须能在仓库里找到，否则自检报错（防止技能改名后规格变成孤儿）。
