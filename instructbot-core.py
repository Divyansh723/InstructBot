from flask import Flask, render_template, jsonify, request
from speech_to_text import listen_command
from ai_response import ask_ai
from system_actions import handle_command
from text_to_speech import speak_text
from config import SAFE_MODE

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", safe_mode=SAFE_MODE)

@app.route("/listen", methods=["POST"])
def listen():
    command = listen_command()
    if not command:
        return jsonify({"transcript": "", "response": "I didn't catch that."})
    
    result = handle_command(command)
    if result is None:
        ai_reply = ask_ai(command)
        speak_text(ai_reply)
        return jsonify({"transcript": command, "response": ai_reply})
    else:
        speak_text(result)
        return jsonify({"transcript": command, "response": result})

if __name__ == "__main__":
    app.run(debug=True)
