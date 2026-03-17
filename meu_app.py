import streamlit as st
import pandas as pd

# 1. Configuração Visual
st.set_page_config(page_title="PROFET PLAY", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .card { 
        background-color: #1e1e1e; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #2e7bcf; 
        margin-bottom: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 PROFET PLAY MOBILE")

# 2. SEU LINK DA PLANILHA (COLE DENTRO DAS ASPAS)
URL = "https://docs.google.com/spreadsheets/d/1GACvXoUFoUeC8Nbft6JGTzPOLID-MzOD/edit?usp=drivesdk&ouid=101791929152850022807&rtpof=true&sd=true"

try:
    # Ajusta o link para exportar como CSV (formato que o app lê)
    if "edit?" in URL:
        csv_url = URL.split('/edit')[0] + '/export?format=csv'
    else:
        csv_url = URL
    
    # Lê a planilha e pula o cabeçalho da escola
    df = pd.read_csv(csv_url, skiprows=8)
    
    st.write("### 👥 Lista de Alunos")

    # Percorre os alunos da sua planilha
    for index, row in df.iterrows():
        nome = row.iloc[1] # Coluna B (Nomes)
        if pd.notna(nome) and str(nome).strip() != "" and "ALUNOS" not in str(nome):
            with st.container():
                st.markdown(f"<div class='card'>👤 {nome}</div>", unsafe_allow_html=True)
                if st.button(f"🏆 Dar Ponto", key=f"btn_{index}"):
                    st.balloons()
                    st.success(f"Ponto para {nome}!")

except Exception as e:
    st.error("⚠️ Verifique se colou o link entre as aspas e se a planilha está aberta para 'Qualquer pessoa com o link'.")
