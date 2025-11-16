import time

from app import interview_repository
from app import user_story_service, const
from common import logger, file_utils


def analyze_model(model: const.Models, interview_file: str, transcription: str):
    logger.log(f"Inicio {model.name}...")
    chunk_size = 1100
    start = time.perf_counter()
    data_stories, chunks_count = user_story_service.create_user_stories(model.name,
                                                                        interview_file, chunk_size)
    end = time.perf_counter()
    elapsed_seconds = end - start
    interview_repository.save_result(interview_file, transcription, const.Models.QWEN_25_7B.name,
                                     4096, 0.5, chunks_count, chunk_size, data_stories, elapsed_seconds)
    logger.log(f"Fim modelo")
    logger.log(f"=======================================")


def main():
    for interview_file in const.INTERVIEWS_FILES:
        transcription = file_utils.read_file(interview_file)

        analyze_model(const.Models.QWEN_25_7B, interview_file, transcription)
        # analyze_model(const.Models.QWEN_2_5_3B, interview_file, transcription)
        # analyze_model(const.Models.PHI_4_3B, interview_file, transcription)
        # analyze_model(const.Models.META_LLAMA_3_1_8B, interview_file, transcription)
        # analyze_model(const.Models.META_LLAMA_3_2_1B, interview_file, transcription)
        # analyze_model(const.Models.META_LLAMA_3_2_3B, interview_file, transcription)

    logger.log(f"💾 Processo concluído.")
