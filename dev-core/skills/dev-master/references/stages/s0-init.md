# 阶段 0：项目初始化

**技能**：`project-init` ｜ **产出**：仓库骨架 + `README-DEV.md`

## 做什么
1. 确认项目根目录、子项目划分（`admin/`、`mobile/`、`server/` 等）与命名
2. 建骨架：目录结构、包管理、lint/format 配置、`.env.example`、`.gitignore`
3. 写 `README-DEV.md`：目录约定、命名规范、路由方式、Mock 约定、启动命令
4. 建 `dev/` 落盘骨架：`dev/{SRS,design,plan,test,reports,release}/`（研发链所有文档产出的唯一去处，阶段 1 的 SRS 落 `dev/SRS/`）
5. `git init` + 首次提交（用户已有仓库时跳过，只补缺的配置文件）

## `project-init` 覆盖不到的两件事，本阶段自己补

| 它产出 | 它不产出 |
| --- | --- |
| 脚手架、TS/ESLint/Prettier 配置、`.gitignore`、`CLAUDE.md`、`README.md`、跑通 dev server | **`README-DEV.md`**、**`dev/` 落盘骨架** |

`README-DEV.md` 是阶段 7 `page-generator` 的首选输入（缺了它会改为读项目文件自行推断，
推断出来的约定和你真正的约定不一定一样）。所以**本阶段结束前必须由流程补写**，别指望技能自动生成。

`project-init` 的第 3、5 步偏 Node/前端工具链（`create-vite`、`npm run dev`、`tsc`）。
后端是 Java/Go/Python 时，前 4 步照走，第 5 步换成对应工具链的「装依赖 → 起服务 → 编译检查」。

## 门禁（进阶段 1 前）
- [ ] 项目根目录确定，后续所有相对路径以它为准
- [ ] `dev/` 骨架已建（`SRS/ design/ plan/ test/ reports/ release/`），研发链产出一律落这儿；
      上游 PRD 与老项目历史文档留在 `docs/`，**只读不写**
- [ ] `README-DEV.md` 已写（阶段 7 要读它）

## 可跳过
仓库已存在且有 `README-DEV.md` → 跳过，只把项目根与子项目划分记进进度存档。
