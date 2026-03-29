import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROF PLAY", layout="wide")
st.title("🎮 PROF PLAY - SISTEMA ATIVO")

# Link da sua planilha
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LEITURA PRECISA: Lemos a partir da linha 8 (onde começam os nomes)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Remove colunas vazias que o Google cria automaticamente
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()

    # 2. CONVERSÃO "BLINDADA" DE NÚMEROS
    # Isso transforma qualquer "None" ou "10,0" em número de verdade
    for c in df.columns:
        if c not in ["ALUNOS", "Nº", "NOME"]:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento")
    
    # 3. EDITOR DE DADOS
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # 4. BOTÃO DE CÁLCULO TOTAL
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        with st.spinner("Atualizando Prof Play..."):
            col_total = "TOTAL (XP)"
            
            # Definimos exatamente quais colunas entrarão na soma
            # Pegamos tudo que for número, exceto o Nº da chamada e o próprio Total
            cols_ignoradas = [col_total, "Nº", "Número", "ANTERIOR", "DIFERENÇA", "ALUNOS"]
            cols_para_somar = [c for c in df_editado.columns if c not in cols_ignoradas]
            
            # A SOMA QUE NÃO FALHA
            df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

            # 5. SALVAMENTO NO GOOGLE SHEETS
            conn.update(spreadsheet=url, data=df_editado)
            
            st.success(f"✅ SOMA REALIZADA! Colunas processadas: {len(cols_para_somar)}")
            st.balloons()
            
            # Ranking Visual
            st.subheader("🏆 Melhores da Semana")
            ranking = df_editado[["ALUNOS", col_total]].sort_values(by=col_total, ascending=False).head(5)
            st.table(ranking)

except Exception as e:
    st.error(f"Erro no PROF PLAY: {e}")
