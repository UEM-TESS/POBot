import json

def read_file(file_name: str) -> str:
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

def save_json_file(file_name: str, result: dict):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)