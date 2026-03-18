import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Busca os dados e pula o cabeçalho
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # 2. LIMPEZA TOTAL (Isso evita as células vermelhas)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # Transformamos tudo em "vazio" onde tem 0 ou erro, para o campo ficar limpo
    df = df.astype(str).replace(["None", "nan", "0.0", "0,0", "0"], "")

    st.subheader("📋 Painel de Lançamento")
    
    # 3. EDITOR DE DADOS (Configurado para aceitar qualquer entrada)
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="editor_final"
    )

    # 4. BOTÃO DE CÁLCULO E SALVAMENTO
    st.divider()
    if st.button("🚀 CALCULAR XP E ATUALIZAR PLANILHA"):
        # Mapeia as colunas
        cols = df_editado.columns.tolist()
        col_total = "TOTAL (XP)" if "TOTAL (XP)" in cols else cols[-1]
        
        # O que não for ALUNOS ou o TOTAL, vira número para somar
        for col in cols:
            if col != cols[0] and col != col_total:
                df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
        
        # A SOMA: (L9+H9+G9...) conforme seu print da planilha
        # Soma todas as colunas de missões linha por linha
        df_editado[col_total] = df_editado.drop(columns=[cols[0], col_total]).sum(axis=1)

        # 5. Manda para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ Sistema atualizado! O total foi calculado.")
        st.balloons()
        
        # Mostra o Ranking Realizado
        st.subheader("🏆 Ranking de XP")
        ranking = df_editado[[cols[0], col_total]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro ao processar: {e}")
