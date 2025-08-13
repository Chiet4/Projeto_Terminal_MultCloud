import streamlit as st
from chatbot import get_response  # Certifique-se de que esta função está corretamente implementada

# Configuração da página
st.set_page_config(page_title="Chatbot AWS", layout="centered")
st.title("💬 Chatbot AWS")

# Inicializa o histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite sua pergunta:"):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = get_response(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
