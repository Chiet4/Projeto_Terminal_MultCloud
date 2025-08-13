import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from uuid import uuid4
from models import Models

# Inicializando o modelo de embeddings
models = Models()
embeddings = models.embeddings_ollama  # Modelo de embeddings para vetorização de texto

# Constantes para configuração
data_folder = "./data"  # Diretório onde os arquivos Markdown estão localizados
chunk_size = 500  # Tamanho máximo de cada chunk de texto
chunk_overlap = 100  # Sobreposição entre chunks
chunk_interval = 10  # Intervalo entre execuções do loop principal (em segundos)

# Configuração do banco de dados vetorial (ChromaDB) para armazenar e recuperar documentos.
vector_store = Chroma(
    collection_name="documents",  # Nome da coleção no banco de dados
    embedding_function=embeddings,  # Função de embeddings para vetorização
    persist_directory="./db/chroma_langchain_db",  # Diretório para persistência dos dados
)

# Função para ingerir um arquivo Markdown e armazenar seus chunks no banco de dados vetorial
def ingest_file(file_path):
    # Verifica se o arquivo é um Markdown
    if not file_path.lower().endswith('.md'):
        print(f'Pulando arquivos que não são Markdown: {file_path}')
        return False

    print(f'Iniciando ingestão: {file_path}')
    loader = TextLoader(file_path, encoding="utf-8")  # Carrega o conteúdo do arquivo
    loaded_documents = loader.load()  # Retorna uma lista de documentos carregados

    documentos_filtrados = []
    for doc in loaded_documents:
        texto = doc.page_content  # Conteúdo do documento
        metadata = doc.metadata.copy()  # Metadados do documento

        # Extraindo metadados do caminho do arquivo (ex: awsDocsMark/s3/put-object.md)
        partes = file_path.replace("\\", "/").split("/")
        if len(partes) >= 2:
            metadata["servico"] = partes[-2]  # Nome do serviço (ex: s3)
            metadata["comando"] = partes[-1].replace(".md", "")  # Nome do comando (ex: put-object)

        # Criando um único documento com o conteúdo completo do .md
        novo_doc = Document(page_content=texto, metadata=metadata)
        documentos_filtrados.append(novo_doc)

    # Dividindo o texto em chunks menores
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  # Tamanho máximo de cada chunk
        chunk_overlap=chunk_overlap,  # Sobreposição entre chunks
        separators=["\n\n", "\n", ".", ";", " "],  # Separadores para divisão
    )
    documents = text_splitter.split_documents(documentos_filtrados)

    # Verifica se há documentos válidos
    if not documents:
        print(f'Nenhum documento válido foi extraído de {file_path}.')
        return False

    # Gera IDs únicos para cada chunk
    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(f'Adicionando {len(documents)} chunks ao vetor')
    vector_store.add_documents(documents=documents, ids=uuids)  # Adiciona os chunks ao banco de dados

    print(f'Ingestão finalizada: {file_path}')
    return True

# Loop principal para processar arquivos Markdown
def main_loop():
    while True:
        # Lista todos os arquivos Markdown no diretório de dados
        mds = [f for f in os.listdir(data_folder)
               if f.endswith(".md") and not f.startswith("_")]

        # Verifica se há arquivos para processar
        if not mds:
            print("Nenhum novo arquivo Markdown encontrado. Encerrando.")
            break

        # Processa cada arquivo Markdown
        for filename in mds:
            file_path = os.path.join(data_folder, filename)  # Caminho completo do arquivo
            sucesso = ingest_file(file_path)  # Ingestão do arquivo

            # Renomeia o arquivo para indicar que foi processado
            new_filename = "_" + filename
            new_file_path = os.path.join(data_folder, new_filename)
            os.rename(file_path, new_file_path)

            # Exibe o status do processamento
            status = "ok" if sucesso else "falhou"
            print(f"Processamento de {filename} {status}, renomeado para {new_filename}")

        # Aguarda antes de verificar novamente
        time.sleep(chunk_interval)


if __name__ == "__main__":
    main_loop()