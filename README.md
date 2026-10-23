# Astra — Your AI, Your Space

Astra is a local AI chatbot built with Python, Streamlit, Ollama, and the Qwen3:0.6b model.

## Features

- Chat with a locally running AI model.
- Continue conversations using chat history.
- Create new conversations and switch between saved chats.
- Save and reload conversations using JSON files.
- Handle connection errors when Ollama is unavailable.
- English and Arabic interface.

## Requirements

- Python
- Ollama
- The `qwen3:0.6b` model
- pip

## Installation

1. Install Ollama from https://ollama.com/.
2. Download the model:

   ```bash
   ollama pull qwen3:0.6b
   ```

3. Clone this repository and open its folder.
4. Create and activate a Python virtual environment.
5. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the application

Start Ollama, then run:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Project structure

- `app.py` — Streamlit user interface.
- `chatbot.py` — Ollama communication and response generation.
- `session_manager.py` — Conversation creation, saving, and loading.
- `assets/` — Application images and logo.
- `sessions/` — Local JSON conversation files.

## Model

The application uses `qwen3:0.6b` through Ollama and runs inference locally.

## Notes

The virtual environment is not included in the repository. Install dependencies using `requirements.txt` before running the application.