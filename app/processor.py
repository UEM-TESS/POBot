import json
from common.logger import log
from app import const, config
from openai import OpenAI

client = OpenAI(
    base_url=config.LLM_URL,
    api_key=config.LLM_API_KEY
)


def process_chunk(chunk_text, index, total, model):
    log(f"⚙️  Processando chunk {index}/{total}...")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": const.SYSTEM_PROMPT},
                {"role": "user", "content": chunk_text}
            ],
            temperature=0.5,
            max_tokens=4096,
            response_format=const.JSON_FORMAT_STORIES
        )

        raw = response.choices[0].message.content

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            log(f"⚠️ JSON inválido no chunk {index}. Retorno bruto: {raw}")
            return []

        stories = data.get("stories", [])
        return stories

    except Exception as e:
        log(f"❌ Erro no chunk {index}: {e}")
        return []
