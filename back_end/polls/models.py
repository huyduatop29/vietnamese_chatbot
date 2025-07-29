from django.db import models
from pgvector.django import VectorField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chunk_id = models.IntegerField(null=True, blank=True)  
    def __str__(self):
        return f"Chat by {self.user.username} at {self.created_at}"
    class Meta:
        db_table = 'chat_historys'

class Document(models.Model):
    filename = models.TextField()
    file_directory = models.TextField()
    source = models.TextField()
    last_modified = models.DateTimeField()
    filetype = models.TextField()
    languages = ArrayField(
        models.TextField(),
        blank=True,
        default=list
    )
    def __str__(self):
        return self.filename
    class Meta:
        db_table = 'documents'


class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    page_number = models.IntegerField(null=True, blank=True)
    element_id = models.TextField(null=True, blank=True)
    page_content = models.TextField()

    def __str__(self):
        return f"Chunk {self.id} - Doc {self.document_id}"
    class Meta:
        db_table = 'chunks'



class EmphasizedText(models.Model):
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE, related_name="emphasized_texts")
    content = models.TextField()
    tag = models.TextField()

    def __str__(self):
        return f"Emphasis {self.tag} on chunk {self.chunk_id}"
    class Meta:
        db_table = 'emphasized_text'


class Embedding(models.Model):
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE, related_name="embedding")
    vector_data = VectorField(dimensions=1024)

    def __str__(self):
        return f"Embedding for chunk {self.chunk_id}"
    class Meta:
        db_table = 'embeddings'



