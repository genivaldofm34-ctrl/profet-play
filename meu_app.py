import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:

    # lê a planilha
    df = conn.read(
        worksheet="PAINEL DE COMANDO",
        ttl=0
    )

    st.subheader("📊 Painel de edição")

    df_editado = st.data_editor(
        df,
        use_container_width=True
    )

    if st.button("💾 SALVAR ALTERAÇÕES"):

        conn.update(
            worksheet="PAINEL DE COMANDO",
            data=df_editado
        )

        st.success("Alterações salvas com sucesso!")
        st.balloons()

except Exception as e:

    st.error(f"Erro ao carregar dados: {e}")
