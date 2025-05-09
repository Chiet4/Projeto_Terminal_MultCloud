import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from uuid import uuid4
from models import Models

# Inicializando o modelo
models = Models()
embeddings = models.embeddings_ollama

# Constantes
data_folder = "./data"
chunk_size = 300
chunk_overlap = 50
chunk_interval = 10

# Armazenamento em ChromaDB
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",
)

# Ingestão de arquivos .md
def ingest_file(file_path):
    if not file_path.lower().endswith('.md'):
        print(f'Pulando arquivos que não são Markdown: {file_path}')
        return False

    print(f'Iniciando ingestão: {file_path}')
    loader = TextLoader(file_path, encoding="utf-8")
    loaded_documents = loader.load()

    documentos_filtrados = []
    for doc in loaded_documents:
        texto = doc.page_content
        metadata = doc.metadata.copy()

        # Extraindo metadados do caminho (ex: awsDocsMark/s3/put-object.md)
        partes = file_path.replace("\\", "/").split("/")
        if len(partes) >= 2:
            metadata["servico"] = partes[-2]
            metadata["comando"] = partes[-1].replace(".md", "")

        # Criando um único documento com o conteúdo completo do .md
        novo_doc = Document(page_content=texto, metadata=metadata)
        documentos_filtrados.append(novo_doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", ";", " "],
    )

    documents = text_splitter.split_documents(documentos_filtrados)

    if not documents:
        print(f'Nenhum documento válido foi extraído de {file_path}.')
        return False

    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(f'Adicionando {len(documents)} chunks ao vetor')
    vector_store.add_documents(documents=documents, ids=uuids)

    print(f'Ingestão finalizada: {file_path}')
    return True

# Loop principal
def main_loop():
    while True:
        mds = [f for f in os.listdir(data_folder)
               if f.endswith(".md") and not f.startswith("_")]

        if not mds:
            print("Nenhum novo arquivo Markdown encontrado. Encerrando.")
            break

        for filename in mds:
            file_path = os.path.join(data_folder, filename)
            sucesso = ingest_file(file_path)

            new_filename = "_" + filename
            new_file_path = os.path.join(data_folder, new_filename)
            os.rename(file_path, new_file_path)

            status = "ok" if sucesso else "falhou"
            print(f"Processamento de {filename} {status}, renomeado para {new_filename}")

        time.sleep(chunk_interval)


if __name__ == "__main__":
    main_loop()
