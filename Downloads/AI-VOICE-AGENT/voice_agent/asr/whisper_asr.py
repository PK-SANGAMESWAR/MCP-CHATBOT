import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("small", device=device)

def transcribe_audio(path):
    print(f"📝 Transcribing on {device.upper()}...")
    result = model.transcribe(path)
    return result["text"]
