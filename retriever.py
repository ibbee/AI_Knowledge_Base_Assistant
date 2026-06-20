from service import get_index,get_embeddings
import numpy as np

def retrieve_chunks(question,top_k=3):
    embedding = get_embeddings(question)
    index = get_index(len(embedding),"vector_store/document_index.faiss")

    _, I = index.search(np.array([embedding]).astype('float32'),top_k)

    return I[0].tolist()