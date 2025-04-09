import os
from langchain_ollama import OllamaEmbeddings, ChatOllama


class Models:
    def __init__(self):
        self.embeddings_ollama = OllamaEmbeddings(
            model="bge-m3"
        )

        self.model_ollama = ChatOllama(
            model="llama3.1:8b",
            temperature=0
        )