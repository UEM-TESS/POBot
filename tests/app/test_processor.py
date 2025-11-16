import json
from unittest.mock import patch, MagicMock

from app.processor import process_chunk


# ---------------------------
# Helper para criar respostas fake
# ---------------------------
def fake_llm_response(content: str):
    mock_choice = MagicMock()
    mock_choice.message.content = content

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    return mock_response


# ---------------------------
# TESTE 1 — Resposta JSON válida
# ---------------------------
@patch("app.processor.client")
def test_process_chunk_valid_json(mock_client):
    fake_json = {
        "stories": [
            {"titulo": "A", "descricao": "B", "evidencia": "C"}
        ]
    }

    mock_client.chat.completions.create.return_value = fake_llm_response(
        json.dumps(fake_json)
    )

    result = process_chunk("texto aqui", 1, 1, model="fake-model")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["titulo"] == "A"
    assert result[0]["descricao"] == "B"
    assert result[0]["evidencia"] == "C"


# ---------------------------
# TESTE 2 — JSON inválido
# ---------------------------
@patch("app.processor.client")
def test_process_chunk_invalid_json(mock_client):
    mock_client.chat.completions.create.return_value = fake_llm_response(
        "isto não é json"
    )

    result = process_chunk("texto qualquer", 1, 1, model="fake-model")

    assert result == []


# ---------------------------
# TESTE 3 — Falha na requisição da LLM
# ---------------------------
@patch("app.processor.client")
def test_process_chunk_llm_exception(mock_client):
    mock_client.chat.completions.create.side_effect = Exception("falha na LLM")

    result = process_chunk("texto", 1, 1, model="fake-model")

    assert result == []


# ---------------------------
# TESTE 4 — Campo stories está ausente
# ---------------------------
@patch("app.processor.client")
def test_process_chunk_missing_stories(mock_client):
    fake_json = {"outro_campo": 123}
    mock_client.chat.completions.create.return_value = fake_llm_response(
        json.dumps(fake_json)
    )

    result = process_chunk("texto", 1, 1, model="fake-model")

    assert result == []


# ---------------------------
# TESTE 6 — Vários stories
# ---------------------------
@patch("app.processor.client")
def test_process_chunk_multiple_stories(mock_client):
    fake_json = {
        "stories": [
            {"titulo": "A", "descricao": "B", "evidencia": "C"},
            {"titulo": "X", "descricao": "Y", "evidencia": "Z"},
        ]
    }

    mock_client.chat.completions.create.return_value = fake_llm_response(
        json.dumps(fake_json)
    )

    result = process_chunk("texto", 1, 1, model="fake-model")

    assert len(result) == 2
    assert result[1]["titulo"] == "X"
