import os
import re
# Use a pipeline as a high-level helper
from transformers import pipeline

import nltk
from nltk import tokenize
from openai import OpenAI
import psycopg2
from psycopg2.extras import execute_values

client = OpenAI(
    api_key='')

def slice_text(text, max_length=500):
    """
    Slice the text into chunks with a maximum length of `max_length` tokens.
    """
    sentences = tokenize.sent_tokenize(text, language='english')
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_length:
            # If adding this sentence exceeds the max length, start a new chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding


def connect_db():
    conn = psycopg2.connect(database="postgres", user="postgres.seqkcnapvgkwqbqipqqs",
                        password="IT Web Server12", host="aws-0-ap-southeast-2.pooler.supabase.com", port=6543)
    return conn


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS text_embeddings (
                id SERIAL PRIMARY KEY,
                subject TEXT,
                chunk_id INT,
                original_text TEXT,
                embedding VECTOR(1536)
            );
        """)
        conn.commit()


def insert_embedding(conn, filename, chunk_id, original_text, embedding):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO text_embeddings (subject, chunk_id, original_text, embedding) VALUES (%s, %s, %s, %s);""",
            (filename.split("_")[0], chunk_id, original_text, embedding)
        )
        conn.commit()


def search_similar_texts(query, top_n=5):
    conn = connect_db()
    query_embedding = get_embedding(query)

    with conn.cursor() as cur:
        # Convert the query embedding to a string for PostgreSQL
        query_embedding_str = str(query_embedding).replace('{', '[').replace('}', ']')

        cur.execute(f"""
            SELECT subject, chunk_id, original_text, embedding <=> '{query_embedding_str}'::vector AS distance
            FROM text_embeddings
            ORDER BY distance ASC
            LIMIT %s;
        """, (top_n,))

        results = cur.fetchall()
        conn.close()
        for result in results:
            print(f"Subject: {result[0]}, Chunk ID: {result[1]}, Text: {result[2]}, Distance: {result[3]}")

def process_files_and_upload(folder_path):
    conn = connect_db()
    create_table(conn)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                chunks = slice_text(text, max_length=512)
                for i, chunk in enumerate(chunks):
                    embedding = get_embedding(chunk)
                    insert_embedding(conn, filename, i, chunk, embedding)

    conn.close()


if __name__ == "__main__":
    folder_path = 'subjectInfo'
    process_files_and_upload(folder_path)
    print("Embeddings generated and uploaded to PostgreSQL.")
    query = "which subject teaches data processing?"
    search_similar_texts(query, 1)

