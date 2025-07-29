import numpy as np 
import pipeline
from connect import PostgresConnect
from sentence_transformers import SentenceTransformers
import torch
import ast 
import faiss


model = SentenceTransformer("AITeamVN/Vietnamese_Embedding")
model_kwargs = {'device' : 'cpu'}
model.max_seq_length = 2048

def psql_query(cur, text_query : str) -> list:
    cur.execute("""
        select c.id , c.page_content, e.vector_data 
        from embeddings as e 
        join chunks as c on c.id = e.chunk_id 
        order by c.id asc; 
    """)
    rows = cur.fetchall()
    query = model.encode(text_query)
    query = np.array(query)    


