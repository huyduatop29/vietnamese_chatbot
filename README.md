MÔ TẢ
- Đánh giá và lựa chọn mô hình NLP phù hợp trên Hugging Face:
Tiến hành khảo sát, thử nghiệm và so sánh các mô hình embedding và generative từ thư viện Hugging Face. Dựa trên độ phù hợp ngữ cảnh tiếng Việt, tốc độ xử lý và khả năng mở rộng, lựa chọn mô hình ATeamVN/Vietnamese_Embedding để nhúng văn bản và VietAI/gpt-neo-1.3B-vietnamese-news để sinh câu trả lời.

- ây dựng pipeline xử lý văn bản với LangChain và Unstructured:
Sử dụng Unstructured để trích xuất nội dung từ tài liệu đầu vào (PDF, DOCX,...), sau đó tích hợp với LangChain để tiền xử lý, phân đoạn văn bản (chunking) theo độ dài tối ưu, nhằm phục vụ quá trình embedding và truy vấn hiệu quả.

- Embedding văn bản với mô hình tiếng Việt chuyên dụng:
Triển khai mô hình ATeamVN/Vietnamese_Embedding từ Hugging Face để chuyển các chunk văn bản thành vector ngữ nghĩa. Mô hình này được tối ưu hóa cho tiếng Việt, đảm bảo khả năng tìm kiếm ngữ nghĩa chính xác.

- hiết kế cơ sở dữ liệu và mô hình quan hệ:
Xây dựng hệ thống lưu trữ bằng PostgreSQL để quản lý thông tin gốc của các chunk và tài liệu. Thiết kế hai bảng chính: chunks chứa nội dung và metadata, embeddings chứa vector hóa và ánh xạ tới các chunk tương ứng.

- Tích hợp FAISS và PostgreSQL cho truy xuất hiệu quả:
Thực hiện ánh xạ từ cơ sở dữ liệu PostgreSQL sang FAISS để lưu trữ vector embedding cục bộ, giúp tiết kiệm tài nguyên và tăng tốc độ tìm kiếm. Dữ liệu được đồng bộ giữa database và index FAISS.

- Tìm kiếm ngữ nghĩa bằng FAISS (similarity search):
 Sử dụng kỹ thuật tìm kiếm theo độ tương đồng vector (L2 distance hoặc Cosine similarity) để truy xuất các chunk có nội dung ngữ nghĩa gần nhất với câu hỏi người dùng.

- Tìm kiếm theo từ vựng bằng BM25:
Kết hợp thêm phương pháp BM25 để tìm kiếm các chunk có mức độ tương đồng cao về mặt từ ngữ với truy vấn đầu vào, bổ trợ cho kết quả tìm kiếm ngữ nghĩa nhằm tăng độ chính xác.

-Tạo prompt đầu vào cho mô hình sinh ngôn ngữ (Generative AI):
Sau khi lấy được các đoạn văn bản phù hợp, hệ thống ghép các chunk thành ngữ cảnh đầu vào (context prompt) và truyền vào mô hình VietAI/gpt-neo-1.3B-vietnamese-news để sinh câu trả lời tiếng Việt tự nhiên, mạch lạc và có tính tham chiếu thực tiễn.

CÔNG CỤ
🧠 Mô hình học máy / NLP:

    Hugging Face Transformers – tải và fine-tune mô hình NLP

    ATeamVN/Vietnamese_Embedding – mô hình embedding tiếng Việt

    VietAI/gpt-neo-1.3B-vietnamese-news – mô hình sinh văn bản tiếng Việt (Generative AI)

🧱 Xử lý văn bản & dữ liệu:

    LangChain – xây dựng pipeline RAG (truy vấn – sinh phản hồi)

    Unstructured – tách nội dung văn bản và chunking document

    BM25 (rank_bm25) – tìm kiếm theo điểm từ khóa

📊 Lưu trữ và tìm kiếm vector:

    FAISS – xây dựng và truy vấn chỉ mục vector (Cosine / L2 similarity)

    PostgreSQL – lưu trữ document, chunk, embedding ID, metadata

    psycopg2 –  để thao tác dữ liệu với PostgreSQL

🧪 Môi trường và Framework:

    PyTorch – thực thi mô hình ngôn ngữ và embedding

    Transformers (from HuggingFace) – tokenizer và mô hình NLP

    Python – ngôn ngữ chính cho toàn bộ pipeline


KẾT QUẢ :
<img width="1913" height="924" alt="569942129_1223201279831750_8418946232681406193_n" src="https://github.com/user-attachments/assets/3f6e0626-37ba-4524-bd89-57ecd89228bb" />

