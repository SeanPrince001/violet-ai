def update_emotions(user_message, emotion_state):
    """
    Dynamically adjust emotions based on user input.
    """

    text = user_message.lower()

    positive_words = [
        "thank you",
        "thanks",
        "love",
        "appreciate",
        "happy",
        "kind",
        "care",
        "friend"
    ]

    negative_words = [
        "hate",
        "annoying",
        "stupid",
        "leave",
        "angry",
        "mad",
        "idiot"
    ]

    vulnerable_words = [
        "sad",
        "lonely",
        "afraid",
        "hurt",
        "cry",
        "depressed",
        "tired",
        "anxious"
    ]

    # Positive emotional effects
    for word in positive_words:
        if word in text:
            emotion_state["trust"] += 0.03
            emotion_state["warmth"] += 0.02
            emotion_state["attachment"] += 0.025

    # Negative emotional effects
    for word in negative_words:
        if word in text:
            emotion_state["trust"] -= 0.04
            emotion_state["warmth"] -= 0.03

    # Emotional vulnerability effects
    for word in vulnerable_words:
        if word in text:
            emotion_state["attachment"] += 0.02
            emotion_state["warmth"] += 0.015

    # Clamp values safely
    for key in emotion_state:
        emotion_state[key] = max(
            0.0,
            min(1.0, emotion_state[key])
        )

    return emotion_state