---
## superpowers / using-git-worktrees

### 來源
- repo：superpowers
- 路徑：skills/using-git-worktrees/SKILL.md
- 檔案類型：SKILL.md

### 一句話定位
用 git worktree 建立隔離工作目錄，安全展開多線開發。

### 核心人格特質
流程紀律, 完成導向, 務實, 操作導向, 證據導向, 懷疑論, 謹慎, 防呆導向, 協作導向, 拆解導向

### 核心思考框架
- [Overview]
- **Core principle:** Systematic directory selection + safety verification = reliable isolation.
- **Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."
- [Directory Selection Process]
- Follow this priority order:
- **If found:** Use that directory. If both exist, `.worktrees` wins.
- **If preference specified:** Use it without asking.
- If no directory exists and no CLAUDE.md preference:
- [Example Workflow]

### 核心行為規則
必須做
- **MUST verify directory is ignored before creating worktree:**
- - **brainstorming** (Phase 4) - REQUIRED when design is approved and implementation follows
- - **subagent-driven-development** - REQUIRED before executing any tasks
- - **executing-plans** - REQUIRED before executing any tasks
- - **finishing-a-development-branch** - REQUIRED for cleanup after work complete

禁止做
- 原文過短，無法提取

### 提問方式
無明確提問模板

### 審查維度
非審查型

### 輸出格式要求
無特定格式要求

### 適用場景
- 適合在需要「用 git worktree 建立隔離工作目錄，安全展開多線開發」的工作階段使用。
- 常出現在審查、驗證、合併前檢查或上線後回看階段。

### 原文精華摘錄
> Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
> Overview
> **Core principle:** Systematic directory selection + safety verification = reliable isolation.
> **Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."
> Directory Selection Process
> Follow this priority order:
> **If found:** Use that directory. If both exist, `.worktrees` wins.
> **If preference specified:** Use it without asking.
> If no directory exists and no CLAUDE.md preference:
> Safety Verification

### 和其他 skill 的潛在關聯
- finishing-a-development-branch（superpowers） - 相似 - 共享領域：shipping；共享分類：工具程序型、流程型；共同關鍵詞：common, flags, integration, mistakes
- subagent-driven-development（superpowers） - 相似 - 共享領域：parallel；共享分類：工具程序型、流程型；共同關鍵詞：current, example, executing, flags
- writing-skills（superpowers） - 互補 - 共享分類：流程型；共同關鍵詞：common, creation, directory, flags
- verification-before-completion（superpowers） - 相似 - 共享領域：shipping；共享分類：流程型；共同關鍵詞：common, flags, overview, red

### 分類標記
- [ ] 思考框架型
- [ ] 審查型
- [x] 工具程序型
- [ ] 人格型
- [x] 流程型
- [ ] 元技能型
---
