---
## gstack / browse

### 來源
- repo：gstack
- 路徑：browse/SKILL.md
- 檔案類型：SKILL.md

### 一句話定位
以無頭瀏覽器快速操作頁面、驗證狀態與蒐集 QA 證據的工具技能。

### 核心人格特質
務實, 操作導向, 證據導向, 懷疑論

### 核心思考框架
- [Core QA Patterns]
- ### 1. Verify a page loads correctly
- ### 2. Test a user flow
- ### 3. Verify an action worked
- ### 4. Visual evidence for bug reports
- ### 5. Find all clickable elements (including non-ARIA)
- ### 6. Assert element states

### 核心行為規則
必須做
- auto-invoke skills based on conversation context. Only run skills the user explicitly
- If `LAKE_INTRO` is `no`: Before continuing, introduce the Completeness Principle.
- Only run `open` if the user says yes. Always run `touch` to mark as seen. This only happens once.
- ask the user about telemetry. Use AskUserQuestion:
- ask the user about proactive behavior. Use AskUserQuestion:
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This command writes telemetry to
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one

禁止做
- This only happens once. If `TEL_PROMPTED` is `yes`, skip this entirely.
- This only happens once. If `PROACTIVE_PROMPTED` is `yes`, skip this entirely.
- The user always has context you don't. Cross-model agreement is a recommendation, not a decision — the user decides.
- Slug: lowercase hyphens, max 60 chars. Skip if exists. Max 3/session. File inline, don't stop.
- If you cannot determine the outcome, use "unknown". The local JSONL always logs. The

### 提問方式
無明確提問模板

### 審查維度
非審查型

### 輸出格式要求
- [Plan Status Footer]
- When you are in plan mode and about to call ExitPlanMode:
- 1. Check if the plan file already has a `## GSTACK REVIEW REPORT` section.
- 2. If it DOES — skip (a review skill already wrote a richer report).
- 3. If it does NOT — run this command:
- Then write a `## GSTACK REVIEW REPORT` section to the end of the plan file:
- - If the output contains review entries (JSONL lines before `---CONFIG---`): format the
- [GSTACK REVIEW REPORT]
- **VERDICT:** NO REVIEWS YET — run \`/autoplan\` for full review pipeline, or individual reviews above.
- **PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one

### 適用場景
- 適合在需要「以無頭瀏覽器快速操作頁面、驗證狀態與蒐集 QA 證據的工具技能」的工作階段使用。
- 常見觸發語句：open in browser / test the
site / take a screenshot / dogfood this
- 常出現在審查、驗證、合併前檢查或上線後回看階段。

### 原文精華摘錄
> Fast headless browser for QA testing and site dogfooding
> Navigate any URL, interact with elements, verify page state, diff before/after actions, take annotated screenshots, check responsive layouts, test forms and uploads, handle dialogs, and assert element states
> ~100ms per command
> Use when you need to test a feature, verify a deployment, dogfood a user flow, or file a bug with evidence
> Use when asked to "open in browser", "test the site", "take a screenshot", or "dogfood this"
> Preamble (run first)
> types (e.g., /qa, /ship). If you would have auto-invoked a skill, instead briefly say:
> Then offer to open the essay in their default browser:
> ask the user about telemetry. Use AskUserQuestion:
> Options:
> Voice
> **Tone:** direct, concrete, sharp, never corporate, never academic. Sound like a builder, not a consultant. Name the file, the function, the command. No filler, no throat-clearing.
> **Writing rules:** No em dashes (use commas, periods, "..."). No AI vocabulary (delve, crucial, robust, comprehensive, nuanced, etc.). Short paragraphs. End with what to do.
> Contributor Mode
> **File only:** gstack tooling bugs where the input was reasonable but gstack failed. **Skip:** user app bugs, network errors, auth failures on user's site.
> **To file:** write `~/.gstack/contributor-logs/{slug}.md`:

### 和其他 skill 的潛在關聯
- SKILL（gstack） - 相似 - 共享領域：browser；共享分類：工具程序型；共同關鍵詞：after, annotated, asked, browse
- qa（gstack） - 相似 - 共享領域：browser；共享分類：工具程序型；共同關鍵詞：after, asked, browse, command
- qa-only（gstack） - 相似 - 共享領域：browser；共同關鍵詞：asked, browse, bug, command
- setup-browser-cookies（gstack） - 相似 - 共享領域：browser；共享分類：工具程序型；共同關鍵詞：asked, browse, browser, command

### 分類標記
- [ ] 思考框架型
- [ ] 審查型
- [x] 工具程序型
- [ ] 人格型
- [ ] 流程型
- [ ] 元技能型
---
