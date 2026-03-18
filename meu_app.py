import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados e limpando valores nulos para evitar erros de edição
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna("") # Preenche espaços vazios para permitir escrita
    
    st.subheader("📋 Painel de Edição")
    
    # FORÇANDO A EDIÇÃO:
    # O parâmetro 'disabled=False' garante que nada seja bloqueado
    df_editado = st.data_editor(
        df, 
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("💾 SALVAR ALTERAÇÕES"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
