import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Busca os dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # 2. Limpeza total (Tira o 'None' e colunas fantasmas)
    df = df.fillna(0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])

    # Garante que a coluna de Alunos aceite texto
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace(["0", "0.0"], "")

    st.subheader("📋 Painel de Lançamento")
    
    # 3. Editor de dados
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic"
    )

    # --- MOTOR DE CÁLCULO (A SOMA VIVA) ---
    # Pegamos todas as colunas que NÃO são texto e NÃO são resultados
    cols_ignorar = ["ALUNOS", "TOTAL (XP)", "TOTAL", "ANTERIOR", "DIFERENÇA"]
    cols_soma = [c for c in df_editado.columns if c not in cols_ignorar]
    
    # Converte para número e soma
    for col in cols_soma:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    # Calcula o Total na hora
    df_editado["TOTAL (XP)"] = df_editado[cols_soma].sum(axis=1)

    # 4. Ranking (Onde você confirma se somou)
    st.divider()
    st.subheader("🏆 Ranking em Tempo Real")
    ranking = df_editado[["ALUNOS", "TOTAL (XP)"]].copy()
    ranking = ranking.sort_values(by="TOTAL (XP)", ascending=False)
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    # 5. Salvar
    if st.button("💾 SALVAR E ATUALIZAR"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no código: {e}")
