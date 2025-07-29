import psycopg2
import numpy as np
import faiss
import ast

from decouple import config
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def UpFaiss():
    conn = psycopg2.connect(
        dbname=config('NAME'),
        user=config('USER'),
        password=config('PASSWORD'),
        host=config('HOST', default='localhost'),
        port=config('PORT', default='5432'),
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT e.id, e.vector_data, c.page_content
        FROM embeddings AS e
        JOIN chunks AS c ON e.chunk_id = c.id
        ORDER BY e.id ASC;
    """)
    rows = cur.fetchall()

    chunk_ids = []
    vectors = []
    page_contents = []

    for row in rows:
        chunk_ids.append(row[0])
        vectors.append(row[1] if isinstance(row[1], list) else ast.literal_eval(row[1]))
        page_contents.append(row[2])

    if not vectors:
        return None

    vectors_np = np.array(vectors, dtype='float32')
    chunk_ids_np = np.array(chunk_ids)

    dim = vectors_np.shape[1]
    base_index = faiss.IndexFlatL2(dim)
    index = faiss.IndexIDMap(base_index)
    index.add_with_ids(vectors_np, chunk_ids_np)

    documents = [
        Document(page_content=content, metadata={"chunk_id": chunk_id})
        for chunk_id, content in zip(chunk_ids, page_contents)
    ]

    docstore = InMemoryDocstore({
        str(chunk_id): doc for chunk_id, doc in zip(chunk_ids, documents)
    })

    vector_store = FAISS(
        embedding_function=None,
        index=index,
        docstore=docstore,
        index_to_docstore_id={
            i: str(chunk_ids[i]) for i in range(len(chunk_ids))
        }
    )

    cur.close()
    conn.close()
    print(f"Đã khởi tạo FAISS index với {len(chunk_ids)} vectors.")
    vector_store.save_local("faiss_index")
    return vector_store

if __name__ == "__main__":
    UpFaiss()


