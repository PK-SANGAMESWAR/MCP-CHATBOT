import requests
from datetime import datetime

# memory components
from memory.memory import load_memory, add_to_history, update_user_profile
from memory.vector_memory import add_memory, search_memory
from memory.category_detector import detect_category
from memory.emotion_detector import detect_emotion


def generate_reply(user_text):

    memory = load_memory()

    # 1. Detect emotion
    emotion, conf = detect_emotion(user_text)

    # Store emotion if confidence is high
    if conf > 0.6:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        emotion_text = (
            f"At {timestamp}, user seemed {emotion} "
            f"(confidence {conf}) after saying: '{user_text}'"
        )
        add_memory(emotion_text, "emotion")

    # 2. Detect semantic category
    category = detect_category(user_text)
    if category:
        add_memory(user_text, category)

        # store user name
        if category == "personal" and "my name is" in user_text.lower():
            name = user_text.split("is")[-1].strip()
            update_user_profile(memory, "name", name)

    # 3. Retrieve emotional memory
    emotional_context = search_memory("emotion", k=5)
    
    emotion_strings = []
    for m in emotional_context:
        if isinstance(m, dict):
            emotion_strings.append(m.get("text", ""))
        else:
            emotion_strings.append(str(m))

    emotional_lines = "\n".join(emotion_strings)

    # 4. Retrieve semantic memory
    retrieved = search_memory(user_text, k=5)

    retrieval_strings = []
    for m in retrieved:
        if isinstance(m, dict):
            retrieval_strings.append(f"[{m.get('category','unknown')}] {m.get('text','')}")
        else:
            retrieval_strings.append(f"[unknown] {str(m)}")

    retrieved_lines = "\n".join(retrieval_strings)

    # 5. Conversation history
    history = ""
    for h in memory["conversation_history"]:
        history += f"{h['role']}: {h['text']}\n"

    # 6. Build prompt
    prompt = f"""
You are an emotionally intelligent AI assistant.

Conversation history:
{history}

Relevant long-term memories:
{retrieved_lines}

Emotional memories:
{emotional_lines}

User profile:
{memory['user_profile']}

User says:
{user_text}

Emotion detected: {emotion} (confidence {conf})

Your goals:
1. Respond empathetically.
2. Use emotional memory when helpful.
3. Use personal/work/preferences/tasks memory when relevant.
4. Be supportive, warm and helpful.

Assistant:
"""

    # 7. Query Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False}
    ).json()

    assistant_reply = response.get("response", "").strip()

    # 8. Save conversation
    add_to_history(memory, "User", user_text)
    add_to_history(memory, "Assistant", assistant_reply)

    return assistant_reply
