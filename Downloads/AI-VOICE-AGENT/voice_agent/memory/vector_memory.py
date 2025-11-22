import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

VECTOR_INDEX = "memory/vector_store.faiss"
META_DATA_FILE = "memory/vector_store.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS + metadata
def load_faiss():
    try:
        index = faiss.read_index(VECTOR_INDEX)
        with open(META_DATA_FILE, "rb") as f:
            metadata = pickle.load(f)  # list of {text, category}
        print("Loaded vector memory.")
    except:
        dim = 384
        index = faiss.IndexFlatL2(dim)
        metadata = []
        print("Created new vector memory.")
    return index, metadata

# Save everything
def save_faiss(index, metadata):
    faiss.write_index(index, VECTOR_INDEX)
    with open(META_DATA_FILE, "wb") as f:
        pickle.dump(metadata, f)

# Add memory with category
def add_memory(text, category):
    index, metadata = load_faiss()
    embedding = model.encode([text]).astype("float32")
    
    index.add(embedding)
    metadata.append({"text": text, "category": category})
    
    save_faiss(index, metadata)
    print(f"Stored [{category}] memory:", text)

# Search memory and keep category
def search_memory(query, k=5):
    index, metadata = load_faiss()

    if len(metadata) == 0:
        return []

    query_vec = model.encode([query]).astype("float32")
    distances, ids = index.search(query_vec, k)

    results = []
    for i in ids[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results
