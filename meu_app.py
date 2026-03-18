import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0) # Preenche vazios com 0 para a conta não dar erro
    
    # 2. Limpeza de colunas indesejadas
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])

    st.subheader("📋 Painel de Edição e Cálculos")

    # 3. O Editor de Dados
    df_editado = st.data_editor(df, use_container_width=True, hide_index=True)

    # --- A MÁGICA DA SOMA ---
    # Identifica colunas que não são o nome do aluno e soma
    colunas_notas = [c for c in df_editado.columns if c.lower() != "aluno" and c.lower() != "total"]
    
    # Converte para número e soma
    for col in colunas_notas:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    df_editado["TOTAL"] = df_editado[colunas_notas].sum(axis=1)

    # Exibe o ranking ou total atualizado na tela
    st.write("📊 **Prévia do Total:**")
    st.dataframe(df_editado[["ALUNO", "TOTAL"]].sort_values(by="TOTAL", ascending=False), hide_index=True)

    if st.button("💾 SALVAR E ATUALIZAR PLANILHA"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Somas calculadas e dados salvos!")
        st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
