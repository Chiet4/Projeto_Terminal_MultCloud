import os 
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from preprocessamento import extrair_blocos_relevantes
from langchain_core.documents import Document
from langchain_chroma import Chroma
from uuid import uuid4
from models import Models

# inicializando o modelo
models = Models()
embeddings = models.embeddings_ollama
#llm = models.model_ollama

# Definindo constantes
data_folder = "./data"
#chunk_size = 1000
#chunk_overlap = 50
chunk_interval = 10

# Definindo o armazenamento de vetor Chroma
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db", # Data local 
)

# Ingestão de dados
def ingest_file(file_path):

    if not file_path.lower().endswith('.pdf'):
        print(f'Pulando arquivos que não-PDF: {file_path}')
        return False
    
    print(f'Começando ingestão de dados: {file_path}')
    loader = PyPDFLoader(file_path)
    loaded_documents = loader.load()

    documentos_filtrados = []
    for doc in loaded_documents:
        blocos = extrair_blocos_relevantes(doc.page_content)
        for bloco in blocos:
            novo_doc = Document(page_content=bloco, metadata=doc.metadata)
            documentos_filtrados.append(novo_doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 50,
        separators=["\n\n", "\n", ".", ";", " "],
    )

    documents = text_splitter.split_documents(documentos_filtrados)

    if not documents:
        print(f'Nenhum documento válido foi extraído de {file_path}.')
        return False

    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(f'Adicionando documentos {len(documents)} ao armazenamento de vetor')
    vector_store.add_documents(documents=documents, ids=uuids)

    print(f'Terminando ingestão dos arquivos: {file_path}')
    return True

# Main loop
def main_loop():
    while True:
        files = [f for f in os.listdir(data_folder) if not f.startswith("_") and f.endswith(".pdf")]

        if not files:  # Se não houver mais arquivos para processar, encerra o programa
            print("Nenhum novo arquivo encontrado. Encerrando o processo.")
            break

        for filename in os.listdir(data_folder):
            if not filename.startswith("_"):
                file_path = os.path.join(data_folder, filename)

                sucess = ingest_file(file_path) 
                if sucess:
                    new_filename = "_" + filename
                    new_file_path = os.path.join(data_folder, new_filename)
                    os.rename(file_path, new_file_path)

        time.sleep(chunk_interval) # espera 10 para cada vez


# run
if __name__ == "__main__":
    main_loop()