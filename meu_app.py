import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# 1. Link da sua planilha
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=0"

# 2. Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 3. Lendo os dados da aba específica
    # worksheet="painel de comando" garante que ele abra a aba certa
    # skiprows=7 pula o cabeçalho da escola
    df = conn.read(
        spreadsheet=url,
        worksheet="painel de comando",
        skiprows=7,
        ttl=0
    )

    st.subheader("📋 Painel de edição")
    
    # 4. Editor de dados
    df_editado = st.data_editor(df, use_container_width=True)

    if st.button("💾 SALVAR"):
        # 5. Atualizando a aba correta
        conn.update(
            spreadsheet=url,
            worksheet="painel de comando",
            data=df_editado
        )
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("Dica: Verifique se o nome da aba na planilha é exatamente 'painel de comando' (em minúsculas, como você escreveu).")
