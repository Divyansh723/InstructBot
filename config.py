# Configuration file for keys, settings, etc.from dotenv import load_dotenv
import os
from dotenv import load_dotenv

load_dotenv()

SAFE_MODE = os.getenv("SAFE_MODE", "True") == "True"
ALLOW_ADMIN = os.getenv("ALLOW_ADMIN", "False") == "True"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

SAFE_COMMANDS = [
    "open notepad",
    "screenshot",
    "what time is it",
    "tell me the time"
]
