import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_core.documents import Document  # Importando a classe Document
from models import Models

# Função para inicializar os modelos
def initialize_embeddings():
    models = Models()
    return models.embeddings_ollama

# Função para inicializar o armazenamento vetorial (Chroma)
def initialize_vector_store(embeddings):
    return Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory="./db/chroma_langchain_db",
    )

# Função para processar um arquivo .md
def ingest_file(file_path, vector_store):
    if not file_path.lower().endswith('.md'):
        print(f'Pulando arquivos que não são Markdown: {file_path}')
        return False

    print(f'Iniciando ingestão: {file_path}')
    loader = TextLoader(file_path, encoding="utf-8")
    loaded_documents = loader.load()

    # Processar cada documento
    documents = []
    for doc in loaded_documents:
        text = doc.page_content
        metadata = extract_metadata(file_path)
        new_doc = Document(page_content=text, metadata=metadata)  # Corrigido: criação do Document
        documents.append(new_doc)

    # Dividir os documentos em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunked_documents = text_splitter.split_documents(documents)

    # Adicionar documentos ao vetor
    uuids = [str(uuid4()) for _ in range(len(chunked_documents))]
    vector_store.add_documents(documents=chunked_documents, ids=uuids)
    
    print(f'Ingestão finalizada: {file_path}')
    return True

# Função para extrair metadados do caminho do arquivo
def extract_metadata(file_path):
    partes = file_path.replace("\\", "/").split("/")
    metadata = {}
    if len(partes) >= 2:
        metadata["servico"] = partes[-2]
        metadata["comando"] = partes[-1].replace(".md", "")
    return metadata

# Função principal para iniciar o processo de ingestão
def main_loop():
    embeddings = initialize_embeddings()
    vector_store = initialize_vector_store(embeddings)
    
    while True:
        mds = [f for f in os.listdir('./data') if f.endswith(".md") and not f.startswith("_")]
        if not mds:
            print("Nenhum novo arquivo Markdown encontrado. Encerrando.")
            break

        for filename in mds:
            file_path = os.path.join('./data', filename)
            if ingest_file(file_path, vector_store):
                new_filename = "_" + filename
                os.rename(file_path, os.path.join('./data', new_filename))

            time.sleep(10)  # Pausa entre processamentos

# Executando o processo
if __name__ == "__main__":
    main_loop()
