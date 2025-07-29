'''
import psycopg2
import numpy as np
import pipeline
from connect import PostgresConnect
from sentence_transformers import SentenceTransformer
import torch
import ast

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

    similarity = []
    for row in rows:
        id = row[0]
        chunk = row[1]
        vector_db = row [2]     
        vt = np.array(ast.literal_eval(vector_db), dtype=np.float32)
        score = np.dot(query, vt) / (np.linalg.norm(query) * np.linalg.norm(vt))

        similarity.append((score, id, chunk))

    similarity. sort(reverse = True)

    return similarity[0:5]
   
if __name__ == "__main__":
    text = "thế nào là học máy"
    sol = pipeline.Solution()
    con = PostgresConnect()
    text = sol.preprocessing(text)
    cur = con.cur
    top_k = psql_query(cur, text)
    print(top_k)
    con.close()

'''

from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import genativeAI
from genativeAI import tokenizer

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever



#model = SentenceTransformer("AITeamVN/Vietnamese_Embedding")
embedding_model = HuggingFaceEmbeddings(model_name="AITeamVN/Vietnamese_Embedding")

vector_store = FAISS.load_local(
    "faiss_index",
    #embeddings=model.encode,
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)
def answer(question):
    top_2 = []
    #question = "làm thế nào để xử lý ảnh nhận diện biển số xe"
    docs = vector_store.similarity_search(question, k=10)

    retriever = BM25Retriever.from_documents(docs)
    results = retriever.invoke(question)

    #print(len(results))


    for result in results[0:2]:
        prompt = f"""Câu hỏi: {question}

        Dữ liệu: {result.page_content}

        Trả lời:"""
        gens = genativeAI.gen(prompt)
        
        gen_text = tokenizer.decode(gens[0], skip_special_tokens=True)
        top_2.append((gen_text, result.metadata))

        #print(gen_text)
        #print('----------------------------------------')
    return top_2 

'''       
if __name__ == "__main__":
    question = 'làm thế nào để xử lý ảnh nhận diện biển số xe'
    ans = answer(question)
    print(ans)        
'''


'''
    for result in results:
        #print(result)
        result.page_content = str(result.page_content)

        gens = genativeAI.gen(result.page_content)
        #print(gens)
        
        #for i, gen in enumerate(gens):
        #    print(">> Generated text {}\n\n{}".format(i + 1, tokenizer.decode(gen.tolist())))
        #    print('\n---')
        print(len(gens))

        for i, gen in enumerate(gens):
            gen_text = tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
            print(f'gentext {i} : {gen_text}')
            print('----------------------------------------')

'''


