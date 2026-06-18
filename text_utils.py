def chunk_text(text, chunk_size=500, overlap=100):
    i = 0
    chunks = []
    size = len(text)

    while(i<size):
        if i + chunk_size >= size:
            chunks.append(text[i:size])
            break
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap

    return chunks