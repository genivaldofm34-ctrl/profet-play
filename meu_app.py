import streamlit as st
import pandas as pd

# 1. Estilo Profet Play (Igual ao seu PC)
st.set_page_config(page_title="PROFET PLAY", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .card-aluno { 
        background-color: #1e1e1e; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #2e7bcf;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .stButton>button { width: 100%; background-color: #2e7bcf; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Link da sua Planilha (https://docs.google.com/spreadsheets/d/1GACvXoUFoUeC8Nbft6JGTzPOLID-MzOD/edit?usp=drivesdk&ouid=101791929152850022807&rtpof=true&sd=true"

st.title("🎮 PROFET PLAY MOBILE")

try:
    # Transforma o link da planilha para formato de leitura rápida
    if "edit?" in URL:
        csv_url = URL.split('/edit')[0] + '/gviz/tq?tqx=out:csv'
    else:
        csv_url = URL

    # Lê os dados
    df = pd.read_csv(csv_url)
    
    st.markdown("### 👥 Lista de Alunos Ativa")

    # Na sua foto, os nomes estão na Coluna B (índice 1 no Python)
    # E começam pra valer depois da linha 8
    for index, row in df.iterrows():
        if index >= 7:  # Ajuste para pular o cabeçalho da escola
            nome = row.iloc[1] # Coluna B
            pontos = row.iloc[3] # Coluna D (Total)
            
            if pd.notna(nome) and str(nome).strip() != "":
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    col1.markdown(f"<div class='card-aluno'>{nome}</div>", unsafe_allow_html=True)
                    if col2.button(f"🏆 {pontos}", key=f"btn_{index}"):
                        st.balloons()
                        st.toast(f"Ponto registrado para {nome}!")

except Exception as e:
    st.error("⚠️ Erro na conexão. Verifique se o link da planilha foi colado corretamente e se o tradutor está desligado.")
