import chromadb
import uuid

client = chromadb.PersistentClient(path="memory_db")

collection = client.get_or_create_collection(
    name="violet_memory"
)


def is_important_memory(text):
    """
    Determines whether a message is important enough
    to save into long-term memory.
    """

    important_keywords = [
        "love",
        "sad",
        "happy",
        "afraid",
        "dream",
        "memory",
        "lonely",
        "friend",
        "family",
        "hurt",
        "important",
        "future",
        "goal",
        "relationship",
        "trust",
        "fear",
        "cry",
        "pain",
        "emotion"
    ]

    text_lower = text.lower()

    for keyword in important_keywords:
        if keyword in text_lower:
            return True

    # Save longer meaningful messages
    if len(text.split()) > 12:
        return True

    return False


def save_memory(text):
    """
    Save only important memories.
    """

    if not is_important_memory(text):
        return

    collection.add(
        documents=[text],
        ids=[str(uuid.uuid4())]
    )


def get_memories(query, n_results=3):
    """
    Retrieve relevant memories.
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results["documents"][0]