# TW527E's Bot

中文名稱：TW527E的機器人

這是一個早期開發的 Discord 管理/互動機器人。此分支已將專案整理成可在現代 `discord.py` 2.x 執行的結構，並移除敏感資料、快取資料與舊的音樂播放模組。

## 目前功能

- 基本斜線指令：`/ping`、`/avatar`、`/info`、`/guild`、`/now_time`
- 管理斜線指令：`/kick`、`/ban`、`/unban`、`/del_msg`、`/say_msg`、`/say_dm`
- 伺服器管理：建立文字/語音頻道、查看/新增/移除身分組、修改伺服器名稱
- 事件監聽：成員加入/離開通知、reaction role
- 訊息互動：關鍵字回覆、不雅詞過濾
- 等級系統：依訊息數累積經驗值，資料存放於本機 `data/levels.json`
- 定時公告：可設定公告時間、頻道與內容

音樂播放功能已完整刪除。原模組長期無法穩定運作，且依賴 YouTube 下載/串流流程，容易碰到版權與平台規範問題。

## 環境需求

- Python 3.10 或更新版本
- Discord Bot Token
- 已在 Discord Developer Portal 啟用必要 intents

安裝依賴：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Discord 設定

本專案使用 Discord 斜線指令。邀請 bot 時需要包含 `bot` 和 `applications.commands` scopes。

因為 bot 仍會讀取訊息內容做關鍵字回覆、不雅詞過濾與等級系統，並且會監聽成員加入/離開事件，請在 Discord Developer Portal 的 Bot 頁面啟用：

- Message Content Intent
- Server Members Intent

程式中已同步設定：

- `intents.message_content = True`
- `intents.members = True`
- `intents.reactions = True`

## 本機設定

敏感資訊不要提交到版本庫。此專案會優先讀取 `.env`，也支援本機 `setting.json`。

`.env` 範例：

```env
DISCORD_TOKEN=你的 Bot Token
DISCORD_OWNER_ID=你的 Discord 使用者 ID
```

也可以用 `setting.example.json` 建立本機 `setting.json`，常用欄位如下：

- `Token`：Discord Bot Token，建議改用 `.env` 的 `DISCORD_TOKEN`
- `Owner_id`：bot 擁有者 Discord 使用者 ID
- `bot_ready_channel`：bot 上線通知頻道 ID
- `Indecent_words`：不雅詞過濾清單
- `MC_img`：指定本機圖片路徑清單，空陣列時會 fallback 到 `Photo/`
- `url_img`：隨機網路圖片 URL 清單
- `time`：定時公告時間，格式 `HHMM`
- `auto_message`：定時公告內容
- `auto_message_channel`：定時公告頻道 ID

伺服器專屬設定請參考 `servers/server.example.json` 建立本機 `servers/<name>.json`。這些檔案已被 `.gitignore` 忽略。

啟動時如果存在 `servers/*.json`，程式會把 slash commands 同步到這些 guild，通常可立即測試。若沒有伺服器設定檔，程式會同步全域 slash commands，Discord 可能需要一段時間才會顯示。

## 啟動

```powershell
.\.venv\Scripts\python.exe start.py
```

Windows 也可以執行：

```powershell
.\start.bat
```

## 專案結構

```text
cmds/        一般文字指令與管理指令
event/       Discord 事件監聽
server/      伺服器與頻道管理指令
core/        共用設定、Log、Cog 基底與 Discord helper
Photo/       本機圖片素材，已忽略，不提交
G/           本機圖片素材，已忽略，不提交
data/        執行時資料，已忽略
Log/         執行時 log，已忽略
```

## 已清理的內容

- 移除重複入口 `bot.py`
- 移除舊備份 `Voice Backup.py`
- 移除壞掉且有版權風險的音樂模組 `server/Voice.py`
- 移除個人 `.vscode/` 設定
- 移除舊依賴清單文字檔
- 移除 tracked `setting.json`、`setting.bot.json`、`servers/*.json` 與等級資料 JSON
- 移除 tracked `G/`、`Photo/` 圖片素材，改由本機忽略保存
- 新增 `.env.example`、`setting.example.json`、`servers/server.example.json`
- 更新 `.gitignore`，忽略 token、本機設定、log、cache、下載檔與執行時資料
