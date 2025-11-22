from audio.record import record_audio
from asr.whisper_asr import transcribe_audio
from llm.local_llm import generate_reply
from tts.tts_engine import speak

def main():
    print("\n=== AI Assistant with Memory ===")

    while True:
        print("\nSpeak after the beep...")

        wav_path = record_audio(duration=4)
        user_text = transcribe_audio(wav_path)

        if not user_text.strip():
            print("Didn't hear anything, try again.")
            continue

        print("You:", user_text)

        reply = generate_reply(user_text)
        print("Assistant:", reply)

        speak(reply)

if __name__ == "__main__":
    main()
