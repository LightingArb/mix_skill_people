---
## gstack / investigate

### 來源
- repo：gstack
- 路徑：investigate/SKILL.md
- 檔案類型：SKILL.md

### 一句話定位
以根因調查、模式分析、假設驗證到實作的流程來系統化除錯。

### 核心人格特質
框架導向, 第一性原理, 推理導向, 流程紀律, 完成導向, 證據導向, 懷疑論

### 核心思考框架
- [Completeness Principle — Boil the Lake]
- **Effort reference** — always show both scales:
- [Iron Law]
- **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**
- [Phase 1: Root Cause Investigation]
- 1. **Collect symptoms:** Read the error messages, stack traces, and reproduction steps. If the user hasn't provided enough context, ask ONE question at a time via AskUserQuestion.
- 2. **Read the code:** Trace the code path from the symptom back to potential causes. Use Grep to find all references, Read to understand the logic.
- 3. **Check recent changes:**
- 4. **Reproduce:** Can you trigger the bug deterministically? If not, gather more evidence before proceeding.
- [Phase 2: Pattern Analysis]
- Check if this bug matches a known pattern:
- Also check:
- - `TODOS.md` for related known issues
- - `git log` for prior fixes in the same area — **recurring bugs in the same files are an architectural smell**, not a coincidence
- **External pattern search:** If the bug doesn't match a known pattern above, WebSearch for:
- - "{framework} {generic error type}" — **sanitize first:** strip hostnames, IPs, file paths, SQL, customer data. Search the error category, not the raw message.
- [Phase 3: Hypothesis Testing]
- 1. **Confirm the hypothesis:** Add a temporary log statement, assertion, or debug output at the suspected root cause. Run the reproduction. Does the evidence match?

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
- If `CROSS_PROJECT` is `unset` (first time): Use AskUserQuestion:
- Before writing ANY fix, verify your hypothesis.
- 2. **If the hypothesis is wrong:** Before forming the next hypothesis, consider searching for the error. **Sanitize first** — strip hostnames, IPs, file paths, SQL fragments, customer identifiers, and any internal/proprietary data from the error message. Search only the generic error type and framework context: "{component} {sanitized error type} {framework version}". If the error message is too specific to sanitize safely, skip the search. If WebSearch is unavailable, skip and proceed. Then return to Phase 1. Gather more evidence. Do not guess.
- 3. **3-strike rule:** If 3 hypotheses fail, **STOP**. Use AskUserQuestion:

禁止做
- This only happens once. If `TEL_PROMPTED` is `yes`, skip this entirely.
- This only happens once. If `PROACTIVE_PROMPTED` is `yes`, skip this entirely.
- **User sovereignty.** The user always has context you don't — domain knowledge, business relationships, strategic timing, taste. When you and another model agree on a change, that agreement is a recommendation, not a decision. Present it. The user decides. Never say "the outside voice is right" and act. Say "the outside voice recommends X — do you want to proceed?"
- - Be direct about quality. "Well-designed" or "this is a mess." Don't dance around judgments.
- Slug: lowercase hyphens, max 60 chars. Skip if exists. Max 3/session. File inline, don't stop.
- If you cannot determine the outcome, use "unknown". The local JSONL always logs. The
- If WebSearch is unavailable, skip this search and proceed with hypothesis testing. If a documented solution or known dependency bug surfaces, present it as a candidate hypothesis in Phase 3.
- **Fresh verification:** Reproduce the original bug scenario and confirm it's fixed. This is not optional.
- **Only log genuine discoveries.** Don't log obvious things. Don't log things the user
- - **Never apply a fix you cannot verify.** If you can't reproduce and confirm, don't ship it.
- - DONE_WITH_CONCERNS — fixed but cannot fully verify (e.g., intermittent bug, requires staging)

### 提問方式
- **Final test:** does this sound like a real cross-functional builder who wants to help someone make something people want, ship it, and make it actually work?
- [AskUserQuestion Format]
- **ALWAYS follow this structure for every AskUserQuestion call:**
- 4. **Options:** Lettered options: `A) ... B) ... C) ...` — when an option involves effort, show both scales: `(human: ~X / CC: ~Y)`
- 1. **Confirm the hypothesis:** Add a temporary log statement, assertion, or debug output at the suspected root cause. Run the reproduction. Does the evidence match?

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
- 適合在需要「以根因調查、模式分析、假設驗證到實作的流程來系統化除錯」的工作階段使用。
- 常見觸發語句：debug this / fix this bug / why is this broken / investigate this error / root cause analysis
- 也適合在使用者尚未明講，但上下文已顯示相同需求時主動建議使用。

### 原文精華摘錄
> Systematic debugging with root cause investigation
> Four phases: investigate, analyze, hypothesize, implement
> Iron Law: no fixes without root cause
> Use when asked to "debug this", "fix this bug", "why is this broken", "investigate this error", or "root cause analysis"
> Proactively suggest when the user reports errors, unexpected behavior, or is troubleshooting why something stopped working
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

### 和其他 skill 的潛在關聯
- qa（gstack） - 相似 - 共享領域：debugging；共享分類：流程型；共同關鍵詞：asked, askuserquestion, boil, broken
- qa-only（gstack） - 相似 - 共享領域：debugging；共享分類：流程型；共同關鍵詞：asked, askuserquestion, boil, bug
- review（gstack） - 相似 - 共享分類：思考框架型、流程型；共同關鍵詞：asked, askuserquestion, boil, capture
- autoplan（gstack） - 互補 - 共享分類：流程型；共同關鍵詞：asked, askuserquestion, boil, completeness

### 分類標記
- [x] 思考框架型
- [ ] 審查型
- [ ] 工具程序型
- [ ] 人格型
- [x] 流程型
- [ ] 元技能型
---
