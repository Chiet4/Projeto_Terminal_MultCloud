import os
import logging
from models import Models
from langchain_ollama import ChatOllama
from sentence_transformers import CrossEncoder
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Carrega modelos
models = Models()
embedding = models.embeddings_ollama
llm = models.model_ollama

# Reranker leve
reranker = CrossEncoder(
    os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base"),
    device=os.getenv("RERANKER_DEVICE", "cpu")
)

# Configura ChromaDB
VECTOR_DB_PATH = os.getenv("CHROMA_DB", "./db/chroma_langchain_db")
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embedding,
    persist_directory=VECTOR_DB_PATH
)

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": int(os.getenv("RETRIEVE_K", 10)), "lambda_mult": float(os.getenv("MMR_LAMBDA", 0.5))}
)

# Prompt para AWS CLI
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
    logging.info(f"Query recebida: {user_query}")

    docs = retriever.invoke(user_query)
    docs = [doc if isinstance(doc, Document) else Document(page_content=str(doc)) for doc in docs]

    # Rerank
    pairs = [(user_query, doc.page_content) for doc in docs]
    try:
        scores = reranker.predict(pairs)
    except Exception as e:
        logging.error(f"Erro no reranker: {e}")
        scores = [0] * len(docs)

    logging.info(f"Reranked {len(scores)} documentos")

    # Seleciona top 5
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, _ in ranked[:5]]
    chain = create_stuff_documents_chain(llm, prompt)

    try:
        result = chain.invoke({
            "context": top_docs,
            "question": user_query
        })
        return result if isinstance(result, str) else result.get("answer", "")
    except Exception as e:
        logging.error(f"Erro no chain LLM: {e}")
        return "Desculpe, ocorreu um erro ao gerar a resposta."


def main():
    logging.info("Iniciando chatbot AWS CLI. Digite 'q' para sair.")
    while True:
        query = input("Você: ").strip()
        if query.lower() in {"q", "sair", "exit", "quit"}:
            logging.info("Encerrando chatbot.")
            break
        resposta = get_response(query)
        print(f"\nAssistente: {resposta}\n")

if __name__ == "__main__":
    main()