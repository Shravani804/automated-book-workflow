from db.chroma_store import save_version, search_similar
from pathlib import Path

# Save all versions with UTF-8 decoding
save_version("chapter1", "original", Path("data/chapter1.txt").read_text(encoding="utf-8"))
save_version("chapter1", "spun", Path("data/chapter1_spun.txt").read_text(encoding="utf-8"))
save_version("chapter1", "reviewed", Path("data/chapter1_reviewed.txt").read_text(encoding="utf-8"))
save_version("chapter1", "final", Path("data/chapter1_final.txt").read_text(encoding="utf-8"))

# Search similar content
print("\n🔍 Searching...")
results = search_similar("polished version with storytelling")
for i, doc in enumerate(results["documents"][0], start=1):
    print(f"\nResult {i}:\n", doc[:300], "...\n")
