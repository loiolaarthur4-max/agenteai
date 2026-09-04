import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Configuração da página
st.set_page_config(
    page_title="Agente de Pesquisa IA",
    page_icon="🔎",
    layout="centered"
)

# Estilização CSS personalizada para um visual moderno
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #0f172a;
    }
    .main-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Cabeçalho principal
st.title("🔎 Agente de Pesquisa IA")
st.caption("Pesquisas em tempo real impulsionadas pelo Google e Gemini 2.5")

# 3. Campo para configuração da chave da API na interface
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    with st.sidebar:
        st.header("⚙️ Configurações")
        api_key = st.text_input("Cole sua GEMINI_API_KEY aqui:", type="password")
        st.caption("Obtenha uma chave gratuita em: aistudio.google.com")

# 4. Interface de Pesquisa
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
pergunta = st.text_area(
    "O que você gostaria de pesquisar na web hoje?",
    placeholder="Ex: Quais são os suplementos mais estudados para ganho de massa muscular em 2026?",
    height=100
)

col1, col2 = st.columns([1, 1])
with col1:
    btn_buscar = st.button("🚀 Pesquisar na Web")
with col2:
    btn_limpar = st.button("🗑️ Limpar")

st.markdown("</div>", unsafe_allow_html=True)

if btn_limpar:
    st.rerun()

# 5. Processamento da Pesquisa
if btn_buscar:
    if not api_key:
        st.error("Por favor, informe a sua GEMINI_API_KEY na barra lateral ou defina a variável de ambiente.")
    elif not pergunta.strip():
        st.warning("Por favor, digite uma pergunta antes de pesquisar.")
    else:
        with st.spinner("🤖 O agente está pesquisando na web e compilando a resposta..."):
            try:
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=pergunta,
                    config=types.GenerateContentConfig(
                        tools=[{"google_search": {}}],  # Ativa o agente de busca no Google
                        system_instruction="Você é um assistente de pesquisa preciso e amigável. Responda em português de forma clara e estruturada usando formatação Markdown."
                    ),
                )
                
                # Exibição do resultado em um card bonito
                st.markdown("### 📋 Resposta do Agente:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Ocorreu um erro ao realizar a consulta: {str(e)}")
