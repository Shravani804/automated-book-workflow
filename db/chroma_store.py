import chromadb
from pathlib import Path
from uuid import uuid4

# Create persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="chromadb_store")

# Create or load the collection
collection = chroma_client.get_or_create_collection(name="chapter_versions")

def save_version(chapter_id: str, stage: str, content: str, reward: float = 0.0) -> str:
    version_id = f"{chapter_id}_{stage}_{uuid4()}"
    collection.add(
        documents=[content],
        ids=[version_id],
        metadatas=[{
            "chapter": chapter_id,
            "stage": stage,
            "reward": reward
        }]
    )
    print(f"✅ Stored: {version_id}")
    return version_id

def search_similar(query: str, top_k: int = 3):
    return collection.query(query_texts=[query], n_results=top_k)

def get_best_version(chapter_id: str) -> str:
    results = collection.get(
        where={"chapter": chapter_id},
        include=["documents", "metadatas", "ids"]
    )
    best = sorted(
        zip(results['documents'], results['metadatas']),
        key=lambda x: x[1].get('reward', 0),
        reverse=True
    )[0]
    return best[0]
