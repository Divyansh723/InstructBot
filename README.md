# 🎙️ AI Voice Assistant – Flask App

A smart voice assistant web application built with Flask that listens to user speech, interprets the command using AI, and performs system tasks or responds with natural language. The assistant speaks the response back and provides real-time feedback on the interface.

---

## 🧠 Key Features

- 🎤 **Voice Input**: Capture user voice commands through the browser.
- 🧠 **AI-Powered Interpretation**: Uses `ask_instructbot()` to decide if a command is a system task or general question.
- 🛠️ **System Task Execution**: Executes commands like opening apps, fetching system info, etc.
- 💬 **Natural Language Replies**: Responds using intelligent AI-generated replies when no system task is needed.
- 🔈 **Text-to-Speech Output**: Speaks the response aloud using the system’s TTS engine.
- 🖥️ **Responsive Frontend**: Real-time status updates like “Listening…”, “Thinking…”, and “Stopped”.

---

## 📁 Project Structure

instructbot/
├── app.py # Main Flask app
├── config.py # SAFE_MODE and other settings
├── speech_to_text.py # Microphone input and speech recognition
├── text_to_speech.py # Text-to-speech conversion
├── ai_response.py # AI decision logic (chat vs system task)
├── system_actions.py # Executes commands (e.g., open apps)
├── templates/
│ └── index.html # Frontend UI with buttons and status
├── static/
│ └── style.css # (Optional) UI styling
└── README.md # You’re here!

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Divyansh723/InstructBot.git
cd instructbot
2. Create virtual environment and install dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
3. Set environment variables
Create a .env or set in config.py:

python
Copy
Edit
SAFE_MODE = True  
4. Run the app
bash
Copy
Edit
python app.py
Then open http://localhost:5000 in your browser.

🧪 Example Workflow
Press Start Listening

Say: “Open Notepad” or “What is the weather?”

The assistant will:

Listen to your voice

Use ask_instructbot() to decide the intent

If it’s a system command, it runs run_system_task()

Otherwise, replies using AI

Finally, speaks the result out loud

🔧 API Endpoints
Method	Endpoint	Description
POST	/start_listening	Begins speech recognition, sends command to AI and executes
POST	/stop_listening	Stops the assistant
GET	/	Loads the HTML interface

📌 Dependencies
Flask

SpeechRecognition

pyttsx3 (Text-to-speech)

OpenAI / Gemini API (optional for AI replies)

OS libraries for system commands

Install via:

bash
Copy
Edit
pip install Flask SpeechRecognition pyttsx3
⚠️ Safety Notes
If SAFE_MODE = False, system commands will execute directly – use caution.

AI response models should be sandboxed if connected to powerful tools.

##📃 License
This project is open-source and available under the MIT License.
---
##🙋‍♂️ Author
Made with ❤️ by Divyansh
---
