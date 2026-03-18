import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura dos dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Limpeza de colunas vazias que o Sheets as vezes envia
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.fillna(0)

    st.subheader("📋 1. Lance os Dados na Tabela")
    
    # 2. Editor de dados
    df_editado = st.data_editor(df, use_container_width=True, hide_index=True)

    # --- MOTOR DE SOMA POR POSIÇÃO (SEM ERRO DE NOME) ---
    # Pegamos todas as colunas exceto a primeira (nome) e a última (total)
    todas_cols = df_editado.columns.tolist()
    col_nome = todas_cols[0]
    col_total = todas_cols[-1]
    cols_para_somar = todas_cols[1:-1] # Tudo que está no "meio"

    # Forçamos a soma
    for col in cols_para_somar:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    # A MÁGICA: Soma tudo e joga na última coluna
    df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

    st.divider()
    st.subheader("📊 2. Ranking de XP (Confirmação)")
    
    # Mostra o ranking baseado na última coluna da sua planilha
    ranking = df_editado[[col_nome, col_total]].copy()
    ranking = ranking.sort_values(by=col_total, ascending=False)
    
    # Formatação para o nome do aluno aparecer como texto
    ranking[col_nome] = ranking[col_nome].astype(str).replace(["0", "0.0"], "")
    
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    # 3. Botão de Salvar
    if st.button("💾 SALVAR TUDO"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success(f"Somado com sucesso na coluna {col_total}!")
        st.balloons()

except Exception as e:
    st.error(f"Erro Crítico: {e}")
