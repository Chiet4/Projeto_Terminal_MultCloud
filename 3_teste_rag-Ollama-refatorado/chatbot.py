import time
import logging
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from models import Models

# Configuração do logging para gravar os logs em um arquivo .txt
logging.basicConfig(level=logging.DEBUG,  # Definindo o nível de log para DEBUG
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',  # Nome do arquivo de log
                    filemode='w')  # 'w' sobrescreve o arquivo a cada execução

# Função para inicializar o modelo e embeddings
def initialize_models():
    logging.info("Inicializando modelos...")
    models = Models()
    embeddings = models.embeddings_ollama
    llm = models.model_ollama
    logging.info("Modelos inicializados com sucesso.")
    return embeddings, llm

# Função para inicializar o armazenamento vetorial (Chroma)
def initialize_vector_store(embeddings):
    logging.info("Inicializando armazenamento vetorial (Chroma)...")
    vector_store = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory="./db/chroma_langchain_db",
    )
    logging.info("Armazenamento vetorial inicializado com sucesso.")
    return vector_store

# Função para inicializar a memória de conversa
def initialize_memory():
    logging.info("Inicializando memória de conversa...")
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True, 
        chat_memory_limit=500
    )
    logging.info("Memória de conversa inicializada com sucesso.")
    return memory

# Função para inicializar a cadeia de recuperação (retrieval chain)
def initialize_retrieval_chain(llm, retriever, memory):
    logging.info("Inicializando a cadeia de recuperação (ConversationalRetrievalChain)...")
    retrieval_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False
    )
    logging.info("Cadeia de recuperação inicializada com sucesso.")
    return retrieval_chain

# Função principal de interação com o usuário
def main():
    logging.info("Iniciando chatbot...")
    embeddings, llm = initialize_models()
    vector_store = initialize_vector_store(embeddings)
    memory = initialize_memory()
    retrieval_chain = initialize_retrieval_chain(llm, vector_store.as_retriever(), memory)
    
    while True:
        query = input("Digite 'q', 'end' para sair: ")
        if query.lower() in ['q', 'end']:
            logging.info("Saindo da aplicação...")
            break

        try:
            # Marcar o tempo de início da consulta
            start_time = time.time()
            logging.info(f"Recebendo consulta do usuário: {query}")

            # Processando a consulta
            result = retrieval_chain.invoke({"question": query})

            # Calcular o tempo de processamento
            elapsed_time = time.time() - start_time
            logging.info(f"Consulta processada em {elapsed_time:.4f} segundos.")

            # Log da resposta gerada
            answer = result.get("answer", "Desculpe, não encontrei uma resposta.")
            logging.info(f"Resposta gerada: {answer}")

            # Feedback para o usuário
            print(f"Assistente: {answer}")
            print(f"Tempo de processamento: {elapsed_time:.4f} segundos.")
        
        except Exception as e:
            logging.error(f"Erro ao processar a pergunta: {str(e)}")



# Executando o código
if __name__ == "__main__":
    main()
