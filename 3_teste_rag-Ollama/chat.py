from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory

from models import Models

# inicializar o modelo
models = Models()
embeddings = models.embeddings_ollama
llm = models.model_ollama

# Inciando o armazenamento de vetor 
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db", 
)

# memória de conversa
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

# Criando o prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente especializado em AWS. Responda com precisão baseado APENAS nos documentos fornecidos. Se não souber, diga que não tem a informação."),
        ("human", "{chat_history}"),
        ("human", "Explique detalhadamente: {input}. Use apenas {context} como fonte.")
    ]
)

# Chamada retrieval chain
#retriever = vector_store.as_retriever(kwargs={"k": 10})
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 10, "lambda_mult": 0.5})
combine_docs_chain = create_stuff_documents_chain(
    llm, prompt
)
#retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain, memory=memory)

# chain de conversa com memória
retrieval_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    verbose=True  # opcional: para debugar
)

# main loop
def main():
    while True:
        query = input("Digite 'q', 'end' para sair: ")
        if query.lower() in ['q', 'end']:
            break

        try:
            result = retrieval_chain.invoke({"question": query})
            answer = result.get("answer", "Desculpe, não encontrei uma resposta.")
            print("Assistente:", answer, "\n\n")
        except Exception as e:
            print("Erro ao processar a pergunta:", str(e))


# Run
if __name__ == "__main__":
    main()