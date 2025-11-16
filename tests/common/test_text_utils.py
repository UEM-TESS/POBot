from common.text_utils import chunk_text


def test_chunk_text_empty():
    """Should return an empty list when input text is empty."""
    result = chunk_text("", max_words=1500)
    assert result == []


def test_chunk_text_less_than_max_words():
    """Should return a single chunk when text has fewer words than max."""
    text = "word " * 10  # 10 words
    result = chunk_text(text, max_words=1500)
    assert len(result) == 1
    assert len(result[0].split()) == 10


def test_chunk_text_exact_max_words():
    """Chunk should contain exactly max_words words."""
    max_words = 5
    text = "one two three four five"
    result = chunk_text(text, max_words=max_words)
    assert len(result) == 1
    assert len(result[0].split()) == max_words


def test_chunk_text_multiple_chunks():
    """Should split into multiple chunks of max_words size."""
    max_words = 3
    text = "one two three four five six seven"
    # Words = 7 → chunks: ["one two three", "four five six", "seven"]
    result = chunk_text(text, max_words=max_words)

    assert len(result) == 3
    assert result[0] == "one two three"
    assert result[1] == "four five six"
    assert result[2] == "seven"


def test_chunk_text_preserves_order():
    """Words should remain in the exact same order."""
    max_words = 2
    text = "alpha beta gamma delta"
    result = chunk_text(text, max_words=max_words)
    assert result == ["alpha beta", "gamma delta"]


def test_chunk_text_last_chunk_smaller():
    """Last chunk can have fewer words than max_words."""
    text = "one two three four"
    result = chunk_text(text, max_words=3)
    assert len(result) == 2
    assert result[0] == "one two three"
    assert result[1] == "four"
