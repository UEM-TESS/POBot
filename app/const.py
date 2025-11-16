from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ModeloInfo:
    name: str
    temperature: float
    descricao: str


class Models(Enum):
    QWEN_25_7B = ModeloInfo(
        name="qwen/qwen2.5-7b-instruct",
        temperature=0.5,
        descricao="Qwen 2.5 - 7B Instruct"
    )
    PHI_4_3B = ModeloInfo(
        name="microsoft/phi-4-mini-reasoning",
        temperature=0.5,
        descricao="phi 4 - Mini Reasoning 3B Instruct"
    )
    QWEN_2_5_3B = ModeloInfo(
        name="lmstudio-community/Qwen2.5-3B-Instruct-GGUF",
        temperature=0.5,
        descricao="Qwen 2.5 - 3B Instruct"
    )
    META_LLAMA_3_1_8B = ModeloInfo(
        name="meta-llama/Meta-Llama-3.1-8B-Instruct",
        temperature=0.5,
        descricao="Meta Llama - 3.1-8B Instruct"
    )
    META_LLAMA_3_2_1B = ModeloInfo(
        name="meta-llama/Llama-3.2-1B-Instruct",
        temperature=0.5,
        descricao="Meta Llama - 3.2-1B Instruct"
    )
    META_LLAMA_3_2_3B = ModeloInfo(
        name="meta-llama/Llama-3.2-3B-Instruct",
        temperature=0.5,
        descricao="Meta Llama - 3.2-3B Instruct"
    )


INTERVIEWS_FILES = ["./resources/interviews/teste.txt"
                    #   ,"./resources/interviews/sistema_gestao_clinica_veterinaria.txt",
                    #   ,"./resources/interviews/sistema_telemarketing.txt"
                    ]

SYSTEM_PROMPT = """
Você é Product Owner de Software.
Crie User Stories usando o formato Agile: Como..., Quero..., Para que...
Inclua também a evidência literal do trecho analisado.
"""

JSON_FORMAT_STORIES = {
    "type": "json_schema",
    "json_schema": {
        "name": "stories_output",
        "schema": {
            "type": "object",
            "properties": {
                "stories": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "titulo": {"type": "string"},
                            "descricao": {"type": "string"},
                            "evidencia": {"type": "string"}
                        },
                        "required": ["titulo", "descricao", "evidencia"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["stories"],
            "additionalProperties": False
        }
    }
}
