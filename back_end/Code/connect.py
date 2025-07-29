import psycopg2
from decouple import config 
import faiss
import numpy as np
from langchain.schema import Document
from langchain.vectorstores import FAISS

class PostgresConnect:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=config('NAME'),
                user=config('USER'),
                password=config('PASSWORD'),
                host=config('HOST', default='localhost'),
                port=config('PORT', default='5432'),
            )
            self.cur = self.conn.cursor()
            print("Connected to database successfully.")
        except psycopg2.Error as e:
            print("Database connection failed.")
            raise e

    def upload(self, docs: list, embeddings: list):
        for i, doc in enumerate(docs):
            # Insert into documents
            self.cur.execute("""
                SELECT id FROM documents
                WHERE source = %s;
            """, (doc.metadata['source'],))
            existing = self.cur.fetchone()

            if existing:
                document_id = existing[0]
            else:
                self.cur.execute("""
                    INSERT INTO documents (filename, file_directory, source, last_modified, filetype, languages)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    doc.metadata['filename'],
                    doc.metadata['file_directory'],
                    doc.metadata['source'],
                    doc.metadata['last_modified'],
                    doc.metadata['filetype'],
                    doc.metadata['languages']
                ))
                document_id = self.cur.fetchone()[0]

            # Insert into chunks
            self.cur.execute("""
                INSERT INTO chunks (document_id, page_number, element_id, page_content)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (
                document_id,
                doc.metadata.get('page_number'),
                doc.metadata.get('element_id'),
                doc.page_content
            ))
            chunk_id = self.cur.fetchone()[0]

            # Insert into emphasized_text
            for content, tag in zip(
                doc.metadata.get('emphasized_text_contents', []),
                doc.metadata.get('emphasized_text_tags', [])
            ):
                self.cur.execute("""
                    INSERT INTO emphasized_text (chunk_id, content, tag)
                    VALUES (%s, %s, %s);
                """, (chunk_id, content, tag))

            # Insert into embeddings
            embedding_array = embeddings[i].tolist()
            self.cur.execute("""
                INSERT INTO embeddings (chunk_id, vector_data)
                VALUES (%s, %s);
            """, (
                chunk_id,
                embedding_array
            ))

        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

