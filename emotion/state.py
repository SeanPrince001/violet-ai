import json
from pathlib import Path

EMOTION_FILE = Path("emotion/emotion_state.json")


DEFAULT_STATE = {
    "trust": 0.4,
    "warmth": 0.5,
    "attachment": 0.3,
    "curiosity": 0.7,
    "sadness": 0.1
}


def load_emotion_state():
    """
    Load emotional state from disk.
    """

    if not EMOTION_FILE.exists():
        save_emotion_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

    with open(EMOTION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_emotion_state(state):
    """
    Save emotional state to disk.
    """

    with open(EMOTION_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)


emotion_state = load_emotion_state()