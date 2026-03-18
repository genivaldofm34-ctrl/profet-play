import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados (Ignorando o cabeçalho decorativo)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    
    # Limpa colunas vazias
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    st.subheader("📋 Painel de Lançamento")
    
    # 2. O Editor de Dados
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic"
    )

    # 3. O Botão que dá Vida à Soma
    st.divider()
    if st.button("🚀 CALCULAR SOMAS E SALVAR NO GOOGLE"):
        # Pegamos as colunas
        cols = df_editado.columns.tolist()
        col_nome = cols[0]
        col_total = cols[-1] # Assume que TOTAL (XP) é a última
        cols_missoes = cols[1:-1] # Tudo entre o nome e o total

        # Forçamos a conversão para número
        for col in cols_missoes:
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
        
        # A FÓRMULA: Soma das missões na horizontal
        df_editado[col_total] = df_editado[cols_missoes].sum(axis=1)

        # Envia para o Google
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ SOMA REALIZADA! Verifique sua planilha agora.")
        st.balloons()
        
        # Mostra como ficou o Ranking
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado[[col_nome, col_total]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro: {e}")
