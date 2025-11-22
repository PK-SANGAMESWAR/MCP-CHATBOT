from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

EMOTIONS = [
    "anger",
    "disgust",
    "fear",
    "joy",
    "neutral",
    "sadness",
    "surprise"
]

def detect_emotion(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    scores = torch.softmax(outputs.logits, dim=1).detach().numpy()[0]

    top_idx = np.argmax(scores)
    emotion = EMOTIONS[top_idx]
    confidence = round(float(scores[top_idx]), 3)

    return emotion, confidence
