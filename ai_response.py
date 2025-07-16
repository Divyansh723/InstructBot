import google.generativeai as genai
from config import GEMINI_API_KEY
import json
import re

# === Configure Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# === System Prompt ===
system_instruction = """
You are InstructBot, an intelligent assistant that can either:
1. Respond with natural AI-generated information (type = "ai_response")
2. Classify the command as a system task (type = "system_task")

Always respond ONLY in this structured JSON format:
{
  "type": "ai_response" or "system_task",
  "text": "Your reply to user here.",
  "intent": "open_calculator | open_browser | open_notepad | search_google | set_alarm | shutdown | custom_intent_name",
  "params": { "key1": "value", ... }  // leave blank if unused
}

Guidelines:
- Use "ai_response" if it's a general question, conversation, or information.
- Use "system_task" if it sounds like an executable command.
- Don't generate explanations or extra text outside the JSON block.
"""

# === Function: Ask Gemini & Classify ===
def ask_instructbot(user_input: str) -> dict:
    try:
        full_prompt = system_instruction + f'\n\nUser Input: "{user_input}"\n'
        response = chat.send_message(full_prompt)
        raw = response.text.strip()

        # Strip markdown ```json formatting if present
        if raw.startswith("```"):
            raw = re.sub(r"```(json)?", "", raw).strip()

        # Try parsing the JSON response
        data = json.loads(raw)

        # Validate required keys
        required_keys = {"type", "text", "intent", "params"}
        if not required_keys.issubset(data.keys()):
            raise ValueError("Missing keys in Gemini response.")

        return data

    except Exception as e:
        print(f"❌ Gemini response error: {e}")
        return {
            "type": "error",
            "text": "Sorry, I couldn't understand or process your request.",
            "intent": None,
            "params": {}
        }
