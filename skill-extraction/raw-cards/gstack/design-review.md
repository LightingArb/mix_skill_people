---
## gstack / design-review

### 來源
- repo：gstack
- 路徑：design-review/SKILL.md
- 檔案類型：SKILL.md

### 一句話定位
以設計師視角檢查並修正 UI 一致性、節奏與互動品質的設計 QA 技能。

### 核心人格特質
結構化, 批判性, 風險敏感, 流程紀律, 完成導向, 角色鮮明, 觀點強烈, 品味導向, 體驗敏感

### 核心思考框架
- [Completeness Principle — Boil the Lake]
- **Effort reference** — always show both scales:
- [Phases 1-6: Design Audit Baseline]
- [Modes]
- When on a feature branch, scope to pages affected by the branch changes:
- 1. Analyze the branch diff: `git diff main...HEAD --name-only`
- 2. Map changed files to affected pages/routes
- 3. Detect running app on common local ports (3000, 4000, 8080)
- 4. Audit only affected pages, compare design quality before/after
- [Phase 1: First Impression]
- 1. Navigate to the target URL
- 2. Take a full-page desktop screenshot: `$B screenshot "$REPORT_DIR/screenshots/first-impression.png"`
- 3. Write the **First Impression** using this structured critique format:
- - "The site communicates **[what]**." (what it says at a glance — competence? playfulness? confusion?)
- - "I notice **[observation]**." (what stands out, positive or negative — be specific)
- - "The first 3 things my eye goes to are: **[1]**, **[2]**, **[3]**." (hierarchy check — are these intentional?)
- [Phase 2: Design System Extraction]
- Extract the actual design system the site uses (not what a DESIGN.md says, but what's rendered):

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
- **If no URL is given and you're on main/master:** Ask the user for a URL.
- **If NO runtime detected** (no config files found): Use AskUserQuestion:

禁止做
- This only happens once. If `TEL_PROMPTED` is `yes`, skip this entirely.
- This only happens once. If `PROACTIVE_PROMPTED` is `yes`, skip this entirely.
- **User sovereignty.** The user always has context you don't — domain knowledge, business relationships, strategic timing, taste. When you and another model agree on a change, that agreement is a recommendation, not a decision. Present it. The user decides. Never say "the outside voice is right" and act. Say "the outside voice recommends X — do you want to proceed?"
- - Be direct about quality. "Well-designed" or "this is a mess." Don't dance around judgments.
- - **`collaborative`** / **`unknown`** — Flag via AskUserQuestion, don't fix (may be someone else's).
- - **Layer 1** (tried and true) — don't reinvent. **Layer 2** (new and popular) — scrutinize. **Layer 3** (first principles) — prize above all.
- Slug: lowercase hyphens, max 60 chars. Skip if exists. Max 3/session. File inline, don't stop.
- If you cannot determine the outcome, use "unknown". The local JSONL always logs. The
- C) Skip — don't set up testing right now
- First check: If CLAUDE.md already has a `## Testing` section → skip. Don't duplicate.
- MUST be saved to `~/.gstack/projects/$SLUG/designs/`, NEVER to `.context/`,
- 9. **Document incrementally.** Write each finding to the report as you find it. Don't batch.

### 提問方式
- **Final test:** does this sound like a real cross-functional builder who wants to help someone make something people want, ship it, and make it actually work?
- [AskUserQuestion Format]
- **ALWAYS follow this structure for every AskUserQuestion call:**
- 4. **Options:** Lettered options: `A) ... B) ... C) ...` — when an option involves effort, show both scales: `(human: ~X / CC: ~Y)`
- - Clear focal point? One primary CTA per view?
- - Eye flows naturally top-left to bottom-right?
- - Visual noise — competing elements fighting for attention?
- - Information density appropriate for content type?
- - Z-index clarity — nothing unexpectedly overlapping?
- - Above-the-fold content communicates purpose in 3 seconds?
- - Squint test: hierarchy still visible when blurred?
- - White space is intentional, not leftover?

### 審查維度
- [GSTACK REVIEW REPORT]
- **VERDICT:** NO REVIEWS YET — run \`/autoplan\` for full review pipeline, or individual reviews above.
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one
- [Phases 1-6: Design Audit Baseline]
- [Phase 3: Page-by-Page Visual Audit]
- For each page in scope:
- After the first navigation, check if the URL changed to a login-like path:
- If URL contains `/login`, `/signin`, `/auth`, or `/sso`: the site requires authentication. AskUserQuestion: "This site requires authentication. Want to import cookies from your browser? Run `/setup-browser-cookies` first if needed."
- **1. Visual Hierarchy & Composition** (8 items)
- - Clear focal point? One primary CTA per view?
- - Eye flows naturally top-left to bottom-right?
- [Phase 4: Interaction Flow Review]
- Walk 2-3 key user flows and evaluate the *feel*, not just the function:
- Evaluate:
- - **Response feel:** Does clicking feel responsive? Any delays or missing loading states?
- - **Transition quality:** Are transitions intentional or generic/absent?

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
- 適合在需要「以設計師視角檢查並修正 UI 一致性、節奏與互動品質的設計 QA 技能」的工作階段使用。
- 常見觸發語句：audit the design / visual QA / check if it looks good / design polish
- 也適合在使用者尚未明講，但上下文已顯示相同需求時主動建議使用。
- 常出現在審查、驗證、合併前檢查或上線後回看階段。

### 原文精華摘錄
> Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them
> Iteratively fixes issues in source code, committing each fix atomically and re-verifying with before/after screenshots
> For plan-mode design review (before implementation), use /plan-design-review
> Use when asked to "audit the design", "visual QA", "check if it looks good", or "design polish"
> Proactively suggest when the user mentions visual inconsistencies or wants to polish the look of a live site
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
> 1. **Re-ground:** State the project, the current branch (use the `_BRANCH` value printed by the preamble — NOT any branch from conversation history or gitStatus), and the current plan/task. (1-2 sentences)
> 2. **Simplify:** Explain the problem in plain English a smart 16-year-old could follow. No raw function names, no internal jargon, no implementation details. Use concrete examples and analogies. Say what it DOES, not what it's called.
> 3. **Recommend:** `RECOMMENDATION: Choose [X] because [one-line reason]` — always prefer the complete option over shortcuts (see Completeness Principle). Include `Completeness: X/10` for each option. Calibration: 10 = complete implementation (all edge cases...

### 和其他 skill 的潛在關聯
- qa（gstack） - 相似 - 共享領域：review；共享分類：審查型、流程型；共同關鍵詞：additional, after, asked, askuserquestion
- plan-design-review（gstack） - 相似 - 共享領域：design, review；共享分類：審查型、人格型、流程型；共同關鍵詞：after, asked, askuserquestion, audit
- qa-only（gstack） - 相似 - 共享領域：review；共享分類：審查型、流程型；共同關鍵詞：additional, asked, askuserquestion, boil
- design-consultation（gstack） - 相似 - 共享領域：design；共享分類：人格型、流程型；共同關鍵詞：asked, askuserquestion, boil, browse

### 分類標記
- [ ] 思考框架型
- [x] 審查型
- [ ] 工具程序型
- [x] 人格型
- [x] 流程型
- [ ] 元技能型
---
