import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Link atualizado com o GID da aba PAINEL DE COMANDO
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados usando o link que já aponta para a aba correta
    # O skiprows=7 pula o cabeçalho da escola
    df = conn.read(
        spreadsheet=url,
        skiprows=7,
        ttl=0
    )

    st.subheader("📋 Painel de Edição")
    df_editado = st.data_editor(df, use_container_width=True)

    if st.button("💾 SALVAR ALTERAÇÕES"):
        conn.update(
            spreadsheet=url,
            data=df_editado
        )
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
