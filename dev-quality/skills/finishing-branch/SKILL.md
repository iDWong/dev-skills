---
name: finishing-branch
description: 开发分支完成后的结构化收尾流程 — 验证测试、检测环境、提供 merge/PR/保留/丢弃 四选项
---

# 完成开发分支

## 概述

开发工作完成后，引导用户选择集成方式。

**核心流程：** 验证测试 → 检测环境 → 提供选项 → 执行选择 → 清理

**启动时声明：** "使用 finishing-branch 技能完成分支收尾。"

## 触发条件

- 用户说"完成了"、"可以合并了"、"提 PR"、"分支完成"
- 所有计划任务已完成且测试通过

## 流程

### Step 1: 验证测试

```bash
cd admin && npx vue-tsc --noEmit && npx vite build
```

测试失败 → 停止，修复后才能继续。

### Step 2: 检测环境

```bash
CURRENT_BRANCH=$(git branch --show-current)
BASE_BRANCH=$(git merge-base --fork-point main HEAD 2>/dev/null && echo "main" || echo "master")
```

### Step 3: 提供选项

```
开发完成。请选择：

1. 本地合并到 <base-branch>
2. 推送并创建 Pull Request
3. 保留分支（稍后处理）
4. 丢弃这些工作
```

### Step 4: 执行选择

#### 选项 1: 本地合并

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
# 验证合并后测试
cd admin && npx vue-tsc --noEmit
# 成功后删除分支
git branch -d <feature-branch>
```

#### 选项 2: 推送并创建 PR

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## 总结
<变更摘要>

## 验证
- [ ] 构建通过
- [ ] 类型检查通过
EOF
)"
```

#### 选项 3: 保留

报告分支名和当前状态，不做任何操作。

#### 选项 4: 丢弃

**必须确认：**
```
将永久删除：
- 分支 <name>
- 所有 commit: <list>

输入 'discard' 确认。
```

等待确认后执行 `git branch -D <feature-branch>`。

## 红旗

- 测试未通过不能提供选项
- 丢弃前必须确认
- 不能 force-push 除非用户明确要求
- PR 创建后不清理本地分支（用户可能需要迭代）
