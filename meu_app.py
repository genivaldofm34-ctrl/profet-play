import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados
    if 'df_mestre' not in st.session_state:
        df_inicial = conn.read(spreadsheet=url, skiprows=7, ttl=0)
        df_inicial = df_inicial.fillna(0)
        df_inicial = df_inicial.loc[:, ~df_inicial.columns.str.contains('^Unnamed')]
        if "Número" in df_inicial.columns:
            df_inicial = df_inicial.drop(columns=["Número"])
        st.session_state.df_mestre = df_inicial

    # --- A FÓRMULA DE SOMA ---
    def calcular_tudo():
        df = st.session_state.df_mestre
        # Identifica colunas que são missões (não são nomes nem totais)
        cols_ignorar = ["ALUNOS", "TOTAL (XP)", "TOTAL", "ANTERIOR", "DIFERENÇA"]
        cols_missoes = [c for c in df.columns if c not in cols_ignorar]
        
        # Converte para número e soma linha por linha
        for col in cols_missoes:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # A SOMA QUE VOCÊ PEDIU:
        df["TOTAL (XP)"] = df[cols_missoes].sum(axis=1)
        st.session_state.df_mestre = df

    st.subheader("📋 Painel de Lançamento")
    
    # 2. Editor de dados com gatilho de cálculo
    df_editado = st.data_editor(
        st.session_state.df_mestre, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic",
        key="meu_editor"
    )

    # Botão para forçar a soma aparecer na tela
    if st.button("🧮 ATUALIZAR SOMAS"):
        st.session_state.df_mestre = df_editado
        calcular_tudo()
        st.rerun()

    # 3. Ranking Automático
    st.divider()
    st.subheader("🏆 Ranking dos Ninjas")
    ranking = st.session_state.df_mestre[["ALUNOS", "TOTAL (XP)"]].copy()
    ranking = ranking.sort_values(by="TOTAL (XP)", ascending=False)
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    # 4. Botão Salvar
    if st.button("💾 SALVAR TUDO NO GOOGLE"):
        conn.update(spreadsheet=url, data=st.session_state.df_mestre)
        st.success("Somas salvas com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
