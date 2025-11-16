import json

from common.file_utils import read_file, save_json_file


def test_read_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_content = "Olá, mundo!"
    file_path.write_text(file_content, encoding="utf-8")

    result = read_file(str(file_path))

    assert result == file_content


def test_save_json_file(tmp_path):
    file_path = tmp_path / "data.json"
    data = {"nome": "Leonardo", "idade": 18}

    save_json_file(str(file_path), data)

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data
