import ollama
import faiss
import numpy as np

def generate_embedding(text):
    return ollama.embed(
        model="nomic-embed-text",
        input=text
    )['embeddings'][0]

def create_index(dimensions):
    return faiss.IndexFlatL2(dimensions)

def add_embeddings(index, embeddings):
    index.add(np.asarray(embeddings,dtype=np.float32))