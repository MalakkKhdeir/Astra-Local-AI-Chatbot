
import ollama

MODEL_NAME = "qwen3:0.6b"
TIMEOUT_SECONDS = 300


def ask_ai(message, history=None):
    """Send a message and conversation history to Ollama."""

    if history is None:
        history = []

    messages = history + [
        {"role": "user", "content": message}
    ]

    client = ollama.Client(
        host="http://127.0.0.1:11434",
        timeout=TIMEOUT_SECONDS,
    )

    response = client.chat(
        model=MODEL_NAME,
        messages=messages,
    )

    return response["message"]["content"]
