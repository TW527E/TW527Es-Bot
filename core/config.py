import json
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional until dependencies are installed
    load_dotenv = None


ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = ROOT / "setting.json"
SERVER_CONFIG_DIR = ROOT / "servers"
DATA_DIR = ROOT / "data"

DEFAULT_SETTINGS = {
    "Token": "",
    "Owner_id": "",
    "bot_ready_channel": "",
    "Indecent_words": [],
    "MC_img": [],
    "url_img": [],
    "time": "0900",
    "auto_message": "test",
    "auto_message_channel": "",
}


def _load_dotenv():
    if load_dotenv is not None:
        load_dotenv(ROOT / ".env")


def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return {} if default is None else default.copy()

    with path.open("r", encoding="utf8") as file:
        return json.load(file)


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.write("\n")


def get_settings():
    _load_dotenv()
    settings = DEFAULT_SETTINGS.copy()
    stored_settings = read_json(SETTINGS_PATH, {})
    settings.update({key: value for key, value in stored_settings.items() if key in DEFAULT_SETTINGS})

    token = os.getenv("DISCORD_TOKEN")
    owner_id = os.getenv("DISCORD_OWNER_ID")

    if token:
        settings["Token"] = token
    if owner_id:
        settings["Owner_id"] = owner_id

    return settings


def save_settings(settings):
    current = DEFAULT_SETTINGS.copy()
    stored_settings = read_json(SETTINGS_PATH, {})
    current.update({key: value for key, value in stored_settings.items() if key in DEFAULT_SETTINGS})
    current.update({key: value for key, value in settings.items() if key in DEFAULT_SETTINGS})
    write_json(SETTINGS_PATH, current)


def get_token(settings=None):
    settings = settings or get_settings()
    return str(settings.get("Token") or "").strip()


def int_or_none(value):
    try:
        if value in (None, ""):
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def get_owner_id(settings=None):
    settings = settings or get_settings()
    return int_or_none(settings.get("Owner_id"))


def get_configured_images(settings, key, fallback_dir):
    configured = settings.get(key) or []
    images = []

    for item in configured:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / path
        if path.exists() and path.is_file():
            images.append(path)

    if not images:
        directory = ROOT / fallback_dir
        if directory.exists():
            images = sorted(
                path
                for path in directory.iterdir()
                if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}
            )

    return images


def get_guild_configs():
    configs = []
    if not SERVER_CONFIG_DIR.exists():
        return configs

    for path in sorted(SERVER_CONFIG_DIR.glob("*.json")):
        if path.name.endswith(".example.json"):
            continue
        data = read_json(path, {})
        guild_id = int_or_none(data.get("guild_id"))
        if guild_id is None:
            continue
        data["_name"] = path.stem
        data["guild_id"] = guild_id
        configs.append(data)

    return configs
