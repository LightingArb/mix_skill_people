---
## gstack / document-release

### 來源
- repo：gstack
- 路徑：document-release/SKILL.md
- 檔案類型：SKILL.md

### 一句話定位
在發版後同步更新 README、架構與變更記錄等文件的文件收尾技能。

### 核心人格特質
流程紀律, 完成導向, 務實, 操作導向

### 核心思考框架
- [Completeness Principle — Boil the Lake]
- **Effort reference** — always show both scales:

### 核心行為規則
必須做
- auto-invoke skills based on conversation context. Only run skills the user explicitly
- If `LAKE_INTRO` is `no`: Before continuing, introduce the Completeness Principle.
- Only run `open` if the user says yes. Always run `touch` to mark as seen. This only happens once.
- ask the user about telemetry. Use AskUserQuestion:
- ask the user about proactive behavior. Use AskUserQuestion:
- **ALWAYS follow this structure for every AskUserQuestion call:**
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This command writes telemetry to
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one
- - Auto-fix minor voice adjustments. Use AskUserQuestion if a rewrite would alter meaning.
- version mismatch). Use AskUserQuestion for narrative contradictions.
- significantly changed, its description may be stale. Use AskUserQuestion to confirm whether
- 3. **If VERSION was NOT bumped:** Use AskUserQuestion:

禁止做
- This only happens once. If `TEL_PROMPTED` is `yes`, skip this entirely.
- This only happens once. If `PROACTIVE_PROMPTED` is `yes`, skip this entirely.
- **User sovereignty.** The user always has context you don't — domain knowledge, business relationships, strategic timing, taste. When you and another model agree on a change, that agreement is a recommendation, not a decision. Present it. The user decides. Never say "the outside voice is right" and act. Say "the outside voice recommends X — do you want to proceed?"
- - Be direct about quality. "Well-designed" or "this is a mess." Don't dance around judgments.
- Slug: lowercase hyphens, max 60 chars. Skip if exists. Max 3/session. File inline, don't stop.
- If you cannot determine the outcome, use "unknown". The local JSONL always logs. The
- **NEVER do:**
- **CRITICAL — NEVER CLOBBER CHANGELOG ENTRIES.**
- preserved them. This skill must NEVER do that.
- **If CHANGELOG was not modified in this branch:** skip this step.
- If TODOS.md does not exist, skip this step.
- **CRITICAL — NEVER BUMP VERSION WITHOUT ASKING.**

### 提問方式
- **Final test:** does this sound like a real cross-functional builder who wants to help someone make something people want, ship it, and make it actually work?
- [AskUserQuestion Format]
- **ALWAYS follow this structure for every AskUserQuestion call:**
- 4. **Options:** Lettered options: `A) ... B) ... C) ...` — when an option involves effort, show both scales: `(human: ~X / CC: ~Y)`
- - Does it describe all features and capabilities visible in the diff?
- - Are install/setup instructions consistent with the changes?
- - Are examples, demos, and usage descriptions still valid?
- - Are troubleshooting steps still accurate?
- - Do ASCII diagrams and component descriptions match the current code?
- - Are design decisions and "why" explanations still accurate?
- - Are the listed commands accurate? Would each step succeed?
- - Do test tier descriptions match the current test infrastructure?

### 審查維度
非審查型

### 輸出格式要求
- [AskUserQuestion Format]
- **ALWAYS follow this structure for every AskUserQuestion call:**
- 1. **Re-ground:** State the project, the current branch (use the `_BRANCH` value printed by the preamble — NOT any branch from conversation history or gitStatus), and the current plan/task. (1-2 sentences)
- 2. **Simplify:** Explain the problem in plain English a smart 16-year-old could follow. No raw function names, no internal jargon, no implementation details. Use concrete examples and analogies. Say what it DOES, not what it's called.
- 3. **Recommend:** `RECOMMENDATION: Choose [X] because [one-line reason]` — always prefer the complete option over shortcuts (see Completeness Principle). Include `Completeness: X/10` for each option. Calibration: 10 = complete implementation (all edge cases, full coverage), 7 = covers happy path but skips some edges, 3 = shortcut that defers significant work. If both options are 8+, pick the higher; if one is ≤5, flag it.
- 4. **Options:** Lettered options: `A) ... B) ... C) ...` — when an option involves effort, show both scales: `(human: ~X / CC: ~Y)`
- [Plan Status Footer]
- When you are in plan mode and about to call ExitPlanMode:
- 1. Check if the plan file already has a `## GSTACK REVIEW REPORT` section.
- 2. If it DOES — skip (a review skill already wrote a richer report).
- 3. If it does NOT — run this command:
- Then write a `## GSTACK REVIEW REPORT` section to the end of the plan file:
- - If the output contains review entries (JSONL lines before `---CONFIG---`): format the
- [GSTACK REVIEW REPORT]

### 適用場景
- 適合在需要「在發版後同步更新 README、架構與變更記錄等文件的文件收尾技能」的工作階段使用。
- 常見觸發語句：update the docs / sync documentation / post-ship docs
- 也適合在使用者尚未明講，但上下文已顯示相同需求時主動建議使用。
- 常出現在收尾、發布、分支整理或部署交接階段。

### 原文精華摘錄
> Post-ship documentation update
> Reads all project docs, cross-references the diff, updates README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md to match what shipped, polishes CHANGELOG voice, cleans up TODOS, and optionally bumps VERSION
> Use when asked to "update the docs", "sync documentation", or "post-ship docs"
> Proactively suggest after a PR is merged or code is shipped
> Preamble (run first)
> types (e.g., /qa, /ship). If you would have auto-invoked a skill, instead briefly say:
> Then offer to open the essay in their default browser:
> ask the user about telemetry. Use AskUserQuestion:
> Options:
> Voice
> **Core belief:** there is no one at the wheel. Much of the world is made up. That is not scary. That is the opportunity. Builders get to make new things real. Write in a way that makes capable people, especially young builders early in their careers, feel t...
> **Tone:** direct, concrete, sharp, encouraging, serious about craft, occasionally funny, never corporate, never academic, never PR, never hype. Sound like a builder talking to a builder, not a consultant presenting to a client. Match the context: YC partner...
> **Humor:** dry observations about the absurdity of software. "This is a 200-line config file to print hello world." "The test suite takes longer than the feature it tests." Never forced, never self-referential about being AI.
> **Concreteness is the standard.** Name the file, the function, the line number. Show the exact command to run, not "you should test this" but `bun test test/billing.test.ts`. When explaining a tradeoff, use real numbers: not "this might be slow" but "this q...
> AskUserQuestion Format
> **ALWAYS follow this structure for every AskUserQuestion call:**

### 和其他 skill 的潛在關聯
- ship（gstack） - 相似 - 共享領域：shipping；共享分類：工具程序型、流程型；共同關鍵詞：about, asked, askuserquestion, audit
- review（gstack） - 相似 - 共享領域：shipping；共享分類：流程型；共同關鍵詞：about, asked, askuserquestion, base
- plan-ceo-review（gstack） - 互補 - 共享分類：流程型；共同關鍵詞：after, ask, asked, askuserquestion
- qa（gstack） - 互補 - 共享分類：工具程序型、流程型；共同關鍵詞：after, asked, askuserquestion, base

### 分類標記
- [ ] 思考框架型
- [ ] 審查型
- [x] 工具程序型
- [ ] 人格型
- [x] 流程型
- [ ] 元技能型
---
