from flask import Flask, render_template, jsonify, request
from speech_to_text import listen
from ai_response import ask_instructbot  # will decide system vs non-system
from system_actions import run_system_task
from text_to_speech import speak
from config import SAFE_MODE

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", safe_mode=SAFE_MODE)

listening = False

@app.route("/start_listening", methods=["POST"])
def start_listening():
    global listening
    listening = True

    # Step 1: Listen for input
    command = listen()

    if not command:
        return jsonify({"transcript": "", "response": "I didn't catch that."})

    # Step 2: Pass command to AI block for decision
    decision = ask_instructbot(command)  # This must return a dictionary like: {"type": "system" / "chat", "response": "..."}
    print(f"AI Decision: {decision}")
    # Step 3: Handle system command
    if decision.get("type") == "system_task":
        system_result = run_system_task(decision["intent"], decision.get("params", {}))
        final_response = system_result or "System task executed."
    else:
        final_response = decision.get("text", "I didn't understand that.")

    # Step 4: Speak out the final response
    speak(final_response)

    return jsonify({
        "transcript": command,
        "response": final_response
    })

@app.route("/stop_listening", methods=["POST"])
def stop_listening():
    global listening
    listening = False
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    app.run(debug=True)
