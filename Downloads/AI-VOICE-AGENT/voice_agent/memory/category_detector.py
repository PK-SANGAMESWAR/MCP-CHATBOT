def detect_category(text):
    text_l = text.lower()

    # PERSONAL
    if any(x in text_l for x in ["my name is", "i am", "i live in", "my birthday", "my age is"]):
        return "personal"

    # WORK
    if any(x in text_l for x in ["i work at", "my job", "my role is", "i am a", "company"]):
        return "work"

    # PREFERENCES
    if any(x in text_l for x in ["i like", "i love", "my favorite", "i prefer"]):
        return "preferences"

    # TASKS
    if any(x in text_l for x in ["remind me", "i need to", "i must", "task", "to-do"]):
        return "tasks"

    return None
