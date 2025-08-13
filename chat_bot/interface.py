import streamlit as st
from chat_reranker import get_response

# Configuração da página
st.set_page_config(page_title="Chatbot AWS", layout="centered")
st.title("💬 Chatbot Cloud CLI")

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens já enviadas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua pergunta:")

if user_input:
    # Adiciona a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gera a resposta do bot
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = get_response(user_input)
            except Exception as e:
                response = f"⚠️ Erro ao gerar resposta: {e}"
            st.markdown(response)

    # Armazena a resposta do bot
    st.session_state.messages.append({"role": "assistant", "content": response})