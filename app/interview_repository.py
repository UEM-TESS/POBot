import uuid

import psycopg2

from app import config
from common import logger

connection = psycopg2.connect(
    dbname=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT
)


def insert_interview(description: str, transcription: str, total_chuncks: int, size_chunks: int):
    id_interview = str(uuid.uuid4())
    sql = "insert into interview(id, description,datetime,content,language,total_chunks,size_chunks) values(%s,%s,current_timestamp,%s,'PT-BR',%s,%s)"
    valores = (id_interview, description, transcription, total_chuncks, size_chunks)
    cursor = connection.cursor()
    cursor.execute(sql, valores)
    connection.commit()
    return id_interview


def insert_interview_model(id_interview: uuid.UUID, model_name: str, tokens_max: int, temperature: float,
                           time_spent: float):
    id_model = str(uuid.uuid4())
    sql = "insert into interview_model (id,interview_id,model_name,result_generated,tokens_count,tokens_max,temperature,time_spent ) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    valores = (id_model, id_interview, model_name, "", 99, tokens_max, temperature, time_spent)
    cursor = connection.cursor()
    cursor.execute(sql, valores)
    connection.commit()
    return id_model


def insert_story(interview_model_id: int, stories):
    # Insere dados story
    sql = "insert into story (id,interview_model_id ,number,description,evidence,story_name,similaridade) values(%s,%s,%s,%s,%s,%s,%s)"
    story_number = 0
    logger.log("Início da inserção de stories")
    for story in stories:
        story_number += 1
        print("Story n ", story_number)
        id_story = str(uuid.uuid4())
        valores = (id_story, interview_model_id, story_number, story.get("descricao"), story.get("evidencia"),
                   story.get("titulo"), 0)
        cursor = connection.cursor()
        cursor.execute(sql, valores)
    logger.log("Fim da inserção de stories")
    connection.commit()


def save_result(interview_title: str, interview_description: str, model_name: str, tokens_max: int,
                temperature: float, chunks: int, chunk_size: int, data_stories: dict, elapsed_seconds: float):
    id_interview = insert_interview(interview_title, interview_description, chunks, chunk_size)
    id_model_interview = insert_interview_model(id_interview, model_name, tokens_max, temperature, elapsed_seconds)
    stories = data_stories.get("stories", [])
    insert_story(id_model_interview, stories)
