import os 
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from uuid import uuid4
from models import Models

# Inicializando o modelo
models = Models()
embeddings = models.embeddings_ollama

# Definindo constantes
data_folder = "./data"
chunk_interval = 10

# Armazenamento de vetor com Chroma
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",
)

# Ingestão de arquivos Markdown
def ingest_file(file_path):
    if not file_path.lower().endswith('.md'):
        print(f'Pulando arquivos que não são .md: {file_path}')
        return False

    print(f'Começando ingestão de dados: {file_path}')
    
    loader = UnstructuredMarkdownLoader(file_path, mode="elements")  # pode usar "single" também
    loaded_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", ";", " "],
    )

    documents = text_splitter.split_documents(loaded_documents)
    if not documents:
        print(f'Nenhum documento válido foi extraído de {file_path}.')
        return False

    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(f'Adicionando {len(documents)} documentos ao armazenamento de vetor')
    vector_store.add_documents(documents=documents, ids=uuids)

    print(f'Terminando ingestão dos arquivos: {file_path}')
    return True

# Loop principal
def main_loop():
    while True:
        files = [f for f in os.listdir(data_folder) if not f.startswith("_") and f.endswith(".md")]

        if not files:
            print("Nenhum novo arquivo encontrado. Encerrando o processo.")
            break

        for filename in files:
            file_path = os.path.join(data_folder, filename)

            success = ingest_file(file_path)
            if success:
                new_filename = "_" + filename
                new_file_path = os.path.join(data_folder, new_filename)
                os.rename(file_path, new_file_path)

        time.sleep(chunk_interval)

# Run
if __name__ == "__main__":
    main_loop()
