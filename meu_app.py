import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Link com o GID da sua aba PAINEL DE COMANDO
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados e removendo o 'None' chato
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0) # Tudo que é vazio vira 0 para poder somar
    
    # Limpa colunas fantasmas e a coluna 'Número'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])

    # 2. Garante que a coluna ALUNOS aceite texto
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace(["0", "0.0"], "")

    st.subheader("📋 Painel de Lançamento de XP")
    
    # 3. Editor de dados - Onde a mágica acontece
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic",
        key="editor_prof" # Chave para o Streamlit monitorar mudanças
    )

    # --- MOTOR DE CÁLCULO (SOMA TUDO) ---
    # Pegamos todas as colunas que NÃO são texto (ALUNOS) e NÃO são o resultado (TOTAL (XP))
    cols_para_somar = [c for c in df_editado.
