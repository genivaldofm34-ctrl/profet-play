import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY - EDITOR", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Link atualizado da sua nova planilha
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados. 
    # Se a sua tabela de alunos começar na linha 8, mantenha o skiprows=7
    df = conn.read(spreadsheet=url, skiprows=7)
    
    st.write("### 📝 Painel de Edição")
    df_editado = st.data_editor(df)

    if st.button("💾 SALVAR ALTERAÇÕES"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
