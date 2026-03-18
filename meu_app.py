import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY - EDITOR", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Link direto para a aba correta da sua planilha
url = "https://docs.google.com/spreadsheets/d/1wytV0LyDt5PXe-35T_X3zfsZKaXGKNaWlRWCEeZ_dlM/edit#gid=1926794755"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # O skiprows=7 pula o cabeçalho da escola para pegar os nomes dos alunos
    df = conn.read(spreadsheet=url, skiprows=7)
    
    st.write("### 📝 Edite as notas e clique em Salvar")
    df_editado = st.data_editor(df)

    if st.button("💾 SALVAR NA PLANILHA"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Planilha atualizada com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro de conexão: {e}")
