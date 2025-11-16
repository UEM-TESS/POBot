def chunk_text(text, max_words=1500):
    words = text.split()
    chunks = []
    buffer = []

    for word in words:
        buffer.append(word)
        if len(buffer) >= max_words:
            chunks.append(" ".join(buffer))
            buffer = []

    if buffer:
        chunks.append(" ".join(buffer))

    return chunks
