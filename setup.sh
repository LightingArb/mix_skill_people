#!/bin/bash
echo "正在安裝研究工具..."

# 安裝 Node 依賴 + Playwright chromium
npm install
npx playwright install chromium

# 安裝 chrome-devtools-mcp
npm install -g @anthropic/chrome-devtools-mcp 2>/dev/null || echo "chrome-devtools-mcp 安裝失敗，動態爬蟲仍可使用 Playwright"

echo ""
echo "安裝完成！你可以開始使用了。"
echo "打開 Claude Code，對 AI 說「創建人格」就能開始。"
