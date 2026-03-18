import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados (começando da linha 8 onde estão os cabeçalhos)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    
    # Limpeza de colunas extras
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    st.subheader("📋 Painel de Lançamento de XP")
    
    # 2. Editor de dados
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic"
    )

    # --- A FÓRMULA QUE VOCÊ QUER (IGUAL AO SHEETS) ---
    # Colunas que entram na soma de XP:
    cols_missoes = [
        "Nível 1 (20 XP)", "Nível 2 (30 XP)", "Nível 3 (20 XP)", 
        "Nível 4 (10 XP)", "Nível 5 (20 XP)", "Guardião do silêncio (15 XP)",
        "Monitor de missões (15 XP)", "Lenda da semana (5 XP)",
        "Melhor companheiro (5 XP)", "Superação da semana (5 XP)", 
        "EXTRA", "ANTERIOR"
    ]

    # Verificamos quais dessas colunas realmente existem na tabela para não dar erro
    cols_presentes = [c for c in cols_missoes if c in df_editado.columns]

    # Convertemos para número e aplicamos a soma linha por linha
    for col in cols_presentes:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    # O TOTAL XP agora recebe a soma exata de todas as missões + o anterior
    if "TOTAL (XP)" in df_editado.columns:
        df_editado["TOTAL (XP)"] = df_editado[cols_presentes].sum(axis=1)

    # 3. Botão Salvar e Calcular
    st.divider()
    if st.button("💾 ATUALIZAR SOMAS E SALVAR NO GOOGLE"):
        # Envia os dados já somados pelo Python para a planilha
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Soma realizada! A planilha ganhou vida.")
        st.balloons()
        st.rerun()

except Exception as e:
    st.error(f"Erro ao processar as colunas: {e}")
