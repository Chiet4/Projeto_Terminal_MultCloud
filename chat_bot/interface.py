import streamlit as st
from chat_reranker import get_response

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Chatbot AWS",  # Título da aba do navegador
    layout="centered"  # Layout centralizado
)
st.title("💬 Chatbot Cloud CLI")  # Título exibido na interface

# Inicializa o histórico de mensagens na sessão do usuário
# Isso permite que as mensagens sejam mantidas mesmo após a interface ser atualizada
if "messages" not in st.session_state:
    st.session_state.messages = []  # Lista para armazenar mensagens do usuário e do bot

# Exibe o histórico de mensagens já enviadas (usuário e bot)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # Define o papel (usuário ou assistente)
        st.markdown(message["content"])  # Exibe o conteúdo da mensagem

# Campo de entrada para o usuário digitar sua pergunta
user_input = st.chat_input("Digite sua pergunta:")  # Exibe um campo de entrada na interface

if user_input:
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):  # Exibe a mensagem do usuário na interface
        st.markdown(user_input)

    # Gera a resposta do bot
    with st.chat_message("assistant"):  # Exibe a mensagem do assistente na interface
        with st.spinner("Pensando..."):  # Exibe um spinner enquanto a resposta é gerada
            try:
                response = get_response(user_input)  # Chama a função para gerar a resposta
            except Exception as e:
                response = f"⚠️ Erro ao gerar resposta: {e}"  # Trata erros e exibe uma mensagem de erro
            st.markdown(response)  # Exibe a resposta gerada

    # Armazena a resposta do bot no histórico
    st.session_state.messages.append({"role": "assistant", "content": response})