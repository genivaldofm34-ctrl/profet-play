import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY - EDITOR", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Link da sua planilha (verifique se ela permite edição)
url = "https://docs.google.com/spreadsheets/d/1GACvXoUFoUeC8Nbft6JGTzPOLID-MzOD/edit?usp=sharing&ouid=101791929152850022807&rtpof=true&sd=true"

# Cria a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lê os dados pulando as linhas iniciais se necessário
    df = conn.read(spreadsheet=url, skiprows=7)
    
    st.write("### 📝 Edite as notas e clique em Salvar")
    
    # Área de edição
    df_editado = st.data_editor(df)

    if st.button("💾 SALVAR NA PLANILHA"):
        # Envia as alterações de volta para a nuvem
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Planilha atualizada com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.info("Dica: Verifique se o link da planilha está correto e se o arquivo requirements.txt já foi processado pelo servidor.")
