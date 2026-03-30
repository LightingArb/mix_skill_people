# mix_skill_people

這個專案是一次針對 AI coding skill system 的系統性抽取工程。

它把兩個上游 skill repo:

- `garrytan/gstack`
- `obra/superpowers`

裡面的 skill 文件完整拉下來、逐份閱讀、逐份抽卡，最後產出一套可檢索、可分析、可再加工的 raw dataset，目的是把原本分散在大量 `SKILL.md`、`CLAUDE.md`、`AGENTS.md`、`README.md` 裡的「人格設定、思考框架、行為規則、審查維度、提問方式」抽出來，變成可以直接被人類或 AI 使用的結構化資產。

這不是原始 skill repo 的 fork，也不是新的 skill runtime。

這個 repo 的核心價值是：

1. 把技能文件從「只能動態載入的 prompt 資料」變成「可閱讀、可分類、可比較、可重組的知識庫」。
2. 把技能之間隱含的人格與方法論從原文中抽出來，降低之後整合 skill system 的成本。
3. 為後續建立單一整合版 persona / meta-skill 提供乾淨的中間層。

## 這個專案在做什麼

簡單說，這個專案做了三件事：

1. 從 `gstack` 和 `superpowers` 兩個 repo 抓取所有指定文件。
2. 依照固定規格，對每一份文件生成一張 extraction card。
3. 再把所有卡片整理成總索引、分類彙整與分析報告，讓後續可以做整合與去重。

這裡保存的不是簡單摘要，而是偏向研究用的 raw data。

也就是說，這個 repo 的重點不是「幫你快速看懂一個 skill」，而是「保留足夠完整的抽取結果，讓你之後可以判斷哪些 skill 的人格值得保留、哪些 boilerplate 應該去重、哪些框架應該提升成全域規則」。

## 為什麼要這樣做

這個專案要處理的是一個很實際的問題：

現成的 skill repo 雖然強，但它們通常是為「動態載入」而設計，不是為「低成本整合」而設計。

直接拿來當日常工作流的問題通常有幾個：

- skill 之間有大量重複 preamble、voice、telemetry、格式規則，context 很快被吃滿
- AI 需要反覆去 repo 裡找 skill，載入速度慢，還會增加決策噪音
- 某些 skill 會過度觸發或堆疊，讓 AI 行為失控
- 思維框架、角色人格、操作流程、工具指令全部混在同一份文件裡，不容易拆解重用
- 你很難知道「真正有價值的是哪一部分」，是思考方式、審查方式、還是純工具步驟

所以這個 repo 不是在「再做一套 skills」，而是在做 skill system 的逆向拆解。

先抽乾淨，再分析，再整合。

## 專案目的

這個 repo 的目的是把上游 skill repo 裡最重要的資產，從文件型 prompt 中抽離出來，讓它們可以被更穩定地使用。

具體目標包括：

- 找出每個 skill 對 AI 行為的真正影響
- 區分哪些內容是人格、哪些是思考框架、哪些是審查維度、哪些只是工具流程
- 建立一份完整、不漏項、不先做價值判斷的 raw dataset
- 為後續去重、瘦身、合併與 persona 整合提供可靠基礎
- 最終降低 AI 在實際工作時的 context 浪費與 skill 路由成本

## 最後產生了什麼

目前 repo 內的主要產出如下：

- `49` 張技能抽取卡片
- `gstack 34` 份來源文件對應卡片
- `superpowers 15` 份來源文件對應卡片
- `1` 份總索引
- `1` 份分類彙整
- `1` 份分析報告
- `1` 份整合版 `skill-persona.md`
- `1` 支可重跑的產生器腳本 `generate_skill_extraction.py`

也就是說，這個 repo 既保存了：

- 上游來源
- 中間抽取資料
- 研究分析
- 後續整合方向

## 這個專案解決了什麼問題

### 1. 解決 skill 文件難以比較的問題

原始 `SKILL.md` 通常很長，而且同時包含：

- 使用時機
- 語氣設定
- 流程要求
- tool hooks
- output format
- 共同 boilerplate

這使得你很難橫向比較兩個 skill 到底差在哪裡。

這個 repo 把它們統一抽成相同欄位的卡片後，就可以很直接地比較：

- 哪個 skill 比較偏人格型
- 哪個 skill 比較偏審查型
- 哪個 skill 本質上只是在包工具流程
- 哪些 skill 的思維框架高度重疊

### 2. 解決 context 爆炸的問題

當 AI 每次都要重新去讀外部 repo 的 skill 檔，token 成本很高。

尤其像 `gstack` 這類 skill，大量重複的 preamble、voice、telemetry、review footer 會重複灌進上下文。

先抽成 raw card，再整理出共用基底與高價值思維模組，是控制 context 成本的前置工程。

### 3. 解決 skill routing 失控的問題

某些 skill system 會要求「只要有 1% 可能相關就要載入」。

這在理論上很完整，但實務上容易造成：

- 過度載入
- 過度提示
- 無法退出 skill
- 任務被 skill workflow 綁死

這個 repo 的抽取與分析工作，讓後續能把「真正該永遠生效的部分」和「只該按需啟用的部分」拆開。

### 4. 解決後續整合無從下手的問題

如果沒有抽取中間層，你只能直接改寫原始 skill。

那會很難判斷：

- 你是在保留精華，還是在不小心刪掉有效規則
- 你是在去重，還是在破壞 skill 的原始人格
- 哪些內容可以升格為全域規則
- 哪些內容應該退回成查詢式 reference

這個 repo 的存在，就是為了把這一步做成可追蹤、可回溯、可審核。

## 方法與流程

本專案採用明確規格驅動的抽取流程，規格見 [skill-extraction-spec.md](./skill-extraction-spec.md)。

高層流程如下：

1. clone 兩個來源 repo
2. 掃描所有符合條件的文件
3. 完整讀取每一份文件
4. 為每份文件生成 extraction card
5. 生成總索引
6. 生成分類彙整
7. 再基於 raw data 做分析與整合方向建議

這裡刻意先做「完整抽取」，不先做「合併、瘦身、刪減」。

原因很簡單：

如果太早整合，你很容易把本來有價值但不顯眼的思維資產一起抹掉。

## Repo 結構

```text
.
├── README.md
├── generate_skill_extraction.py
├── skill-extraction-spec.md
├── skill-extraction-analysis.md
├── skill-persona.md
└── skill-extraction/
    ├── repos/
    │   ├── gstack/          # 上游來源，submodule
    │   └── superpowers/     # 上游來源，submodule
    ├── raw-cards/
    │   ├── gstack/          # 每份來源文件一張卡片
    │   └── superpowers/
    ├── 00_總索引.md
    ├── 01_分類彙整.md
    └── raw-cards.zip
```

### 各檔案的角色

- `generate_skill_extraction.py`
  - 抽取流程的產生器腳本，負責掃描來源 repo、整理內容、輸出卡片與索引
- `skill-extraction-spec.md`
  - 本次抽取工作的規格與驗收標準
- `skill-extraction-analysis.md`
  - 對 raw data 的二次分析，說明哪些技能真正有價值、哪些可整合
- `skill-persona.md`
  - 基於抽取與分析後形成的整合式 persona / framework 草案
- `skill-extraction/raw-cards/`
  - 研究用核心資料集，每張卡對應一份來源文件
- `skill-extraction/00_總索引.md`
  - 全部卡片的統計、清單與跨 repo 關聯矩陣
- `skill-extraction/01_分類彙整.md`
  - 依分類標記重新整理的總表

## 這個 repo 適合誰

如果你正在做以下事情，這個 repo 會有價值：

- 你想把多個 AI skill repo 整合成單一工作人格
- 你想研究不同 skill system 的 prompt engineering 方法論
- 你想知道哪些 skill 真正改變 AI 思考品質，哪些只是操作流程
- 你想降低 AI 動態載入 skill 時的 token 浪費
- 你想建立自己的 meta-skill / persona system，但不想從零開始整理

## 如何使用這個 repo

### 只想看結果

直接讀這幾份檔案：

- [skill-extraction/00_總索引.md](./skill-extraction/00_總索引.md)
- [skill-extraction/01_分類彙整.md](./skill-extraction/01_分類彙整.md)
- [skill-extraction-analysis.md](./skill-extraction-analysis.md)
- [skill-persona.md](./skill-persona.md)

### 想查某個 skill 的人格與規則

到下列目錄查對應卡片：

- [skill-extraction/raw-cards/gstack](./skill-extraction/raw-cards/gstack)
- [skill-extraction/raw-cards/superpowers](./skill-extraction/raw-cards/superpowers)

### 想重跑產生流程

因為 `repos/` 是 submodule，建議先完整取回來源：

```bash
git clone --recurse-submodules https://github.com/LightingArb/mix_skill_people
cd mix_skill_people
python generate_skill_extraction.py
```

如果是已經 clone 下來的工作目錄：

```bash
git submodule update --init --recursive
python generate_skill_extraction.py
```

## 目前範圍與非目標

### 目前範圍

- 完整抽取 `gstack` 與 `superpowers` 的指定 skill 文件
- 生成人格卡片、總索引、分類彙整
- 產出分析報告與整合方向
- 形成一份初版整合 persona 文件

### 非目標

- 不負責維護上游 repo
- 不提供新的 runtime / loader
- 不保證當前關聯矩陣已是最終最佳版本
- 不在這一輪直接做最終的 skill merge
- 不把所有 raw card 直接視為 production-ready prompt

換句話說，這個 repo 是研究與整合前置層，不是最終成品層。

## 設計原則

這個 repo 背後的原則是：

- **先完整，再整合**
- **先保留 raw data，再做價值判斷**
- **先拆出思維資產，再決定工具怎麼接**
- **把 prompt 從黑盒變成可審視的知識結構**

如果你要做的是長期可維護的 AI workflow，這一步通常逃不掉。

因為真正難的從來不是「寫一份 skill」，而是判斷：

- 哪些規則應該永遠生效
- 哪些規則只該按需觸發
- 哪些人格是核心資產
- 哪些 boilerplate 只是噪音

這個專案就是為了回答這些問題而存在。

## 資料來源

本 repo 目前使用以下上游來源：

- `https://github.com/garrytan/gstack`
- `https://github.com/obra/superpowers`

它們在本 repo 中以 git submodule 形式保留，方便回溯來源版本與重新生成結果。

## 最後一句話

這個專案不是在收集 skill 文件。

它是在把 skill 文件裡真正有價值的「人格、方法論、決策框架與行為約束」拆出來，讓後續可以建立一個更輕、更穩、更可控的 AI 工作人格系統。
