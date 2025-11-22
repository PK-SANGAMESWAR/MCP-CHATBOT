import pyttsx3

engine = pyttsx3.init()

import time

def speak(text):
    print("🔊 Speaking...")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.4)   # give Windows audio driver time to release device

