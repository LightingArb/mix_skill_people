# Skill 人格抽取分析報告

> 目的：為 Remy 的 AI 工作流提供決策依據，從 49 張 raw card 中辨識真正有價值的思維資產，並指出整合方向。

---

## 一、問題診斷

你目前的痛點：

1. **效率低**：AI 每次都要去 repo 動態載入 skill，讀取+思考吃掉大量 context
2. **失控**：AI 自作主張載入不需要的 skill，且無法退出
3. **記憶爆炸**：skill 之間有大量重複的 preamble/boilerplate，灌進去後記憶就滿了

**根因分析**：

gstack 的 34 個 skill 裡，每一個都包含約 40-60% 的**共用 boilerplate**：
- Completeness Principle（Boil the Lake）
- AskUserQuestion 格式
- Voice/Tone 定義
- Telemetry prompt
- Plan Status Footer
- GSTACK REVIEW REPORT 模板
- Contributor Mode / Eureka logging

這意味著如果 AI 同時載入 3 個 gstack skill，有近 50% 的 token 是重複內容。這就是你記憶爆炸的主因。

superpowers 的 15 個 skill 相對精簡，每個約 60-100 行，重複度低，但它的問題是 `using-superpowers` 強制「1% 可能性就必須載入」，導致過度觸發。

---

## 二、價值分層

### Tier S — 核心思維資產（建議永遠可用）

這些 skill 提供的不是工具操作，而是**改變 AI 思考品質**的框架：

| # | 原始 skill | 來源 | 核心價值 |
|---|-----------|------|---------|
| 1 | office-hours | gstack | YC 式產品診斷：6 個逼問、status quo 分析、窄切入點、觀察優先 |
| 2 | plan-ceo-review | gstack | CEO 思維模式：4 種 scope 姿態、Bezos 門分類、前提挑戰、10 星產品 |
| 3 | plan-eng-review | gstack | 工程主管思維：狀態診斷、爆炸半徑、boring by default、可逆偏好 |
| 4 | investigate | gstack | 系統化除錯：Iron Law（無根因不修）、3-strike rule、假設驗證循環 |
| 5 | verification-before-completion | superpowers | 完成前驗證：Evidence before claims、Iron Law |
| 6 | brainstorming | superpowers | 前置釐清：反「太簡單不需要設計」、scope 拆解、一次一問 |

### Tier A — 高價值審查/設計資產（建議按需載入）

| # | 原始 skill | 來源 | 核心價值 |
|---|-----------|------|---------|
| 7 | plan-design-review | gstack | 設計審查 6 維度、hierarchy/empty state/edge case paranoia |
| 8 | cso | gstack | 資安審計：OWASP+STRIDE、AI/LLM 安全、供應鏈掃描 |
| 9 | review | gstack | PR review：scope creep 偵測、diff vs plan 對照、邊界條件追蹤 |
| 10 | systematic-debugging | superpowers | 4 階段除錯（和 investigate 互補，更偏 step-by-step） |
| 11 | test-driven-development | superpowers | TDD Iron Law、RED-GREEN-REFACTOR |
| 12 | autoplan | gstack | 6 Decision Principles、Decision Classification（Mechanical vs Taste） |
| 13 | receiving-code-review | superpowers | 反表演式同意、先驗證再回應 |
| 14 | retro | gstack | 工程回顧：commit 分析、品質趨勢、team pattern |

### Tier B — 工具/操作型（完整保留供你自選）

| # | 原始 skill | 來源 | 性質 |
|---|-----------|------|------|
| 15 | design-consultation | gstack | 設計系統建立流程（需要 browse 工具） |
| 16 | design-shotgun | gstack | 多變體設計探索（需要 API） |
| 17 | design-review | gstack | 視覺 QA（需要 headless browser） |
| 18 | ship | gstack | 出貨流程（git+test+PR） |
| 19 | land-and-deploy | gstack | 部署流程 |
| 20 | qa / qa-only | gstack | 網站 QA |
| 21 | canary | gstack | 部署後監控 |
| 22 | benchmark | gstack | 效能基線 |
| 23 | browse | gstack | headless browser 操作 |
| 24 | learn | gstack | 知識累積管理 |
| 25 | codex | gstack | OpenAI Codex 整合 |
| 26 | writing-plans | superpowers | 計畫拆解（和 plan-eng-review 互補） |
| 27 | executing-plans | superpowers | 計畫執行 |
| 28 | dispatching-parallel-agents | superpowers | 平行 agent 調度 |
| 29 | subagent-driven-development | superpowers | 子代理開發 |
| 30 | using-git-worktrees | superpowers | git worktree 管理 |
| 31 | finishing-a-development-branch | superpowers | 分支收尾 |
| 32 | requesting-code-review | superpowers | 請求 review |
| 33 | writing-skills | superpowers | 技能文件設計 |

### Tier C — 基礎設施/可跳過

| # | 原始 skill | 理由 |
|---|-----------|------|
| 34-38 | careful/freeze/unfreeze/guard | 安全護欄，gstack 專用 |
| 39-41 | setup-deploy/setup-browser-cookies/connect-chrome | 工具設定 |
| 42-43 | gstack-upgrade/document-release | gstack 維護 |
| 44-45 | using-superpowers | 過度觸發的元控制，你自己做路由就不需要 |
| 46-49 | 各 repo 的 ROOT README/CLAUDE/AGENTS | 安裝說明，無思維價值 |

---

## 三、跨 repo 重疊與互補分析

### 高度重疊（可合併）

| 功能域 | gstack | superpowers | 合併策略 |
|--------|--------|-------------|---------|
| 除錯 | investigate | systematic-debugging | gstack 的更完整（有 pattern analysis + external search），superpowers 的更簡潔。建議以 gstack 為主體，補入 superpowers 的 Red Flags checklist |
| 完成驗證 | ship（裡的驗證段） | verification-before-completion | superpowers 更乾淨獨立，直接用 |
| 前置規劃 | office-hours | brainstorming | gstack 偏產品策略，superpowers 偏工程設計。**不合併**，保留兩個視角 |
| 計畫審查 | plan-ceo/design/eng-review | writing-plans | 完全互補，不重疊 |

### 共用模組（需抽離為獨立區塊）

從所有 gstack skill 中反覆出現的共用元素，建議抽成獨立模組一次定義：

1. **Completeness Principle（Boil the Lake）**：出現在所有 gstack skill
2. **6 Decision Principles**：出現在 autoplan、plan-*-review
3. **AskUserQuestion 格式**：Re-ground → Simplify → Recommend → Options
4. **Voice/Tone**：direct, concrete, sharp, builder-to-builder
5. **Engineering Preferences**：DRY、well-tested、engineered-enough、explicit > clever
6. **Knowledge Layers**：Layer 1（tried and true）→ Layer 2（new and popular）→ Layer 3（first principles）
7. **User Sovereignty**：user always has context you don't

---

## 四、建議整合架構

```
你的整合 skill 文件結構：

skill-persona.md
├── §0 元控制（取代 using-superpowers + gstack preamble）
│   ├── 路由規則：什麼場景載入什麼模組
│   ├── 禁止自動載入規則
│   └── user sovereignty 原則
│
├── §1 共用基底（一次定義，全局生效）
│   ├── Completeness Principle
│   ├── 6 Decision Principles
│   ├── Engineering Preferences
│   ├── Knowledge Layers (L1/L2/L3)
│   ├── AskUserQuestion 格式
│   └── Voice/Tone
│
├── §2 思考人格（Tier S，永遠可用）
│   ├── 產品診斷（from office-hours）
│   ├── CEO 思維（from plan-ceo-review）
│   ├── 工程主管思維（from plan-eng-review）
│   ├── 系統化除錯（from investigate + systematic-debugging）
│   ├── 完成驗證（from verification-before-completion）
│   └── 前置釐清（from brainstorming）
│
├── §3 審查模組（Tier A，按需啟用）
│   ├── 設計審查（from plan-design-review）
│   ├── 資安審計（from cso）
│   ├── PR Review（from review）
│   ├── TDD（from test-driven-development）
│   ├── 決策分類（from autoplan 的 decision classification）
│   ├── 反表演式 review（from receiving-code-review）
│   └── 工程回顧（from retro）
│
└── §4 操作參考（Tier B，索引式，需要時再查）
    └── （保留原始卡片作為獨立參考檔）
```

---

## 五、預期效益

| 指標 | 現狀 | 整合後 |
|------|------|--------|
| 載入 3 個 gstack skill 的 token | ~15,000-20,000（含大量重複） | ~5,000-8,000（共用基底只算一次） |
| AI 自主載入不需要的 skill | 經常發生 | 由 §0 路由規則控制，你決定 |
| 思維品質 | 取決於 AI 碰巧載入了哪個 | Tier S 永遠在，品質一致 |
| 找對工具的速度 | AI 要翻 repo 思考 | 查表式，直接到位 |

---

## 六、下一步

1. **確認 Tier 分層**：你看完有沒有要調整的？哪些你覺得分錯了？
2. **確認整合架構**：§0-§4 的結構你同意嗎？
3. **開始寫 skill-persona.md**：從 §1 共用基底開始，逐段產出

你要我直接開始寫，還是先調整分層？
