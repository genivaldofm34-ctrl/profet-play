import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lê os dados pulando o cabeçalho decorativo
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # LIMPEZA TOTAL: Transforma tudo em texto puro para NÃO FICAR VERMELHO ao digitar
    df = df.astype(str).replace(["None", "nan", "0.0", "0,0", "0"], "")

    st.subheader("📋 Painel de Lançamento")
    
    # 2. Editor de Dados Configurado para não travar
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="editor_vfinal"
    )

    # 3. O Botão que faz a mágica da sua planilha
    st.divider()
    if st.button("🚀 CALCULAR XP E ATUALIZAR GOOGLE"):
        # Pegamos os nomes das colunas
        cols = df_editado.columns.tolist()
        col_nome = cols[0]
        col_total = "TOTAL (XP)" if "TOTAL (XP)" in cols else cols[-1]
        
        # O que for nota, a gente força virar número para somar
        for c in cols:
            if c != col_nome and c != col_total:
                df_editado[c] = pd.to_numeric(df_editado[c], errors='coerce').fillna(0)
        
        # A FÓRMULA MÁGICA: Soma todas as colunas de missões (horizontal)
        # É a mesma lógica de (L9+H9+G9...) que você usa no Sheets
        df_editado[col_total] = df_editado.drop(columns=[col_nome, col_total]).sum(axis=1)

        # Salva no Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ Somas realizadas com sucesso!")
        st.balloons()
        st.rerun()

except Exception as e:
    st.error(f"Erro de conexão: {e}")
