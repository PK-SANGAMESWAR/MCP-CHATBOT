# Local Voice Assistant

A privacy-focused, fully local voice assistant that listens to your voice, transcribes it, processes it with a local Large Language Model (LLM), and speaks back the response.

## Features

- **🎙️ Real-time Audio Recording**: Captures voice input via microphone.
- **📝 Local Speech-to-Text**: Uses [OpenAI Whisper](https://github.com/openai/whisper) for accurate transcription running locally.
- **🧠 Local Intelligence**: Powered by [Ollama](https://ollama.com/) (running Llama 3.2) for private, offline responses.
- **💾 Long-term Memory**: Stores user details and conversations using Vector Search (FAISS).
- **😊 Emotion Detection**: Analyzes user sentiment to adjust responses.
- **🗣️ Text-to-Speech**: Uses `pyttsx3` for offline voice synthesis.
- **🔒 Privacy First**: All processing happens on your machine. No data is sent to the cloud.

## Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.8+**
2.  **FFmpeg**: Required for Whisper audio processing.
    *   *Windows*: `winget install ffmpeg` or download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
    *   *Mac*: `brew install ffmpeg`
    *   *Linux*: `sudo apt install ffmpeg`
3.  **Ollama**: Download and install from [ollama.com](https://ollama.com/).
    *   Pull the model used in the code:
        ```bash
        ollama pull llama3.2:3b
        ```
    *   Ensure Ollama is running (`ollama serve` or via the desktop app).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd AI-VOICE-AGENT
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Assistant**:
    ```bash
    python voice_agent/main.py
    ```

2.  **Interact**:
    *   Wait for the "Speak after the beep..." prompt.
    *   Speak your query clearly.
    *   The assistant will:
        *   Transcribe your speech.
        *   Detect your emotion and category (Personal, Work, etc.).
        *   Retrieve relevant past memories.
        *   Generate a context-aware response.
        *   Speak it back to you.

## Project Structure

```
AI-VOICE-AGENT/
├── voice_agent/
│   ├── asr/            # Automatic Speech Recognition (Whisper)
│   ├── audio/          # Audio recording logic
│   ├── llm/            # Local LLM integration (Ollama)
│   ├── memory/         # Memory & Emotion Detection
│   │   ├── category_detector.py
│   │   ├── emotion_detector.py
│   │   ├── memory.py
│   │   └── vector_memory.py
│   ├── tts/            # Text-to-Speech engine
│   └── main.py         # Entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Configuration

- **Model Selection**: To change the LLM model, edit `voice_agent/llm/local_llm.py` and update the `"model"` field in the payload (e.g., to `llama3`, `mistral`, etc.).
- **Recording Duration**: Adjust the `duration` parameter in `voice_agent/main.py` to change how long the assistant listens.

## License

[MIT License](LICENSE)
