import json
import os

MEMORY_FILE = "memory/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"user_profile": {}, "conversation_history": []}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def add_to_history(memory, role, text):
    memory["conversation_history"].append({"role": role, "text": text})
    # keep only last 10 messages to avoid huge prompts
    memory["conversation_history"] = memory["conversation_history"][-10:]
    save_memory(memory)

def update_user_profile(memory, key, value):
    memory["user_profile"][key] = value
    save_memory(memory)
