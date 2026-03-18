import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# 1. Link da sua planilha
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=0"

# 2. Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 3. Lendo os dados da aba correta (AGORA EM MAIÚSCULO)
    # O skiprows=7 pula as 7 linhas de cabeçalho da escola
    df = conn.read(
        spreadsheet=url,
        worksheet="PAINEL DE COMANDO",
        skiprows=7,
        ttl=0
    )

    st.subheader("📋 Painel de Edição")
    
    # 4. Editor de dados
    df_editado = st.data_editor(df, use_container_width=True)

    if st.button("💾 SALVAR ALTERAÇÕES"):
        # 5. Atualizando a planilha
        conn.update(
            spreadsheet=url,
            worksheet="PAINEL DE COMANDO",
            data=df_editado
        )
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("Dica: Verifique se o nome da aba é exatamente PAINEL DE COMANDO na sua planilha.")
