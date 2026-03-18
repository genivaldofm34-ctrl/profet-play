import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

conn = st.connection("gsheets", type=GSheetsConnection)

try:

    df = conn.read(ttl=0)

    st.subheader("Painel de edição")

    df_editado = st.data_editor(df, use_container_width=True)

    if st.button("SALVAR ALTERAÇÕES"):

        conn.update(data=df_editado)

        st.success("Dados salvos!")
        st.balloons()

except Exception as e:
    st.error(e)
