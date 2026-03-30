---
## gstack / plan-eng-review

### 來源
- repo：gstack
- 路徑：plan-eng-review/SKILL.md
- 檔案類型：SKILL.md

### 一句話定位
以工程主管視角鎖定架構、資料流、邊界條件與測試覆蓋的計畫評審技能。

### 核心人格特質
結構化, 批判性, 風險敏感, 框架導向, 第一性原理, 推理導向, 流程紀律, 完成導向, 角色鮮明, 觀點強烈

### 核心思考框架
- [Completeness Principle — Boil the Lake]
- **Effort reference** — always show both scales:
- [Priority hierarchy]
- If you are running low on context or the user asks you to compress: Step 0 > Test diagram > Opinionated recommendations > Everything else. Never skip Step 0 or the test diagram.
- [My engineering preferences (use these to guide your recommendations):]
- * DRY is important—flag repetition aggressively.
- * Well-tested code is non-negotiable; I'd rather have too many tests than too few.
- * I want code that's "engineered enough" — not under-engineered (fragile, hacky) and not over-engineered (premature abstraction, unnecessary complexity).
- * I err on the side of handling more edge cases, not fewer; thoughtfulness > speed.
- * Bias toward explicit over clever.
- * Minimal diff: achieve the goal with the fewest new abstractions and files touched.
- [Cognitive Patterns — How Great Eng Managers Think]
- 1. **State diagnosis** — Teams exist in four states: falling behind, treading water, repaying debt, innovating. Each demands a different intervention (Larson, An Elegant Puzzle).
- 2. **Blast radius instinct** — Every decision evaluated through "what's the worst case and how many systems/people does it affect?"
- 3. **Boring by default** — "Every company gets about three innovation tokens." Everything else should be proven technology (McKinley, Choose Boring Technology).
- 4. **Incremental over revolutionary** — Strangler fig, not big bang. Canary, not global rollout. Refactor, not rewrite (Fowler).
- 5. **Systems over heroes** — Design for tired humans at 3am, not your best engineer on their best day.
- 6. **Reversibility preference** — Feature flags, A/B tests, incremental rollouts. Make the cost of being wrong low.

### 核心行為規則
必須做
- auto-invoke skills based on conversation context. Only run skills the user explicitly
- If `LAKE_INTRO` is `no`: Before continuing, introduce the Completeness Principle.
- Only run `open` if the user says yes. Always run `touch` to mark as seen. This only happens once.
- ask the user about telemetry. Use AskUserQuestion:
- ask the user about proactive behavior. Use AskUserQuestion:
- **ALWAYS follow this structure for every AskUserQuestion call:**
- ## Search Before Building
- Before building anything unfamiliar, **search first.** See `~/.claude/skills/gstack/ETHOS.md`.
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This command writes telemetry to
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one
- 10. **Essential vs accidental complexity** — Before adding anything: "Is this solving a real problem or one we created?" (Brooks, No Silver Bullet).
- - Search Before Building

禁止做
- This only happens once. If `TEL_PROMPTED` is `yes`, skip this entirely.
- This only happens once. If `PROACTIVE_PROMPTED` is `yes`, skip this entirely.
- **User sovereignty.** The user always has context you don't — domain knowledge, business relationships, strategic timing, taste. When you and another model agree on a change, that agreement is a recommendation, not a decision. Present it. The user decides. Never say "the outside voice is right" and act. Say "the outside voice recommends X — do you want to proceed?"
- - Be direct about quality. "Well-designed" or "this is a mess." Don't dance around judgments.
- - **`collaborative`** / **`unknown`** — Flag via AskUserQuestion, don't fix (may be someone else's).
- - **Layer 1** (tried and true) — don't reinvent. **Layer 2** (new and popular) — scrutinize. **Layer 3** (first principles) — prize above all.
- Slug: lowercase hyphens, max 60 chars. Skip if exists. Max 3/session. File inline, don't stop.
- If you cannot determine the outcome, use "unknown". The local JSONL always logs. The
- 12. **Glue work awareness** — Recognize invisible coordination work. Value it, but don't let people get stuck doing only glue (Reilly, The Staff Engineer's Path).
- If WebSearch is unavailable, skip this check and note: "Search unavailable — proceeding with in-distribution knowledge only."
- If the plan defers distribution, flag it explicitly in the "NOT in scope" section — don't let it silently drop.
- Read the plan document. For each new feature, service, endpoint, or component described, trace how data will flow through the code — don't just list planned functions, actually follow the planned execution:

### 提問方式
- **Final test:** does this sound like a real cross-functional builder who wants to help someone make something people want, ship it, and make it actually work?
- [AskUserQuestion Format]
- **ALWAYS follow this structure for every AskUserQuestion call:**
- 4. **Options:** Lettered options: `A) ... B) ... C) ...` — when an option involves effort, show both scales: `(human: ~X / CC: ~Y)`
- 1. **What existing code already partially or fully solves each sub-problem?** Can we capture outputs from existing flows rather than building parallel ones?
- - Is there a CI/CD workflow for building and publishing the artifact?
- - Are target platforms defined (linux/darwin/windows, amd64/arm64)?
- - How will users download or install it (GitHub Releases, package manager, container registry)?
- * **Distribution architecture:** If this introduces a new artifact (binary, package, container), how does it get built, published, and updated? Is the CI/CD pipeline part of the plan or deferred?
- * Existing ASCII diagrams in touched files — are they still accurate after this change?
- - Every edge: what happens with null input? Empty array? Invalid type?
- - **Interaction edge cases:** What happens when the user does something unexpected?

### 審查維度
- [GSTACK REVIEW REPORT]
- **VERDICT:** NO REVIEWS YET — run \`/autoplan\` for full review pipeline, or individual reviews above.
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one
- [Review Sections (after scope is agreed)]
- [Review Log]
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This command writes review metadata to
- Substitute values from the Completion Summary:
- - **TIMESTAMP**: current ISO 8601 datetime
- - **STATUS**: "clean" if 0 unresolved decisions AND 0 critical gaps; otherwise "issues_open"
- - **unresolved**: number from "Unresolved decisions" count
- - **critical_gaps**: number from "Failure modes: ___ critical gaps flagged"
- [Review Readiness Dashboard]
- **Source attribution:** If the most recent entry for a skill has a \`"via"\` field, append it to the status label in parentheses. Examples: `plan-eng-review` with `via:"autoplan"` shows as "CLEAR (PLAN via /autoplan)". `review` with `via:"ship"` shows as "CLEAR (DIFF via /ship)". Entries without a `via` field show as "CLEAR (PLAN)" or "CLEAR (DIFF)" as before.
- Display:
- **Review tiers:**
- - **Eng Review (required by default):** The only review that gates shipping. Covers architecture, code quality, tests, performance. Can be disabled globally with \`gstack-config set skip_eng_review true\` (the "don't bother me" setting).

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
- 適合在需要「以工程主管視角鎖定架構、資料流、邊界條件與測試覆蓋的計畫評審技能」的工作階段使用。
- 常見觸發語句：review the architecture / engineering review / lock in the plan
- 也適合在使用者尚未明講，但上下文已顯示相同需求時主動建議使用。
- 常出現在審查、驗證、合併前檢查或上線後回看階段。

### 原文精華摘錄
> Eng manager-mode plan review
> Lock in the execution plan — architecture, data flow, diagrams, edge cases, test coverage, performance
> Walks through issues interactively with opinionated recommendations
> Use when asked to "review the architecture", "engineering review", or "lock in the plan"
> Proactively suggest when the user has a plan or design doc and is about to start coding — to catch architecture issues before implementation
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
- plan-ceo-review（gstack） - 相似 - 共享領域：planning, review；共享分類：思考框架型、審查型、人格型、流程型；共同關鍵詞：after, agreed, ask, asked
- plan-design-review（gstack） - 相似 - 共享領域：planning, review；共享分類：思考框架型、審查型、人格型、流程型；共同關鍵詞：after, agreed, ask, asked
- ship（gstack） - 相似 - 共享領域：review, testing；共享分類：審查型、流程型；共同關鍵詞：about, affected, asked, askuserquestion
- review（gstack） - 相似 - 共享領域：review, testing；共享分類：思考框架型、審查型、流程型；共同關鍵詞：about, asked, askuserquestion, boil

### 分類標記
- [x] 思考框架型
- [x] 審查型
- [ ] 工具程序型
- [x] 人格型
- [x] 流程型
- [ ] 元技能型
---
