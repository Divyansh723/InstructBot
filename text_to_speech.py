import pyttsx3
import warnings
import os

warnings.simplefilter('ignore')

# === Configuration ===
BOT_NAME = "InstructBot"
DEFAULT_RATE = 175               # Speech speed
DEFAULT_VOLUME = 1.0             # 0.0 to 1.0
DEFAULT_GENDER = "female"        # Options: "male", "female", "any"

# === Voice selection function ===
def select_voice(engine, gender=DEFAULT_GENDER):
    voices = engine.getProperty("voices")
    selected = None

    # Try registry-based voice on Windows
    if os.name == "nt":
        if gender == "female":
            try:
                engine.setProperty("voice", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
                return
            except:
                pass
        elif gender == "male":
            try:
                engine.setProperty("voice", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")
                return
            except:
                pass

    # Fallback to voice matching name
    for voice in voices:
        if gender.lower() in voice.name.lower():
            selected = voice.id
            break

    engine.setProperty("voice", selected or voices[0].id)

# === TTS Function ===
def speak(text,DEFAULT_GENDER=DEFAULT_GENDER):
    print(f"\n🧠 {BOT_NAME} : {text}\n")
    engine = pyttsx3.init()
    engine.setProperty("rate", DEFAULT_RATE)
    engine.setProperty("volume", DEFAULT_VOLUME)
    select_voice(engine, DEFAULT_GENDER)
    engine.say(text)
    engine.runAndWait()

# === Main loop ===
if __name__ == "__main__":
    while True:
        user_input = input("Enter text to speak (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        speak(user_input)
