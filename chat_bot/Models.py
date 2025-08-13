import os
from langchain_ollama import OllamaEmbeddings, ChatOllama


class Models:
    """
    Classe para inicializar e gerenciar os modelos de embeddings e linguagem.
    """

    def __init__(self):
        # Inicializa o modelo de embeddings Ollama para vetorização de texto
        self.embeddings_ollama = OllamaEmbeddings(
            model="bge-m3"  # Nome do modelo de embeddings utilizado
        )

        # Inicializa o modelo de linguagem Ollama para geração de respostas
        self.model_ollama = ChatOllama(
            model="llama3.2",  # Nome do modelo de linguagem utilizado
            temperature=0.6  # Controla a aleatoriedade das respostas geradas
        )