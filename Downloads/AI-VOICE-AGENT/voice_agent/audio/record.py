import sounddevice as sd
import soundfile as sf
import tempfile
import time

def record_audio(duration=4, fs=16000):
    print("🎤 Preparing microphone...")
    time.sleep(0.3)   # allow audio driver to reset after TTS

    try:
        print("🎤 Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()   # no timeout, blocking wait

    except Exception as e:
        print("⚠ Audio device error:", e)
        print("🔁 Trying to reset audio device...")

        # Reset audio device
        sd.stop()
        time.sleep(0.5)

        print("🎤 Recording again...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()

    # Save to temp WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, audio, fs)

    return temp_file.name
