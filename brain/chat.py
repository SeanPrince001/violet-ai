import requests
from memory.memory import save_memory, get_memories

# Load Violet personality profile
with open("character/violet_profile.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Short-term conversation history
conversation_history = []


def build_prompt(user_message):
    # Retrieve relevant memories
    memories = get_memories(user_message)

    memory_text = "\n".join(memories)

    # Keep recent conversation small for speed
    history = "\n".join(conversation_history[-6:])

    # Build final prompt
    prompt = f"""
{SYSTEM_PROMPT}

Relevant Memories:
{memory_text}

Recent Conversation:
{history}

User: {user_message}
Violet:
"""

    return prompt


def chat(user_message):
    prompt = build_prompt(user_message)

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

    # Read streamed chunks from Ollama
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

    # Save user message into long-term memory
    save_memory(user_message)

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