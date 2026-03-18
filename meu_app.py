import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados e limpando o 'None' imediatamente
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    
    # Remove colunas vazias fantasmas
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])

    # 2. Garante que a coluna de Alunos aceite texto (limpa o 0 que o fillna coloca)
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace("0", "").replace("0.0", "")

    st.subheader("📋 Painel de Lançamento")
    
    # 3. Editor de dados - Aqui você lança as notas
    df_editado = st.data_editor(df, use_container_width=True, hide_index=True)

    # --- MOTOR DE CÁLCULO REAL ---
    # Pegamos apenas as colunas que são de notas (Níveis, Extras, etc)
    # Ignoramos ALUNOS e as colunas de resultado final
    cols_para_somar = [c for c in df_editado.columns if c not in ["ALUNOS", "TOTAL (XP)", "TOTAL", "ANTERIOR", "DIFERENÇA"]]
    
    # Converte tudo para número (se houver texto no meio, vira 0)
    for col in cols_para_somar:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    # A SOMA ACONTECE AQUI
    df_editado["TOTAL (XP)"] = df_editado[cols_para_somar].sum(axis=1)

    # Mostra o Ranking atualizado abaixo para conferência
    st.divider()
    st.write("### 🏆 Ranking em Tempo Real")
    ranking = df_editado[["ALUNOS", "TOTAL (XP)"]].sort_values(by="TOTAL (XP)", ascending=False)
    st.table(ranking) # Usando table para visualização mais fixa

    if st.button("💾 SALVAR E CALCULAR"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Tabela somada e salva com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no sistema: {e}")
