from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(r"c:\Users\admin\Desktop\skill")
EXTRACTION_ROOT = ROOT / "skill-extraction"
REPOS_ROOT = EXTRACTION_ROOT / "repos"
RAW_CARDS_ROOT = EXTRACTION_ROOT / "raw-cards"

TARGET_FILE_NAMES = {"SKILL.md", "CLAUDE.md", "AGENTS.md"}
ROOT_README = "README.md"

COMMON_STOPWORDS = {
    "a",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "before",
    "by",
    "can",
    "check",
    "code",
    "create",
    "default",
    "do",
    "each",
    "for",
    "from",
    "get",
    "how",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "mode",
    "not",
    "of",
    "on",
    "or",
    "out",
    "run",
    "skill",
    "skills",
    "that",
    "the",
    "their",
    "them",
    "then",
    "this",
    "to",
    "use",
    "user",
    "using",
    "when",
    "with",
    "you",
    "your",
}

SIMILARITY_STOPWORDS = COMMON_STOPWORDS | {
    "agents",
    "claude",
    "complete",
    "components",
    "debugging",
    "design",
    "development",
    "implementation",
    "meta",
    "parallel",
    "planning",
    "readme",
    "review",
    "session",
    "shipping",
    "superpowers",
    "workflow",
}

FRAMEWORK_HEADING_KEYWORDS = (
    "process",
    "phase",
    "phases",
    "philosophy",
    "principle",
    "principles",
    "pattern",
    "patterns",
    "workflow",
    "workflows",
    "checklist",
    "hierarchy",
    "decision",
    "decisions",
    "modes",
    "flow",
    "guide",
    "overview",
    "iron law",
    "review sections",
    "implementation order",
    "mapping",
)

QUESTION_HEADING_KEYWORDS = (
    "askuserquestion",
    "question",
    "questions",
    "follow-up",
    "forcing questions",
)

REVIEW_HEADING_KEYWORDS = (
    "review",
    "audit",
    "rubric",
    "checklist",
    "items",
    "sections",
    "dimension",
    "dimensions",
    "score",
    "coverage",
    "health",
)

FORMAT_HEADING_KEYWORDS = (
    "required outputs",
    "output",
    "format",
    "formatting",
    "report",
    "dashboard",
    "footer",
    "template",
    "summary",
)

DOMAIN_KEYWORDS = {
    "design": [
        "design",
        "designer",
        "ui",
        "ux",
        "visual",
        "typography",
        "layout",
        "motion",
        "aesthetic",
    ],
    "review": [
        "review",
        "audit",
        "qa",
        "checklist",
        "rubric",
        "score",
        "verify",
        "verification",
    ],
    "debugging": [
        "debug",
        "bug",
        "failure",
        "root cause",
        "unexpected behavior",
        "hypothesis",
        "trace",
    ],
    "shipping": [
        "ship",
        "deploy",
        "release",
        "merge",
        "branch",
        "pr",
        "pull request",
        "changelog",
    ],
    "planning": [
        "plan",
        "scope",
        "requirements",
        "brainstorm",
        "architecture",
        "founder",
        "ceo",
    ],
    "safety": [
        "safety",
        "careful",
        "freeze",
        "guard",
        "destructive",
        "security",
        "risk",
    ],
    "browser": [
        "browse",
        "browser",
        "chrome",
        "cookie",
        "screenshot",
        "page",
        "dialog",
        "headless",
    ],
    "meta": [
        "skill",
        "skills",
        "agents",
        "claude",
        "superpowers",
    ],
    "parallel": [
        "parallel",
        "subagent",
        "worktree",
        "independent tasks",
    ],
    "learning": [
        "learn",
        "learnings",
        "retro",
        "history",
        "trend",
        "telemetry",
    ],
    "performance": [
        "performance",
        "benchmark",
        "core web vitals",
        "regression",
        "page load",
        "canary",
    ],
    "testing": [
        "test",
        "tests",
        "coverage",
        "tdd",
        "red-green-refactor",
        "passing",
    ],
}

ONE_LINERS = {
    ("gstack", "AGENTS.md"): "gstack 倉庫內的技能總覽、建置命令與協作慣例說明。",
    ("gstack", "CLAUDE.md"): "gstack 倉庫的工程規範、文件生成與提交流程總指引。",
    ("gstack", "README.md"): "gstack 的安裝、工作流與核心理念入口文件。",
    ("gstack", "SKILL.md"): "用無頭瀏覽器進行網站 QA、互動驗證與證據擷取的基礎技能。",
    ("gstack", "autoplan/SKILL.md"): "自動串接 CEO、設計與工程評審，按原則連續審核方案的總控技能。",
    ("gstack", "benchmark/SKILL.md"): "以瀏覽守護程序建立與比較效能基線的性能檢測技能。",
    ("gstack", "browse/SKILL.md"): "以無頭瀏覽器快速操作頁面、驗證狀態與蒐集 QA 證據的工具技能。",
    ("gstack", "canary/SKILL.md"): "在部署後持續監控線上站點錯誤、效能與畫面異常的金絲雀檢查技能。",
    ("gstack", "careful/SKILL.md"): "為破壞性命令加上事前警告與人工覆核的安全護欄技能。",
    ("gstack", "codex/SKILL.md"): "把 OpenAI Codex 以 review、challenge、consult 三種模式接入工作流的包裝技能。",
    ("gstack", "connect-chrome/SKILL.md"): "連接可視化的真實 Chrome 與側邊欄，讓使用者即時觀看瀏覽操作。",
    ("gstack", "cso/SKILL.md"): "以資安長視角做基礎設施、供應鏈與 AI 風險審計的安全評審技能。",
    ("gstack", "design-consultation/SKILL.md"): "先理解產品再研究競品並提出完整設計系統方案的設計顧問技能。",
    ("gstack", "design-review/SKILL.md"): "以設計師視角檢查並修正 UI 一致性、節奏與互動品質的設計 QA 技能。",
    ("gstack", "design-shotgun/SKILL.md"): "一次產生多個設計變體、比較並收斂偏好的設計探索技能。",
    ("gstack", "document-release/SKILL.md"): "在發版後同步更新 README、架構與變更記錄等文件的文件收尾技能。",
    ("gstack", "freeze/SKILL.md"): "把本次會話的可編輯範圍鎖定在指定目錄的編輯邊界技能。",
    ("gstack", "gstack-upgrade/SKILL.md"): "將 gstack 升級到最新版本並處理升級提示的維護技能。",
    ("gstack", "guard/SKILL.md"): "同時啟用破壞性命令警告與目錄凍結的全量安全模式技能。",
    ("gstack", "investigate/SKILL.md"): "以根因調查、模式分析、假設驗證到實作的流程來系統化除錯。",
    ("gstack", "land-and-deploy/SKILL.md"): "接手 PR 合併、等待部署並做生產環境驗證的落地部署技能。",
    ("gstack", "learn/SKILL.md"): "管理專案長期 learnings，支援查詢、修剪與匯出的知識累積技能。",
    ("gstack", "office-hours/SKILL.md"): "用 YC office hours 與 design partner 心法逼出真需求與更強產品方向的策略技能。",
    ("gstack", "plan-ceo-review/SKILL.md"): "用 CEO 或創辦人視角重新審視計畫範圍、願景與 10 星產品機會。",
    ("gstack", "plan-design-review/SKILL.md"): "從設計師角度逐維度評估計畫，指出把體驗做成 10 分的方法。",
    ("gstack", "plan-eng-review/SKILL.md"): "以工程主管視角鎖定架構、資料流、邊界條件與測試覆蓋的計畫評審技能。",
    ("gstack", "qa/SKILL.md"): "系統化測試網站後直接修 bug、逐項驗證並提交原子修復的 QA 技能。",
    ("gstack", "qa-only/SKILL.md"): "只做網站 QA 測試與結構化報告、不直接改碼的報告型 QA 技能。",
    ("gstack", "retro/SKILL.md"): "分析提交歷史、工作模式與品質指標，形成週期性工程 retrospective。",
    ("gstack", "review/SKILL.md"): "在合併前對 diff 做結構性風險審查並盡可能先修問題的 PR review 技能。",
    ("gstack", "setup-browser-cookies/SKILL.md"): "把真實 Chromium 的 cookies 匯入 headless 瀏覽 session 的登入前置技能。",
    ("gstack", "setup-deploy/SKILL.md"): "偵測部署平台與健康檢查資訊，為 land-and-deploy 建立部署設定。",
    ("gstack", "ship/SKILL.md"): "從合併 base、跑測試、更新版本到推分支建 PR 的完整出貨技能。",
    ("gstack", "unfreeze/SKILL.md"): "解除 freeze 設定，重新允許跨目錄編輯。",
    ("superpowers", "README.md"): "superpowers 的安裝、基本工作流、哲學與技能總覽入口。",
    ("superpowers", "skills/brainstorming/SKILL.md"): "在任何創作或功能實作前先釐清意圖、需求與設計的前置腦暴技能。",
    ("superpowers", "skills/dispatching-parallel-agents/SKILL.md"): "把彼此獨立的任務拆給多個 agent 並行處理的調度技能。",
    ("superpowers", "skills/executing-plans/SKILL.md"): "依既有實作計畫逐步施工、檢查與回報進度的執行技能。",
    ("superpowers", "skills/finishing-a-development-branch/SKILL.md"): "在開發完成後結構化決定合併、提 PR 或清理分支的收尾技能。",
    ("superpowers", "skills/receiving-code-review/SKILL.md"): "收到 code review 後先驗證、再回應與實作，而不是表演式同意的技能。",
    ("superpowers", "skills/requesting-code-review/SKILL.md"): "在完成主要工作後有條理地請求 code review 的協作技能。",
    ("superpowers", "skills/subagent-driven-development/SKILL.md"): "在同一會話內用子代理執行獨立實作子任務的開發技能。",
    ("superpowers", "skills/systematic-debugging/SKILL.md"): "遇到 bug 時先找根因、再提修復方案的系統化除錯技能。",
    ("superpowers", "skills/test-driven-development/SKILL.md"): "在寫實作前先寫失敗測試，再按 red-green-refactor 前進的 TDD 技能。",
    ("superpowers", "skills/using-git-worktrees/SKILL.md"): "用 git worktree 建立隔離工作目錄，安全展開多線開發。",
    ("superpowers", "skills/using-superpowers/SKILL.md"): "在任何對話開始時先找對 skill 並嚴格遵守技能優先級的總入口技能。",
    ("superpowers", "skills/verification-before-completion/SKILL.md"): "在宣稱完成前先跑驗證並以證據支撐結論的收尾技能。",
    ("superpowers", "skills/writing-plans/SKILL.md"): "在動手前先把多步驟工作拆成可執行計畫的規劃技能。",
    ("superpowers", "skills/writing-skills/SKILL.md"): "建立、測試與維護技能文件本身的技能設計技能。",
}

CATEGORY_OVERRIDES = {
    ("gstack", "AGENTS.md"): ["工具程序型", "元技能型"],
    ("gstack", "CLAUDE.md"): ["工具程序型", "流程型", "元技能型"],
    ("gstack", "README.md"): ["工具程序型", "流程型"],
    ("gstack", "SKILL.md"): ["工具程序型", "流程型"],
    ("gstack", "autoplan/SKILL.md"): ["審查型", "流程型", "元技能型"],
    ("gstack", "benchmark/SKILL.md"): ["審查型", "工具程序型", "流程型"],
    ("gstack", "browse/SKILL.md"): ["工具程序型"],
    ("gstack", "canary/SKILL.md"): ["審查型", "流程型", "工具程序型"],
    ("gstack", "careful/SKILL.md"): ["工具程序型"],
    ("gstack", "codex/SKILL.md"): ["審查型", "工具程序型", "流程型"],
    ("gstack", "connect-chrome/SKILL.md"): ["工具程序型", "流程型"],
    ("gstack", "cso/SKILL.md"): ["思考框架型", "審查型", "人格型"],
    ("gstack", "design-consultation/SKILL.md"): ["思考框架型", "流程型", "人格型"],
    ("gstack", "design-review/SKILL.md"): ["審查型", "流程型", "人格型"],
    ("gstack", "design-shotgun/SKILL.md"): ["思考框架型", "流程型"],
    ("gstack", "document-release/SKILL.md"): ["工具程序型", "流程型"],
    ("gstack", "freeze/SKILL.md"): ["工具程序型"],
    ("gstack", "gstack-upgrade/SKILL.md"): ["工具程序型", "流程型"],
    ("gstack", "guard/SKILL.md"): ["工具程序型", "流程型"],
    ("gstack", "investigate/SKILL.md"): ["思考框架型", "流程型"],
    ("gstack", "land-and-deploy/SKILL.md"): ["審查型", "工具程序型", "流程型"],
    ("gstack", "learn/SKILL.md"): ["工具程序型", "流程型"],
    ("gstack", "office-hours/SKILL.md"): ["思考框架型", "人格型"],
    ("gstack", "plan-ceo-review/SKILL.md"): ["思考框架型", "審查型", "人格型", "流程型"],
    ("gstack", "plan-design-review/SKILL.md"): ["思考框架型", "審查型", "人格型", "流程型"],
    ("gstack", "plan-eng-review/SKILL.md"): ["思考框架型", "審查型", "人格型", "流程型"],
    ("gstack", "qa/SKILL.md"): ["審查型", "工具程序型", "流程型"],
    ("gstack", "qa-only/SKILL.md"): ["審查型", "流程型"],
    ("gstack", "retro/SKILL.md"): ["思考框架型", "審查型", "流程型"],
    ("gstack", "review/SKILL.md"): ["思考框架型", "審查型", "流程型"],
    ("gstack", "setup-browser-cookies/SKILL.md"): ["工具程序型"],
    ("gstack", "setup-deploy/SKILL.md"): ["工具程序型", "流程型"],
    ("gstack", "ship/SKILL.md"): ["審查型", "工具程序型", "流程型"],
    ("gstack", "unfreeze/SKILL.md"): ["工具程序型"],
    ("superpowers", "README.md"): ["元技能型", "流程型"],
    ("superpowers", "skills/brainstorming/SKILL.md"): ["思考框架型", "流程型"],
    ("superpowers", "skills/dispatching-parallel-agents/SKILL.md"): ["工具程序型", "流程型", "元技能型"],
    ("superpowers", "skills/executing-plans/SKILL.md"): ["工具程序型", "流程型"],
    ("superpowers", "skills/finishing-a-development-branch/SKILL.md"): ["工具程序型", "流程型"],
    ("superpowers", "skills/receiving-code-review/SKILL.md"): ["思考框架型", "審查型", "流程型"],
    ("superpowers", "skills/requesting-code-review/SKILL.md"): ["工具程序型", "流程型"],
    ("superpowers", "skills/subagent-driven-development/SKILL.md"): ["工具程序型", "流程型", "元技能型"],
    ("superpowers", "skills/systematic-debugging/SKILL.md"): ["思考框架型", "流程型"],
    ("superpowers", "skills/test-driven-development/SKILL.md"): ["思考框架型", "流程型"],
    ("superpowers", "skills/using-git-worktrees/SKILL.md"): ["工具程序型", "流程型"],
    ("superpowers", "skills/using-superpowers/SKILL.md"): ["流程型", "元技能型"],
    ("superpowers", "skills/verification-before-completion/SKILL.md"): ["思考框架型", "審查型", "流程型"],
    ("superpowers", "skills/writing-plans/SKILL.md"): ["思考框架型", "流程型"],
    ("superpowers", "skills/writing-skills/SKILL.md"): ["思考框架型", "流程型", "元技能型"],
}

CATEGORY_ORDER = ["思考框架型", "審查型", "工具程序型", "人格型", "流程型", "元技能型"]

DOMAIN_OVERRIDES = {
    ("gstack", "AGENTS.md"): ["meta"],
    ("gstack", "CLAUDE.md"): ["meta"],
    ("gstack", "README.md"): ["meta", "shipping"],
    ("gstack", "SKILL.md"): ["browser", "review"],
    ("gstack", "autoplan/SKILL.md"): ["planning", "review", "meta"],
    ("gstack", "benchmark/SKILL.md"): ["performance", "browser", "review"],
    ("gstack", "browse/SKILL.md"): ["browser"],
    ("gstack", "canary/SKILL.md"): ["performance", "browser", "shipping", "review"],
    ("gstack", "careful/SKILL.md"): ["safety"],
    ("gstack", "codex/SKILL.md"): ["review", "meta"],
    ("gstack", "connect-chrome/SKILL.md"): ["browser"],
    ("gstack", "cso/SKILL.md"): ["safety", "review"],
    ("gstack", "design-consultation/SKILL.md"): ["design", "planning"],
    ("gstack", "design-review/SKILL.md"): ["design", "review"],
    ("gstack", "design-shotgun/SKILL.md"): ["design", "planning"],
    ("gstack", "document-release/SKILL.md"): ["shipping", "meta"],
    ("gstack", "freeze/SKILL.md"): ["safety"],
    ("gstack", "gstack-upgrade/SKILL.md"): ["meta", "shipping"],
    ("gstack", "guard/SKILL.md"): ["safety"],
    ("gstack", "investigate/SKILL.md"): ["debugging"],
    ("gstack", "land-and-deploy/SKILL.md"): ["shipping", "review", "browser"],
    ("gstack", "learn/SKILL.md"): ["learning", "meta"],
    ("gstack", "office-hours/SKILL.md"): ["planning", "design"],
    ("gstack", "plan-ceo-review/SKILL.md"): ["planning", "review"],
    ("gstack", "plan-design-review/SKILL.md"): ["planning", "review", "design"],
    ("gstack", "plan-eng-review/SKILL.md"): ["planning", "review", "testing"],
    ("gstack", "qa/SKILL.md"): ["review", "browser", "debugging", "testing"],
    ("gstack", "qa-only/SKILL.md"): ["review", "browser", "debugging"],
    ("gstack", "retro/SKILL.md"): ["learning", "review"],
    ("gstack", "review/SKILL.md"): ["review", "shipping", "testing"],
    ("gstack", "setup-browser-cookies/SKILL.md"): ["browser"],
    ("gstack", "setup-deploy/SKILL.md"): ["shipping"],
    ("gstack", "ship/SKILL.md"): ["shipping", "review", "testing"],
    ("gstack", "unfreeze/SKILL.md"): ["safety"],
    ("superpowers", "README.md"): ["meta"],
    ("superpowers", "skills/brainstorming/SKILL.md"): ["planning", "design"],
    ("superpowers", "skills/dispatching-parallel-agents/SKILL.md"): ["parallel", "meta"],
    ("superpowers", "skills/executing-plans/SKILL.md"): ["planning"],
    ("superpowers", "skills/finishing-a-development-branch/SKILL.md"): ["shipping"],
    ("superpowers", "skills/receiving-code-review/SKILL.md"): ["review"],
    ("superpowers", "skills/requesting-code-review/SKILL.md"): ["review"],
    ("superpowers", "skills/subagent-driven-development/SKILL.md"): ["parallel", "meta", "planning"],
    ("superpowers", "skills/systematic-debugging/SKILL.md"): ["debugging"],
    ("superpowers", "skills/test-driven-development/SKILL.md"): ["testing", "debugging"],
    ("superpowers", "skills/using-git-worktrees/SKILL.md"): ["parallel", "shipping"],
    ("superpowers", "skills/using-superpowers/SKILL.md"): ["meta"],
    ("superpowers", "skills/verification-before-completion/SKILL.md"): ["review", "testing", "shipping"],
    ("superpowers", "skills/writing-plans/SKILL.md"): ["planning"],
    ("superpowers", "skills/writing-skills/SKILL.md"): ["meta", "planning", "testing"],
}


@dataclass
class Section:
    heading: str
    lines: list[str]


@dataclass
class Card:
    repo: str
    relpath: str
    file_type: str
    title: str
    output_name: str
    description: str
    full_text: str
    body_lines: list[str]
    sections: list[Section]
    one_liner: str
    categories: list[str]
    traits: list[str]
    domains: list[str]
    framework_lines: list[str]
    must_lines: list[str]
    forbid_lines: list[str]
    question_lines: list[str]
    review_lines: list[str]
    format_lines: list[str]
    applicable_lines: list[str]
    quote_lines: list[str]
    related: list[tuple[str, str, str, str]]


def iter_target_files(repo: str, base: Path) -> Iterable[tuple[str, Path]]:
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(base).as_posix()
        name = path.name
        if name in TARGET_FILE_NAMES:
            yield rel, path
        elif name == ROOT_README and len(rel.split("/")) <= 2:
            yield rel, path


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text

    raw = parts[1]
    body = parts[2]
    meta: dict[str, str] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        block = re.match(r"^([A-Za-z0-9_-]+):\s*\|$", line)
        if block:
            key = block.group(1)
            i += 1
            values = []
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                values.append(lines[i].strip())
                i += 1
            meta[key] = "\n".join(v for v in values if v)
            continue
        inline = re.match(r"^([A-Za-z0-9_-]+):\s*(.+)$", line)
        if inline:
            meta[inline.group(1)] = inline.group(2).strip()
        i += 1
    return meta, body


def fallback_description(body: str) -> str:
    lines = [line.strip() for line in body.splitlines()]
    chunks = []
    buffer = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line:
            if buffer:
                chunks.append(" ".join(buffer))
                buffer = []
            continue
        if line.startswith("#") or line.startswith("<!--") or line.startswith("<") and line.endswith(">"):
            continue
        buffer.append(line)
        if len(" ".join(buffer)) > 240:
            break
    if buffer:
        chunks.append(" ".join(buffer))
    return chunks[0] if chunks else ""


def parse_sections(body: str) -> list[Section]:
    sections: list[Section] = []
    current_heading = "__ROOT__"
    current_lines: list[str] = []
    for raw_line in body.splitlines():
        if raw_line.startswith("## "):
            sections.append(Section(current_heading, current_lines))
            current_heading = raw_line[3:].strip()
            current_lines = []
        else:
            current_lines.append(raw_line.rstrip())
    sections.append(Section(current_heading, current_lines))
    return sections


def derive_title(relpath: str) -> str:
    if relpath.endswith("/SKILL.md"):
        return relpath.split("/")[-2]
    return Path(relpath).stem


def output_name_for(relpath: str) -> str:
    parts = relpath.split("/")
    if relpath == "README.md":
        return "_root-readme.md"
    if relpath == "CLAUDE.md":
        return "_root-claude.md"
    if relpath == "AGENTS.md":
        return "_root-agents.md"
    if relpath == "SKILL.md":
        return "_root-skill.md"
    if parts[-1] == "SKILL.md":
        return f"{parts[-2]}.md"
    return f"{Path(relpath).stem.lower()}.md"


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def interesting_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("```") or stripped.startswith("<!--"):
        return False
    if stripped.startswith("---"):
        return False
    if len(stripped) < 3:
        return False
    if re.fullmatch(r"[#>*\-\s]+", stripped):
        return False
    return True


def dedupe_keep_order(lines: Iterable[str]) -> list[str]:
    seen = set()
    output = []
    for line in lines:
        key = line.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(line)
    return output


def lines_from_section(section: Section) -> list[str]:
    results = []
    in_code = False
    for raw in section.lines:
        if raw.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        stripped = raw.strip()
        if not interesting_line(stripped):
            continue
        results.append(clean_line(stripped))
    return results


def extract_key_lines(section: Section, limit: int) -> list[str]:
    candidates = []
    for line in lines_from_section(section):
        if (
            re.match(r"^(\d+\.\s|[-*]\s)", line)
            or line.startswith("**")
            or line.endswith(":")
            or "MUST" in line
            or "NEVER" in line
            or "ALWAYS" in line
            or "Question:" in line
            or "Options:" in line
        ):
            candidates.append(line)
    if not candidates:
        candidates = lines_from_section(section)
    return candidates[:limit]


def collect_framework_lines(sections: list[Section]) -> list[str]:
    picked: list[str] = []
    for section in sections:
        heading_lower = section.heading.lower()
        if section.heading == "__ROOT__":
            continue
        if any(keyword in heading_lower for keyword in FRAMEWORK_HEADING_KEYWORDS):
            picked.append(f"[{section.heading}]")
            picked.extend(extract_key_lines(section, 6))
        if len(picked) >= 18:
            break
    return dedupe_keep_order(picked)[:18]


def collect_behavior_lines(lines: list[str]) -> tuple[list[str], list[str]]:
    must_patterns = ("MUST", "ALWAYS", "REQUIRED", "Before ", "Use AskUserQuestion", "Only run", "Ask the user")
    forbid_patterns = ("NEVER", "DO NOT", "don't", "Don't", "cannot", "not optional", "blocked", "skip this", "no fixes without")
    must_lines = []
    forbid_lines = []
    for line in lines:
        if any(token in line for token in must_patterns):
            must_lines.append(line)
        if any(token in line for token in forbid_patterns):
            forbid_lines.append(line)
    return dedupe_keep_order(must_lines)[:12], dedupe_keep_order(forbid_lines)[:12]


def collect_question_lines(sections: list[Section]) -> list[str]:
    picked = []
    for section in sections:
        heading_lower = section.heading.lower()
        if any(keyword in heading_lower for keyword in QUESTION_HEADING_KEYWORDS):
            picked.append(f"[{section.heading}]")
            for line in lines_from_section(section):
                if "Question:" in line or "Options:" in line or line.endswith("?") or "AskUserQuestion" in line:
                    picked.append(line)
        for line in lines_from_section(section):
            if len(picked) >= 12:
                break
            if line.endswith("?") and len(line) < 220:
                picked.append(line)
        if len(picked) >= 12:
            break
    return dedupe_keep_order(picked)[:12]


def split_description_phrases(description: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", description).strip()
    if not cleaned:
        return []
    pieces = re.split(r";|\. ", cleaned)
    results = []
    for piece in pieces:
        piece = piece.strip(" .")
        if not piece:
            continue
        if len(piece) > 220:
            piece = piece[:217].rstrip() + "..."
        results.append(piece)
    return results


def collect_review_lines(description: str, sections: list[Section], categories: list[str]) -> list[str]:
    if "審查型" not in categories:
        return []
    picked = []
    for section in sections:
        heading_lower = section.heading.lower()
        if any(keyword in heading_lower for keyword in REVIEW_HEADING_KEYWORDS):
            picked.append(f"[{section.heading}]")
            picked.extend(extract_key_lines(section, 6))
        if len(picked) >= 16:
            break
    if len(picked) < 4:
        for piece in split_description_phrases(description):
            lower = piece.lower()
            if any(token in lower for token in ("review", "audit", "qa", "analy", "find", "score", "check", "coverage")):
                picked.append(piece)
    return dedupe_keep_order(picked)[:16]


def collect_format_lines(sections: list[Section]) -> list[str]:
    picked = []
    for section in sections:
        heading_lower = section.heading.lower()
        if any(keyword in heading_lower for keyword in FORMAT_HEADING_KEYWORDS):
            picked.append(f"[{section.heading}]")
            picked.extend(extract_key_lines(section, 6))
        if len(picked) >= 14:
            break
    return dedupe_keep_order(picked)[:14]


def collect_quote_lines(description: str, sections: list[Section], line_count: int) -> list[str]:
    max_quotes = 10
    if line_count > 500:
        max_quotes = 16
    if line_count > 1200:
        max_quotes = 20

    picked = []
    for piece in split_description_phrases(description):
        picked.append(piece)

    for section in sections:
        if section.heading == "__ROOT__":
            continue
        picked.append(section.heading)
        picked.extend(extract_key_lines(section, 4))
        if len(picked) >= max_quotes * 2:
            break

    cleaned = []
    for line in dedupe_keep_order(picked):
        candidate = line.strip()
        if not candidate:
            continue
        if candidate.startswith("[") and candidate.endswith("]"):
            continue
        if len(candidate) > 260:
            candidate = candidate[:257].rstrip() + "..."
        cleaned.append(candidate.lstrip("> ").strip())
    return cleaned[:max_quotes]


def infer_categories(repo: str, relpath: str, description: str, body: str) -> list[str]:
    override = CATEGORY_OVERRIDES.get((repo, relpath))
    if override:
        return override

    text = f"{relpath} {description} {body}".lower()
    categories = []
    if any(token in text for token in ("principle", "framework", "pattern", "philosophy", "think", "brainstorm")):
        categories.append("思考框架型")
    if any(token in text for token in ("review", "audit", "qa", "checklist", "rubric", "verification")):
        categories.append("審查型")
    if any(token in text for token in ("setup", "command", "hook", "import", "connect", "worktree", "tool")):
        categories.append("工具程序型")
    if any(token in text for token in ("ceo", "founder", "designer", "chief security officer", "office hours", "voice")):
        categories.append("人格型")
    if any(token in text for token in ("workflow", "step", "steps", "phase", "process", "red-green-refactor")):
        categories.append("流程型")
    if any(token in text for token in ("skill", "skills", "agents", "claude", "superpowers")):
        categories.append("元技能型")
    return categories or ["工具程序型"]


def infer_traits(relpath: str, description: str, categories: list[str]) -> list[str]:
    text = f"{relpath} {description}".lower()
    traits = []
    if "審查型" in categories:
        traits.extend(["結構化", "批判性", "風險敏感"])
    if "思考框架型" in categories:
        traits.extend(["框架導向", "第一性原理", "推理導向"])
    if "流程型" in categories:
        traits.extend(["流程紀律", "完成導向"])
    if "工具程序型" in categories:
        traits.extend(["務實", "操作導向"])
    if "人格型" in categories:
        traits.extend(["角色鮮明", "觀點強烈"])
    if "元技能型" in categories:
        traits.extend(["規範導向", "元認知"])
    if any(token in text for token in ("debug", "root cause", "verification", "tdd", "test")):
        traits.extend(["證據導向", "懷疑論"])
    if any(token in text for token in ("design", "designer", "typography", "visual")):
        traits.extend(["品味導向", "體驗敏感"])
    if any(token in text for token in ("ceo", "founder", "office hours", "scope", "ambition")):
        traits.extend(["挑戰性", "野心導向", "產品導向"])
    if any(token in text for token in ("security", "safety", "careful", "guard", "freeze")):
        traits.extend(["謹慎", "防呆導向"])
    if any(token in text for token in ("parallel", "subagent", "worktree")):
        traits.extend(["協作導向", "拆解導向"])
    if any(token in text for token in ("learn", "retro", "trend")):
        traits.extend(["反思性", "累積導向"])
    return dedupe_keep_order(traits)[:10]


def infer_domains(repo: str, relpath: str, description: str, headings: list[str]) -> list[str]:
    override = DOMAIN_OVERRIDES.get((repo, relpath))
    if override:
        return override
    text = " ".join([relpath, description, *headings]).lower()
    domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            domains.append(domain)
    return domains


def extract_triggers(description: str) -> list[str]:
    triggers = re.findall(r'"([^"]+)"', description)
    return dedupe_keep_order(triggers)


def build_applicable_lines(one_liner: str, description: str) -> list[str]:
    triggers = extract_triggers(description)
    lines = [f"- 適合在需要「{one_liner.rstrip('。')}」的工作階段使用。"]
    if triggers:
        preview = " / ".join(triggers[:8])
        lines.append(f"- 常見觸發語句：{preview}")
    lower = description.lower()
    if "proactively suggest" in lower:
        lines.append("- 也適合在使用者尚未明講，但上下文已顯示相同需求時主動建議使用。")
    if any(token in lower for token in ("review", "audit", "qa", "verification")):
        lines.append("- 常出現在審查、驗證、合併前檢查或上線後回看階段。")
    elif any(token in lower for token in ("plan", "brainstorm", "scope", "requirements")):
        lines.append("- 常出現在規劃、定義問題、確認範圍或決策前討論階段。")
    elif any(token in lower for token in ("deploy", "release", "ship", "branch")):
        lines.append("- 常出現在收尾、發布、分支整理或部署交接階段。")
    elif any(token in lower for token in ("setup", "connect", "import", "worktree")):
        lines.append("- 常出現在正式施工前的環境準備與工具接線階段。")
    return lines[:4]


def tokenize(text: str) -> set[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z][a-z0-9-]{2,}", text)
    return {token for token in tokens if token not in SIMILARITY_STOPWORDS}


def related_reason(shared_domains: set[str], shared_categories: set[str], shared_tokens: set[str]) -> str:
    bits = []
    if shared_domains:
        bits.append("共享領域：" + ", ".join(sorted(shared_domains)[:3]))
    if shared_categories:
        ordered = sorted(shared_categories, key=CATEGORY_ORDER.index)
        bits.append("共享分類：" + "、".join(ordered))
    if shared_tokens:
        bits.append("共同關鍵詞：" + ", ".join(sorted(shared_tokens)[:4]))
    return "；".join(bits) if bits else "主題與流程高度接近"


def relation_type(shared_domains: set[str], shared_categories: set[str]) -> str:
    signal_domains = shared_domains - {"meta"}
    if len(signal_domains) >= 1 or {"審查型", "流程型"}.issubset(shared_categories) or {"思考框架型", "流程型"}.issubset(shared_categories):
        return "相似"
    return "互補"


def markdown_escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def format_checkboxes(categories: list[str]) -> str:
    lines = []
    selected = set(categories)
    for category in CATEGORY_ORDER:
        mark = "x" if category in selected else " "
        lines.append(f"- [{mark}] {category}")
    return "\n".join(lines)


def build_card_markdown(card: Card) -> str:
    framework = "\n".join(f"- {line}" for line in card.framework_lines) if card.framework_lines else "原文過短，無法提取"
    must_block = "\n".join(f"- {line}" for line in card.must_lines) if card.must_lines else "- 原文過短，無法提取"
    forbid_block = "\n".join(f"- {line}" for line in card.forbid_lines) if card.forbid_lines else "- 原文過短，無法提取"
    question_block = "\n".join(f"- {line}" for line in card.question_lines) if card.question_lines else "無明確提問模板"
    review_block = "\n".join(f"- {line}" for line in card.review_lines) if card.review_lines else "非審查型"
    format_block = "\n".join(f"- {line}" for line in card.format_lines) if card.format_lines else "無特定格式要求"
    applicable_block = "\n".join(card.applicable_lines)
    quote_block = "\n".join(f"> {line}" for line in card.quote_lines) if card.quote_lines else "> 原文過短，無法提取"
    if card.related:
        related_block = "\n".join(
            f"- {name}（{repo}） - {relation} - {reason}"
            for name, repo, relation, reason in card.related
        )
    else:
        related_block = "- 尚未發現明確關聯"

    return f"""---
## {card.repo} / {card.title}

### 來源
- repo：{card.repo}
- 路徑：{card.relpath}
- 檔案類型：{card.file_type}

### 一句話定位
{card.one_liner}

### 核心人格特質
{", ".join(card.traits) if card.traits else "原文過短，無法提取"}

### 核心思考框架
{framework}

### 核心行為規則
必須做
{must_block}

禁止做
{forbid_block}

### 提問方式
{question_block}

### 審查維度
{review_block}

### 輸出格式要求
{format_block}

### 適用場景
{applicable_block}

### 原文精華摘錄
{quote_block}

### 和其他 skill 的潛在關聯
{related_block}

### 分類標記
{format_checkboxes(card.categories)}
---
"""


def build_index(cards: list[Card]) -> str:
    repo_groups = defaultdict(list)
    for card in cards:
        repo_groups[card.repo].append(card)

    category_counts = Counter()
    for card in cards:
        category_counts.update(card.categories)

    gstack_rows = []
    superpowers_rows = []
    for idx, card in enumerate(repo_groups["gstack"], start=1):
        related_preview = "；".join(f"{name}（{repo}）" for name, repo, _, _ in card.related[:3]) or "-"
        row = f"| {idx} | {markdown_escape_cell(card.title)} | {markdown_escape_cell(card.one_liner)} | {markdown_escape_cell('、'.join(card.categories))} | {markdown_escape_cell(related_preview)} |"
        gstack_rows.append(row)
    for idx, card in enumerate(repo_groups["superpowers"], start=1):
        related_preview = "；".join(f"{name}（{repo}）" for name, repo, _, _ in card.related[:3]) or "-"
        row = f"| {idx} | {markdown_escape_cell(card.title)} | {markdown_escape_cell(card.one_liner)} | {markdown_escape_cell('、'.join(card.categories))} | {markdown_escape_cell(related_preview)} |"
        superpowers_rows.append(row)

    seen_pairs = set()
    cross_rows = []
    for card in cards:
        for related_name, related_repo, relation, reason in card.related:
            if card.repo == related_repo:
                continue
            left, right = (card.title, related_name) if card.repo == "gstack" else (related_name, card.title)
            key = (left, right, relation)
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            cross_rows.append(
                f"| {markdown_escape_cell(left)} | {markdown_escape_cell(right)} | {relation} | {markdown_escape_cell(reason)} |"
            )

    return "\n".join(
        [
            "# Skill 人格抽取總索引",
            "",
            "## 統計",
            f"- gstack skill 數量：{len(repo_groups['gstack'])}",
            f"- superpowers skill 數量：{len(repo_groups['superpowers'])}",
            f"- 總卡片數：{len(cards)}",
            f"- 思考框架型數量：{category_counts['思考框架型']}",
            f"- 審查型數量：{category_counts['審查型']}",
            f"- 工具程序型數量：{category_counts['工具程序型']}",
            f"- 人格型數量：{category_counts['人格型']}",
            f"- 流程型數量：{category_counts['流程型']}",
            f"- 元技能型數量：{category_counts['元技能型']}",
            "",
            "## gstack 卡片列表",
            "| # | skill 名稱 | 一句話定位 | 分類標記 | 潛在關聯 |",
            "|---|-----------|-----------|---------|---------|",
            *gstack_rows,
            "",
            "## superpowers 卡片列表",
            "| # | skill 名稱 | 一句話定位 | 分類標記 | 潛在關聯 |",
            "|---|-----------|-----------|---------|---------|",
            *superpowers_rows,
            "",
            "## 跨 repo 相似性矩陣",
            "| gstack skill | superpowers skill | 關係 | 理由 |",
            "|-------------|-------------------|------|------|",
            *cross_rows,
            "",
        ]
    )


def build_classification(cards: list[Card]) -> str:
    grouped = defaultdict(list)
    for card in cards:
        for category in card.categories:
            grouped[category].append(card)

    lines = ["# 按分類彙整", ""]
    for category in CATEGORY_ORDER:
        lines.append(f"## {category}")
        if grouped[category]:
            for card in grouped[category]:
                lines.append(f"- {card.title}（{card.repo}）: {card.one_liner}")
        else:
            lines.append("- 無")
        lines.append("")

    lines.append("## 多重分類")
    multi = [card for card in cards if len(card.categories) > 1]
    if multi:
        for card in multi:
            lines.append(f"- {card.title}（{card.repo}）: {'、'.join(card.categories)}")
    else:
        lines.append("- 無")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    cards: list[Card] = []

    for repo in ("gstack", "superpowers"):
        base = REPOS_ROOT / repo
        for relpath, path in iter_target_files(repo, base):
            text = normalize_text(path.read_text(encoding="utf-8", errors="replace"))
            metadata, body = parse_frontmatter(text)
            description = metadata.get("description") or fallback_description(body)
            sections = parse_sections(body)
            headings = [section.heading for section in sections if section.heading != "__ROOT__"]
            categories = infer_categories(repo, relpath, description, body)
            line_count = len(text.splitlines())
            body_lines = [clean_line(line) for line in body.splitlines() if interesting_line(line)]
            one_liner = ONE_LINERS[(repo, relpath)]
            traits = infer_traits(relpath, description, categories)
            domains = infer_domains(repo, relpath, description, headings)
            framework_lines = collect_framework_lines(sections)
            must_lines, forbid_lines = collect_behavior_lines(body_lines)
            question_lines = collect_question_lines(sections)
            review_lines = collect_review_lines(description, sections, categories)
            format_lines = collect_format_lines(sections)
            applicable_lines = build_applicable_lines(one_liner, description)
            quote_lines = collect_quote_lines(description, sections, line_count)

            cards.append(
                Card(
                    repo=repo,
                    relpath=relpath,
                    file_type=Path(relpath).name,
                    title=derive_title(relpath),
                    output_name=output_name_for(relpath),
                    description=description,
                    full_text=text,
                    body_lines=body_lines,
                    sections=sections,
                    one_liner=one_liner,
                    categories=categories,
                    traits=traits,
                    domains=domains,
                    framework_lines=framework_lines,
                    must_lines=must_lines,
                    forbid_lines=forbid_lines,
                    question_lines=question_lines,
                    review_lines=review_lines,
                    format_lines=format_lines,
                    applicable_lines=applicable_lines,
                    quote_lines=quote_lines,
                    related=[],
                )
            )

    token_sets = {
        (card.repo, card.relpath): tokenize(
            " ".join(
                [
                    card.title,
                    card.description,
                    " ".join(section.heading for section in card.sections if section.heading != "__ROOT__"),
                ]
            )
        )
        for card in cards
    }

    for card in cards:
        scores = []
        card_key = (card.repo, card.relpath)
        card_tokens = token_sets[card_key]
        for other in cards:
            other_key = (other.repo, other.relpath)
            if other_key == card_key:
                continue
            shared_domains = set(card.domains) & set(other.domains)
            shared_categories = set(card.categories) & set(other.categories)
            shared_tokens = card_tokens & token_sets[other_key]
            signal_domains = shared_domains - {"meta"}
            score = len(signal_domains) * 6 + len(shared_tokens) * 2 + max(0, len(shared_categories) - 1)
            if "meta" in shared_domains:
                score += 1
            if score <= 0:
                continue
            if not signal_domains and len(shared_tokens) < 2 and len(shared_categories) < 3:
                continue
            scores.append((score, other, shared_domains, shared_categories, shared_tokens))

        scores.sort(key=lambda item: (-item[0], item[1].repo, item[1].title))

        picked = []
        for _, other, shared_domains, shared_categories, shared_tokens in scores:
            relation = relation_type(shared_domains, shared_categories)
            reason = related_reason(shared_domains, shared_categories, shared_tokens)
            picked.append((other.title, other.repo, relation, reason))
            if len(picked) >= 4:
                break
        card.related = picked

    RAW_CARDS_ROOT.mkdir(parents=True, exist_ok=True)
    for repo in ("gstack", "superpowers"):
        (RAW_CARDS_ROOT / repo).mkdir(parents=True, exist_ok=True)

    for card in cards:
        target = RAW_CARDS_ROOT / card.repo / card.output_name
        target.write_text(build_card_markdown(card), encoding="utf-8")

    cards_sorted = sorted(cards, key=lambda card: (card.repo, card.output_name))
    (EXTRACTION_ROOT / "00_總索引.md").write_text(build_index(cards_sorted), encoding="utf-8")
    (EXTRACTION_ROOT / "01_分類彙整.md").write_text(build_classification(cards_sorted), encoding="utf-8")


if __name__ == "__main__":
    main()
