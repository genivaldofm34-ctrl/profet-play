import streamlit as st
import pandas as pd

# Configuração de Página
st.set_page_config(page_title="PROFET PLAY", layout="centered")

# Visual Dark
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .card { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7bcf; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 PROFET PLAY - EDITÁVEL")

# Link da sua Planilha (Lembre de compartilhar como EDITOR)
URL = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

try:
    # Lógica para ler a planilha do Google Sheets
    sheet_url = URL.replace('/edit?usp=sharing', '/gviz/tq?tqx=out:csv')
    df = pd.read_csv(sheet_url)
    
    st.write("### 👥 Lista de Alunos Carregada!")
    # Mostra os nomes da coluna B (índice 1)
    for index, row in df.iterrows():
        if index > 6: # Começa a ler depois do cabeçalho da escola
            nome = row.iloc[1] 
            if pd.notna(nome):
                st.markdown(f"<div class='card'>{nome}</div>", unsafe_allow_html=True)
                st.button(f"🏆 Pontuar", key=f"btn_{index}")
except:
    st.warning("⚠️ Erro de Tradução ou Link. Verifique se o tradutor está desligado.")
