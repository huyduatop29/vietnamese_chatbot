from langchain_unstructured import UnstructuredLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from unstructured.cleaners.core import clean_extra_whitespace
from sentence_transformers import SentenceTransformer

from typing import list 
from unstructured.documents.elements import Element

import torch
import os
import re 
import connect


from collections import Counter, defaultdict
import string
con = connect.PostgresConnect()

model = SentenceTransformer("AITeamVN/Vietnamese_Embedding")
model_kwargs = {'device' : 'cpu'}
model.max_seq_length = 2048

class Solution:
    def remove_footer_elements(self, elements: List[Element]) -> List[Element]:
        filtered = []
        for el in elements:
            text = el.text.strip()        
            if not re.match(r"^Page \d+ of \d+$", text) and "Confidential" not in text:
                filtered.append(el)
    return filtered

    def clean_word(self, w: str) -> str:
        letters = set('aáàảãạăaáàảãạăắằẳẵặâấầẩẫậbcdđeéèẻẽẹêếềểễệfghiíìỉĩịjklmnoóòỏõọôốồổỗộơớờởỡợpqrstuúùủũụưứừửữựvwxyýỳỷỹỵz0123456789')
        new_w = ''
        for letter in w:
            if letter.lower() in letters or letter == '.':
                new_w += letter.lower()
        return new_w
    
    def preprocessing(self, doc:str) -> str:
        doc = doc.replace('\n', ' ').replace('==', ' ')
        words = doc.split()
        cleaned_words = [self.clean_word(word) for word in words]
        new_doc = ' '.join(cleaned_words)
        return new_doc
    

    def Pull_Data(self, folder_path: str):
        file_path = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
    
        for file in file_path:
            docs = []
            loader_doc = UnstructuredLoader(file)
            loader_chunk = UnstructuredLoader(
                file,
                post_processors=[
                    self.remove_footer_elements,
                    clean_extra_whitespace
                ],
                chunking_strategy = "basic",
                max_characters = 500,
                include_orig_elements = False,
            )
            docs = loader_chunk.load()
            #print(f'doc = {docs}')

            embeddings = []
            for doc in docs:
                doc.page_content = self.preprocessing(doc.page_content)
                embedding = model.encode(doc.page_content)
                embeddings.append(embedding)
                #print(f'embedding = {embedding}') 
            
            con.upload(docs,embeddings)


'''
if __name__ == "__main__":
    folder_path = '/home/quochuy/Development/Rag/Data_test'
    solution = Solution()
    con = connect.PostgresConnect()
    con.__init__()
    solution.Pull_Data(folder_path)

    print(texts[0:10])
    print(embeddings[0:10])
    print(documents[0:10])
'''

    


    


    


