import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna("")
    
    # --- AQUI APAGAMOS A PRIMEIRA COLUNA ---
    # Se a primeira coluna estiver vindo com o nome "Unnamed: 0" ou similar, nós a removemos:
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    
    st.subheader("📋 Painel de Edição")
    
    # Exibindo o editor sem a coluna de índice lateral (hide_index=True)
    df_editado = st.data_editor(
        df, 
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True  # Isso remove os números 0, 1, 2 da lateral esquerda
    )

    if st.button("💾 SALVAR ALTERAÇÕES"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
