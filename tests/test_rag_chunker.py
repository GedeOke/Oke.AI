from app.rag.chunker import chunk_text


def test_chunk_text_basic():
    text = " ".join([f"word{i}" for i in range(30)])
    chunks = chunk_text(text, chunk_size=10, overlap=2)
    assert len(chunks) >= 3
    assert "word0" in chunks[0]
