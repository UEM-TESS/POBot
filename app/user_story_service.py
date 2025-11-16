from concurrent.futures import ThreadPoolExecutor, as_completed

from app import config
from app import processor
from common import text_utils, file_utils
from common.logger import log


def create_user_stories(model, file_name, chunk_size):
    log("📄 Lendo arquivo...")
    text = file_utils.read_file(file_name)

    log(f"✂️ Dividindo em chunks {chunk_size} words...")
    chunks = text_utils.chunk_text(text, max_words=chunk_size)
    total_chunks = len(chunks)
    log(f"📌 Total de chunks: {total_chunks}")

    all_stories = []

    with ThreadPoolExecutor(max_workers=config.THREADS) as executor:
        futures = {
            executor.submit(processor.process_chunk, chunk, i + 1, total_chunks, model): i
            for i, chunk in enumerate(chunks)
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                all_stories.extend(result)

    #    log("🧹 Removendo duplicatas...")
    #   all_stories = deduplicate_stories(all_stories)

    log(f"🎉 Total final de User Stories: {len(all_stories)}")

    return {"stories": all_stories}, total_chunks
