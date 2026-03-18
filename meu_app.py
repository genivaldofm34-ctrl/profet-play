import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Limpa nomes
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace(["0", "0.0", "None"], "")

    # 2. Uso de FORM para garantir que os dados sejam processados
    with st.form("meu_formulario"):
        st.subheader("📋 1. Lance as Notas e Aperte 'CALCULAR'")
        df_editado = st.data_editor(df, use_container_width=True, hide_index=True)
        
        botao_calcular = st.form_submit_button("🧮 CALCULAR SOMA E VER RANKING")

    # 3. O Cálculo só acontece se o botão for clicado
    if botao_calcular:
        # Identifica colunas de notas
        cols_ignorar = ["ALUNOS", "TOTAL (XP)", "TOTAL", "ANTERIOR", "DIFERENÇA"]
        cols_missoes = [c for c in df_editado.columns if c not in cols_ignorar]

        # Converte e Soma
        for col in cols_missoes:
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
        
        # Faz a soma real
        df_editado["TOTAL (XP)"] = df_editado[cols_missoes].sum(axis=1)

        st.success("✅ Soma calculada com sucesso!")
        
        # Mostra o Ranking para conferir
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado[["ALUNOS", "TOTAL (XP)"]].sort_values(by="TOTAL (XP)", ascending=False)
        st.dataframe(ranking, use_container_width=True, hide_index=True)

        # Botão para salvar de verdade no Google
        if st.button("💾 SALVAR DEFINITIVAMENTE NO GOOGLE"):
            conn.update(spreadsheet=url, data=df_editado)
            st.success("Planilha atualizada!")
            st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
