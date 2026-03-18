import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura e Limpeza
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace(["0", "0.0", "None"], "")

    st.subheader("📋 1. Lance as Notas Abaixo")
    # O editor serve apenas para entrada de dados
    df_editado = st.data_editor(df, use_container_width=True, hide_index=True)

    # --- CÁLCULO MANUAL FORÇADO ---
    # Identificamos as colunas de missões (que não são nomes nem totais)
    cols_ignorar = ["ALUNOS", "TOTAL (XP)", "TOTAL", "ANTERIOR", "DIFERENÇA"]
    cols_missoes = [c for c in df_editado.columns if c not in cols_ignorar]

    # Convertendo tudo para número para garantir a conta
    for col in cols_missoes:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)

    # Calculando a soma
    df_editado["TOTAL (XP)"] = df_editado[cols_missoes].sum(axis=1)

    st.divider()
    st.subheader("📊 2. Confira a Soma e o Ranking")
    
    # Criamos uma tabela de conferência que mostra o nome e o total calculado
    conferencia = df_editado[["ALUNOS", "TOTAL (XP)"]].copy()
    conferencia = conferencia.sort_values(by="TOTAL (XP)", ascending=False)
    
    # EXIBE A SOMA AQUI (Se aqui estiver somando, o problema está resolvido!)
    st.dataframe(conferencia, use_container_width=True, hide_index=True)

    if st.button("💾 3. SALVAR TUDO NA PLANILHA"):
        # Garante que a coluna de texto não vá com zeros
        df_editado["ALUNOS"] = df_editado["ALUNOS"].replace("0", "")
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados enviados com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no sistema: {e}")
