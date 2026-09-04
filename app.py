import os
import streamlit as st
from google import genai
from google.genai import types

def pesquisar_com_ia(pergunta: str) -> str:
    # 1. Recupera a chave de API das variáveis de ambiente / secrets
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        return "Erro: Chave de API (GEMINI_API_KEY) não foi configurada."

    # 2. Inicializa o cliente do Gemini
    client = genai.Client(api_key=api_key)

    # 3. Faz a requisição ativando a busca do Google
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=pergunta,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],  # Ativa o agente de busca
            ),
        )
        return response.text
    except Exception as e:
        return f"Ocorreu um erro ao consultar a IA: {str(e)}"
