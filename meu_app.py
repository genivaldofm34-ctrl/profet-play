import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# conexão
conn = st.connection("gsheets", type=GSheetsConnection)

try:

    df = conn.read(
        worksheet="FICHA_MODELO",
        ttl=0
    )

    st.subheader("📋 Painel de edição")

    df_editado = st.data_editor(df, use_container_width=True)

    if st.button("💾 SALVAR"):
        conn.update(
            worksheet="FICHA_MODELO",
            data=df_editado
        )
        st.success("Dados salvos com sucesso!")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
