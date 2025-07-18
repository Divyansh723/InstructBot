# config.py — Centralized configuration for system settings and API keys
import os
from dotenv import load_dotenv

# === Load environment variables from .env file ===
load_dotenv()

# === Mode Toggles ===
SAFE_MODE       = os.getenv("SAFE_MODE", "True") == "True"
ALLOW_ADMIN     = os.getenv("ALLOW_ADMIN", "False") == "True"
ALLOW_ADVANCED  = os.getenv("ALLOW_ADVANCED", "False") == "True"

# === API Keys ===
GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# === Allowed Voice/Prompt Commands by Mode ===

SAFE_COMMANDS = [
    "open notepad",
    "open calculator",
    "open browser",
    "take screenshot",
    "what time is it",
    "tell me the time",
    "check battery",
    "count files",
    "search google",
    "open app"
]

ADVANCED_COMMANDS = [
    "clean downloads",
    "move files",
    "system report",
    "clean files by date",
    "create folder"
]

ADMIN_COMMANDS = [
    "shutdown",
    "restart system",
    "run shell",
    "delete file",
    "rename file"
]

# === Utility for Accessing Modes Elsewhere ===
def get_mode_value(mode_name: str) -> bool:
    return {
        "SAFE_MODE": SAFE_MODE,
        "ALLOW_ADMIN": ALLOW_ADMIN,
        "ALLOW_ADVANCED": ALLOW_ADVANCED,
    }.get(mode_name.upper(), False)

def set_mode_value(mode_name: str, value: bool) -> None:
    """
    Set mode flag (SAFE_MODE, ALLOW_ADMIN, ALLOW_ADVANCED) and persist to .env file.
    """
    mode_name = mode_name.upper()
    env_path = ".env"

    if mode_name not in ["SAFE_MODE", "ALLOW_ADMIN", "ALLOW_ADVANCED"]:
        raise ValueError(f"Unsupported mode: {mode_name}")

    # Update .env file
    updated_lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as file:
            lines = file.readlines()
        for line in lines:
            if line.startswith(f"{mode_name}="):
                updated_lines.append(f"{mode_name}={'True' if value else 'False'}\n")
            else:
                updated_lines.append(line)
    else:
        updated_lines = []

    # Add mode if not present
    if not any(line.startswith(f"{mode_name}=") for line in updated_lines):
        updated_lines.append(f"{mode_name}={'True' if value else 'False'}\n")

    # Write back to .env
    with open(env_path, "w") as file:
        file.writelines(updated_lines)

    # Update in-memory variable
    globals()[mode_name] = value
