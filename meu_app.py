import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# 1. Definimos o link e a conexão
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 2. Lendo os dados. 
    # Usamos worksheet="PAINEL DE COMANDO" em maiúsculo.
    # skiprows=7 pula o cabeçalho decorativo.
    df = conn.read(
        spreadsheet=url,
        worksheet="PAINEL DE COMANDO",
        skiprows=7,
        ttl=0
    )

    st.subheader("📋 Painel de Edição")
    
    # 3. Editor de dados
    df_editado = st.data_editor(df, use_container_width=True)

    if st.button("💾 SALVAR"):
        conn.update(
            spreadsheet=url,
            worksheet="PAINEL DE COMANDO",
            data=df_editado
        )
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
