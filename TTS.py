from flask import Flask, request, send_file, abort
import pyttsx3
import uuid
import os
import time

app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text', 'Hello from the server')
    rate = int(data.get('rate', 140))
    volume = float(data.get('volume', 1.0))
    voice_index = int(data.get('voice', 0))

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)

    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Absolute file path to current directory
    file_name = f"tts_output_{uuid.uuid4()}.mp3"
    file_path = os.path.join(os.getcwd(), file_name)

    engine.save_to_file(text, file_path)
    engine.runAndWait()

    # Wait briefly to ensure file write completion
    wait_time = 0
    while not os.path.exists(file_path) and wait_time < 5:
        time.sleep(0.1)
        wait_time += 0.1

    if not os.path.exists(file_path):
        abort(500, description="Audio file was not created.")

    response = send_file(file_path, as_attachment=True)

    @response.call_on_close
    def cleanup():
        if os.path.exists(file_path):
            os.remove(file_path)

    return response

@app.route('/')
def index():
    return 'Server is running'

if __name__ == "__main__":
    app.run(port=5000, debug=True)
