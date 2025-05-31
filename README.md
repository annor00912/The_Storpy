
# Storpy Flask Backend

This is a lightweight Flask backend for the Storpy bedtime story app. It supports story generation and audio rendering via OpenAI.

## Endpoints

- `POST /get-story` — returns a calming bedtime story based on the user's topic.
- `POST /generate-audio` — returns base64 MP3 audio of the generated story.

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-api-key-here
python flask_backend.py
```

## Deployment

Use Railway, Render, or Heroku. Make sure to set the environment variable `OPENAI_API_KEY`.
