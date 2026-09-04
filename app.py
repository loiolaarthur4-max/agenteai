import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Configuração da página
st.set_page_config(
    page_title="Agente de IA",
    page_icon="🤖",
    layout="centered"
)

# Estilização para visual limpo
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Agente de Pesquisa em Tempo Real")
st.caption("Digite sua pergunta e pressione Enter para pesquisar na web.")

# 2. Gerenciamento da Chave de API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    with st.sidebar:
        st.header("⚙️ Configuração")
        api_key = st.text_input("Cole sua GEMINI_API_KEY:", type="password")

# 3. Histórico de mensagens da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Campo de entrada do Chat (Envia automático ao dar Enter)
if pergunta := st.chat_input("Digite sua pergunta e aperte Enter..."):
    if not api_key:
        st.error("Por favor, informe sua GEMINI_API_KEY na barra lateral.")
    else:
        # Mostra a mensagem do usuário na tela
        st.session_state.messages.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        # Gera a resposta do agente com busca na web
        with st.chat_message("assistant"):
            with st.spinner("🔎 Pesquisando na web..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=pergunta,
                        config=types.GenerateContentConfig(
                            tools=[{"google_search": {}}],
                            system_instruction="Você é um assistente de pesquisa preciso. Responda em português de forma direta, clara e formatada em Markdown."
                        ),
                    )
                    
                    resposta_texto = response.text
                    st.markdown(resposta_texto)
                    
                    # Salva no histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})

                except Exception as e:
                    st.error(f"Erro ao processar busca: {str(e)}")
