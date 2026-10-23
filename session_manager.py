
import json
import uuid
from pathlib import Path
from datetime import datetime


SESSIONS_DIR = Path(__file__).parent / "sessions"


def ensure_sessions_dir():
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def create_chat():
    chat = {
        "id": str(uuid.uuid4()),
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().isoformat(),
    }

    save_chat(chat)
    return chat


def save_chat(chat):
    ensure_sessions_dir()

    file_path = SESSIONS_DIR / f"{chat['id']}.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(chat, file, ensure_ascii=False, indent=4)


def load_chat(chat_id):
    ensure_sessions_dir()
    file_path = SESSIONS_DIR / f"{chat_id}.json"

    if not file_path.exists():
        return None

    try:
        with file_path.open("r", encoding="utf-8") as file:
            chat = json.load(file)

        if chat.get("id") != chat_id:
            return None

        return chat

    except (json.JSONDecodeError, OSError):
        return None


def list_chats():
    ensure_sessions_dir()
    chats = []

    for file_path in SESSIONS_DIR.glob("*.json"):
        chat = load_chat(file_path.stem)

        if chat is not None:
            chats.append(chat)

    chats.sort(
        key=lambda chat: chat.get("created_at", ""),
        reverse=True,
    )

    return chats


def update_chat_title(chat):
    if chat["title"] == "New Chat":
        for message in chat["messages"]:
            if message["role"] == "user":
                title = message["content"].strip()
                chat["title"] = title[:40] or "New Chat"
                break

    return chat
