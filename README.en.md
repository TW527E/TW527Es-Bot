# TW527E's Bot

Chinese name: TW527E的機器人

Chinese version: [README.md](README.md)

This is an early-stage Discord moderation and interaction bot. This branch has reorganized the project so it can run on modern `discord.py` 2.x, while removing sensitive data, cache files, and the old music playback module.

## Current Features

- Basic slash commands: `/ping`, `/avatar`, `/info`, `/guild`, `/now_time`
- Moderation slash commands: `/kick`, `/ban`, `/unban`, `/del_msg`, `/say_msg`, `/say_dm`
- Server management: create text/voice channels, view/add/remove roles, and rename the server
- Event listeners: member join/leave notifications and reaction roles
- Message interactions: keyword replies and indecent-word filtering
- Level system: accumulates experience from message count and stores data locally in `data/levels.json`
- Scheduled announcements: configurable announcement time, channel, and message content

Music playback has been fully removed. The original module had long-term stability issues and depended on YouTube download/streaming flows, which can easily run into copyright and platform policy problems.

## Requirements

- Python 3.10 or newer
- Discord Bot Token
- Required intents enabled in the Discord Developer Portal

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Discord Setup

This project uses Discord slash commands. When inviting the bot, include both the `bot` and `applications.commands` scopes.

Because the bot still reads message content for keyword replies, indecent-word filtering, and the level system, and because it listens for member join/leave events, enable these options on the Bot page in the Discord Developer Portal:

- Message Content Intent
- Server Members Intent

The code also enables:

- `intents.message_content = True`
- `intents.members = True`
- `intents.reactions = True`

## Local Configuration

Do not commit sensitive information to the repository. This project reads `.env` first and also supports a local `setting.json`.

Example `.env`:

```env
DISCORD_TOKEN=your Bot Token
DISCORD_OWNER_ID=your Discord user ID
```

You can also create a local `setting.json` from `setting.example.json`. Common fields are:

- `Token`: Discord Bot Token. Prefer using `DISCORD_TOKEN` in `.env`.
- `Owner_id`: Discord user ID of the bot owner.
- `bot_ready_channel`: channel ID for bot online notifications.
- `Indecent_words`: indecent-word filter list.
- `MC_img`: list of local image paths. If empty, the bot falls back to `Photo/`.
- `url_img`: list of random online image URLs.
- `time`: scheduled announcement time in `HHMM` format.
- `auto_message`: scheduled announcement content.
- `auto_message_channel`: scheduled announcement channel ID.

For server-specific configuration, use `servers/server.example.json` to create a local `servers/<name>.json`. These files are ignored by `.gitignore`.

If `servers/*.json` exists on startup, the program syncs slash commands to those guilds, which usually makes testing available immediately. If no server configuration file exists, the program syncs global slash commands instead, and Discord may take some time before they appear.

## Start

```powershell
.\.venv\Scripts\python.exe start.py
```

On Windows, you can also run:

```powershell
.\start.bat
```

## Project Structure

```text
cmds/        General text commands and moderation commands
event/       Discord event listeners
server/      Server and channel management commands
core/        Shared config, logging, Cog base class, and Discord helpers
Photo/       Local image assets, ignored and not committed
G/           Local image assets, ignored and not committed
data/        Runtime data, ignored
Log/         Runtime logs, ignored
```

## Cleaned Up

- Removed duplicate entry point `bot.py`
- Removed old backup `Voice Backup.py`
- Removed the broken music module `server/Voice.py`, which also had copyright risk
- Removed personal `.vscode/` settings
- Removed old dependency-list text file
- Removed tracked `setting.json`, `setting.bot.json`, `servers/*.json`, and level-data JSON files
- Removed tracked `G/` and `Photo/` image assets, keeping them as ignored local files instead
- Added `.env.example`, `setting.example.json`, and `servers/server.example.json`
- Updated `.gitignore` to ignore tokens, local settings, logs, cache, downloaded files, and runtime data
