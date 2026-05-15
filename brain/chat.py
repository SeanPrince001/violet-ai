import requests
from memory.memory import save_memory, get_memories

from emotion.state import (
    emotion_state,
    save_emotion_state
)

# Load Violet personality profile
with open("character/violet_profile.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Short-term conversation history
conversation_history = []


def generate_internal_thought(user_message):
    """
    Generate hidden internal reasoning.
    """

    thought_prompt = f"""
You are Violet's internal thoughts.

Analyze the emotional meaning behind the user's message.

Think carefully about:
- emotional tone
- hidden feelings
- appropriate emotional response
- relationship context
- empathy
- emotional nuance

Keep thoughts short and reflective.

User: {user_message}

Internal Thought:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": thought_prompt,
            "stream": False,
            "options": {
                "temperature": 0.6,
                "top_p": 0.9,
                "num_predict": 60,
                "num_ctx": 1024
            }
        }
    )

    data = response.json()

    return data["response"].strip()


def build_prompt(user_message, internal_thought):
    # Retrieve relevant memories
    memories = get_memories(user_message)

    memory_text = "\n".join(memories)

    # Keep recent conversation short for speed
    history = "\n".join(conversation_history[-6:])

    # Build final prompt
    prompt = f"""
{SYSTEM_PROMPT}

Relevant Memories:
{memory_text}

Recent Conversation:
{history}

Current Emotional State:
Trust: {emotion_state['trust']}
Warmth: {emotion_state['warmth']}
Attachment: {emotion_state['attachment']}
Curiosity: {emotion_state['curiosity']}
Sadness: {emotion_state['sadness']}

Internal Reflection:
{internal_thought}

Behavior Instructions:
- Speak carefree and cheerful
- Be emotionally empathetic and caring
- Respond with slang and exaggerated reactions when necessary
- Prioritize sincerity and emotional understanding
- Respond cheery and gently
- Change personality accordingly
- Never break character

User: {user_message}
Violet:
"""

    return prompt


def chat(user_message):
    # Generate hidden internal reasoning
    internal_thought = generate_internal_thought(user_message)

    # Build final response prompt
    prompt = build_prompt(
        user_message,
        internal_thought
    )

    # Send request to Ollama with streaming enabled
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.72,
                "top_p": 0.9,
                "num_predict": 120,
                "num_ctx": 2048,
                "num_thread": 8
            }
        },
        stream=True
    )

    full_reply = ""

    print("\nViolet: ", end="", flush=True)

    # Stream response chunks
    for line in response.iter_lines():
        if line:
            chunk = line.decode("utf-8")

            try:
                data = requests.models.complexjson.loads(chunk)

                token = data.get("response", "")

                print(token, end="", flush=True)

                full_reply += token

            except Exception:
                pass

    print("\n")

    # Save recent conversation history
    conversation_history.append(f"User: {user_message}")
    conversation_history.append(f"Violet: {full_reply}")

    # Save important memory
    save_memory(user_message)

    # Emotional progression system
    emotion_state["trust"] = min(
        1.0,
        emotion_state["trust"] + 0.01
    )

    emotion_state["attachment"] = min(
        1.0,
        emotion_state["attachment"] + 0.008
    )

    emotion_state["warmth"] = min(
        1.0,
        emotion_state["warmth"] + 0.005
    )

    # Persist emotional state
    save_emotion_state(emotion_state)

    return full_reply


# Terminal chat loop
if __name__ == "__main__":
    print("Violet AI is running.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("\nGoodbye.\n")
            break

        chat(user_input)