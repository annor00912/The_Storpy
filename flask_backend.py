
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import base64
import tempfile
import uuid
import os

app = Flask(__name__)
CORS(app)

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/get-story', methods=['POST'])
def get_story():
    data = request.get_json()
    topic = data.get('topic', '').strip()
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
    try:
        prompt = f"Tell me a calming and engaging bedtime story about {topic}, suitable for all ages, in a soothing tone."
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        story = completion.choices[0].message.content.strip()
        return jsonify({'story': story})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        speech_response = openai_client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        file_id = str(uuid.uuid4()) + ".mp3"
        audio_path = os.path.join(tempfile.gettempdir(), file_id)
        with open(audio_path, 'wb') as f:
            f.write(speech_response.read())
        with open(audio_path, 'rb') as f:
            b64_audio = base64.b64encode(f.read()).decode('utf-8')
        return jsonify({'url': f"data:audio/mp3;base64,{b64_audio}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
