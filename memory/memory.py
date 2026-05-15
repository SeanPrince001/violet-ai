import chromadb

client = chromadb.PersistentClient(path="memory_db")
collection = client.get_or_create_collection("violet_memory")


def save_memory(text):
    collection.add(
        documents=[text],
        ids=[str(hash(text))]
    )


def get_memories(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results["documents"][0]