import os
import logging
from models import Models
from langchain_ollama import ChatOllama
from sentence_transformers import CrossEncoder
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document

# Configuração de logging para registrar informações importantes, como consultas e erros.
logging.basicConfig(
    level=logging.INFO,  # Nível de log: INFO
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato: data, nível e mensagem
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data
)

# Carrega os modelos de embeddings e LLM da classe Models.
models = Models()
embedding = models.embeddings_ollama  # Modelo de embeddings para vetorização de texto
llm = models.model_ollama  # Modelo de linguagem para geração de respostas

# Reranker leve
# Configuração do modelo de reranking (CrossEncoder) para reordenar documentos com base na relevância.
reranker = CrossEncoder(
    os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base"),  # Modelo padrão
    device=os.getenv("RERANKER_DEVICE", "cpu")  # Dispositivo (CPU ou GPU)
)

# Configuração do banco de dados vetorial (ChromaDB) para armazenar e recuperar documentos.
VECTOR_DB_PATH = os.getenv("CHROMA_DB", "./db/chroma_langchain_db")  # Caminho do banco de dados
vector_store = Chroma(
    collection_name="documents",  # Nome da coleção
    embedding_function=embedding,  # Função de embeddings
    persist_directory=VECTOR_DB_PATH  # Diretório para persistência
)

# Configuração do retriever para busca com MMR (Maximal Marginal Relevance).
retriever = vector_store.as_retriever(
    search_type="mmr",  # Tipo de busca
    search_kwargs={"k": int(os.getenv("RETRIEVE_K", 10)), "lambda_mult": float(os.getenv("MMR_LAMBDA", 0.5))}  # Parâmetros
)

# Prompt para guiar o modelo de linguagem a responder apenas com comandos válidos da AWS CLI.
prompt = ChatPromptTemplate.from_template("""\
Você é um assistente de linha de comando da AWS CLI.
Responda somente com comandos reais existentes no contexto.
Se não houver comandos correspondentes, diga:
"Não encontrei um exemplo correspondente na documentação."

Contexto:
{context}

Pergunta:
{question}

Resposta:
""")

def get_response(user_query: str) -> str:
    # Log da consulta recebida
    logging.info(f"Query recebida: {user_query}")

    # Recupera documentos relevantes do banco de dados vetorial
    docs = retriever.invoke(user_query)
    docs = [doc if isinstance(doc, Document) else Document(page_content=str(doc)) for doc in docs]

    # Reordena os documentos com base na relevância usando o modelo de reranking
    pairs = [(user_query, doc.page_content) for doc in docs]
    try:
        scores = reranker.predict(pairs)  # Calcula os scores de relevância
    except Exception as e:
        logging.error(f"Erro no reranker: {e}")
        scores = [0] * len(docs)  # Define scores como 0 em caso de erro

    logging.info(f"Reranked {len(scores)} documentos")

    # Seleciona os 5 documentos mais relevantes
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, _ in ranked[:5]]

    # Cria uma cadeia de documentos para o LLM
    chain = create_stuff_documents_chain(llm, prompt)

    try:
        # Gera a resposta com base nos documentos selecionados e na consulta do usuário
        result = chain.invoke({
            "context": top_docs,
            "question": user_query
        })
        return result if isinstance(result, str) else result.get("answer", "")
    except Exception as e:
        logging.error(f"Erro no chain LLM: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta."


def main():
    # Mensagem inicial do chatbot
    logging.info("Iniciando chatbot AWS CLI. Digite 'q' para sair.")
    while True:
        # Recebe a consulta do usuário
        query = input("Você: ").strip()
        if query.lower() in {"q", "sair", "exit", "quit"}:  # Comandos para sair
            logging.info("Encerrando chatbot.")
            break
        # Processa a consulta e exibe a resposta
        resposta = get_response(query)
        print(f"\nAssistente: {resposta}\n")

if __name__ == "__main__":
    main()