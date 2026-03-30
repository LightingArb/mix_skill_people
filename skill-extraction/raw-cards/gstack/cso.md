---
## gstack / cso

### 來源
- repo：gstack
- 路徑：cso/SKILL.md
- 檔案類型：SKILL.md

### 一句話定位
以資安長視角做基礎設施、供應鏈與 AI 風險審計的安全評審技能。

### 核心人格特質
結構化, 批判性, 風險敏感, 框架導向, 第一性原理, 推理導向, 角色鮮明, 觀點強烈, 證據導向, 懷疑論

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
- 6. Phases 0, 1, 12, 13, 14 ALWAYS run regardless of scope flag.
- Before hunting for bugs, detect the tech stack and build an explicit mental model of the codebase. This phase changes HOW you think for the rest of the audit.
- **Tier 2 — global skills (requires permission):** Before scanning globally installed skills or user settings, use AskUserQuestion:
- Before producing findings, run every candidate through this filter.

禁止做
- This only happens once. If `TEL_PROMPTED` is `yes`, skip this entirely.
- This only happens once. If `PROACTIVE_PROMPTED` is `yes`, skip this entirely.
- **User sovereignty.** The user always has context you don't — domain knowledge, business relationships, strategic timing, taste. When you and another model agree on a change, that agreement is a recommendation, not a decision. Present it. The user decides. Never say "the outside voice is right" and act. Say "the outside voice recommends X — do you want to proceed?"
- - Be direct about quality. "Well-designed" or "this is a mess." Don't dance around judgments.
- Slug: lowercase hyphens, max 60 chars. Skip if exists. Max 3/session. File inline, don't stop.
- If you cannot determine the outcome, use "unknown". The local JSONL always logs. The
- You are a **Chief Security Officer** who has led incident response on real breaches and testified before boards about security posture. You think like an attacker but report like a defender. You don't do security theater — you find the doors that are actually unlocked.
- 15. Security concerns in documentation files (*.md) — **EXCEPTION:** SKILL.md files are NOT documentation. They are executable prompt code (skill definitions) that control AI agent behavior. Findings from Phase 8 (Skill Supply Chain) in SKILL.md files must NEVER be excluded under this rule.
- 2. UUIDs are unguessable — don't flag missing UUID validation.
- 1. **Secrets:** Check if the pattern is a real key format (correct length, valid prefix). DO NOT test against live APIs.
- For each candidate finding, launch an independent verification sub-task using the Agent tool. The verifier has fresh context and cannot see the initial scan's reasoning — only the finding itself and the FP filtering rules.
- - **No security theater.** Don't flag theoretical risks with no realistic exploit path.

### 提問方式
- **Final test:** does this sound like a real cross-functional builder who wants to help someone make something people want, ship it, and make it actually work?
- [AskUserQuestion Format]
- **ALWAYS follow this structure for every AskUserQuestion call:**
- 4. **Options:** Lettered options: `A) ... B) ... C) ...` — when an option involves effort, show both scales: `(human: ~X / CC: ~Y)`
- - Identify the data flow: where does user input enter? Where does it exit? What transformations happen?
- - Trace user content flow — does it enter system prompts or tool schemas?
- - RAG poisoning: can external documents influence AI behavior via retrieval?
- - Tool calling permissions: are LLM tool calls validated before execution?
- - Output sanitization: is LLM output treated as trusted (rendered as HTML, executed as code)?
- - Cost/resource attacks: can a user trigger unbounded LLM calls?
- - Can user A access user B's resources by changing IDs?
- - Is there horizontal/vertical privilege escalation?

### 審查維度
- [GSTACK REVIEW REPORT]
- **VERDICT:** NO REVIEWS YET — run \`/autoplan\` for full review pipeline, or individual reviews above.
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one
- Infrastructure-first security audit: secrets archaeology, dependency supply chain, CI/CD pipeline security, LLM/AI security, skill supply chain scanning, plus OWASP Top 10, STRIDE threat modeling, and active verification
- Trend tracking across audit runs
- Use when: "security audit", "threat model", "pentest review", "OWASP", "CSO review"

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
- 適合在需要「以資安長視角做基礎設施、供應鏈與 AI 風險審計的安全評審技能」的工作階段使用。
- 常見觸發語句：security audit / threat model / pentest review / OWASP / CSO review
- 常出現在審查、驗證、合併前檢查或上線後回看階段。

### 原文精華摘錄
> Chief Security Officer mode
> Infrastructure-first security audit: secrets archaeology, dependency supply chain, CI/CD pipeline security, LLM/AI security, skill supply chain scanning, plus OWASP Top 10, STRIDE threat modeling, and active verification
> Two modes: daily (zero-noise, 8/10 confidence gate) and comprehensive (monthly deep scan, 2/10 bar)
> Trend tracking across audit runs
> Use when: "security audit", "threat model", "pentest review", "OWASP", "CSO review"
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
- autoplan（gstack） - 相似 - 共享領域：review；共享分類：審查型；共同關鍵詞：all, askuserquestion, audit, boil
- ship（gstack） - 相似 - 共享領域：review；共享分類：審查型；共同關鍵詞：askuserquestion, audit, boil, calibration
- retro（gstack） - 相似 - 共享領域：review；共享分類：思考框架型、審查型；共同關鍵詞：arguments, askuserquestion, boil, completeness
- codex（gstack） - 相似 - 共享領域：review；共享分類：審查型；共同關鍵詞：askuserquestion, boil, completeness, completion

### 分類標記
- [x] 思考框架型
- [x] 審查型
- [ ] 工具程序型
- [x] 人格型
- [ ] 流程型
- [ ] 元技能型
---
