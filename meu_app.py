import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 2. Interface de Lançamento
    st.subheader("📋 1. Lance as Notas")
    df_editado = st.data_editor(df, use_container_width=True, hide_index=True)

    # --- A FÓRMULA AUTOMÁTICA ---
    # Pegamos todas as colunas da tabela
    colunas = df_editado.columns.tolist()
    
    # Definimos que:
    # A primeira coluna [0] é o Nome do Aluno
    # A última coluna [-1] é o TOTAL (XP)
    # As colunas do meio [1:-1] são todas as MISSÕES e o ANTERIOR
    
    col_nome = colunas[0]
    col_total = colunas[-1]
    cols_para_somar = colunas[1:-1]

    # Convertendo para número para garantir a conta
    for col in cols_para_somar:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    # EXECUTA A SOMA DAS LINHAS (Igual à sua fórmula do Excel)
    df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

    # 3. Conferência e Ranking
    st.divider()
    st.subheader("🏆 2. Ranking Atualizado (Confirme se somou)")
    
    ranking = df_editado[[col_nome, col_total]].copy()
    ranking = ranking.sort_values(by=col_total, ascending=False)
    
    # Mostra o resultado na tela antes de salvar
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    # 4. Botão Salvar
    if st.button("💾 3. SALVAR E ENVIAR PARA O GOOGLE"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Somas calculadas e enviadas!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no sistema: {e}")
