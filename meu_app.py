import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Conexão simplificada
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados - skiprows=7 pula o cabeçalho da escola
    # Removi o nome da aba para o Google decidir a melhor rota
    df = conn.read(skiprows=7, ttl=0)

    st.subheader("📋 Painel de Edição")
    df_editado = st.data_editor(df, use_container_width=True)

    if st.button("💾 SALVAR ALTERAÇÕES"):
        conn.update(data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    st.info("Verifique se a planilha está como 'Editor' no compartilhamento.")
