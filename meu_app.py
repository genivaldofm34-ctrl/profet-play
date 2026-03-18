import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY - EDITOR", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Link direto para os dados da planilha atualizada
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados. O skiprows=7 pula as linhas de cabeçalho da escola.
    df = conn.read(spreadsheet=url, skiprows=7)
    
    st.write("### 📝 Painel de Edição")
    # Mostra a tabela para edição
    df_editado = st.data_editor(df)

    if st.button("💾 SALVAR ALTERAÇÕES"):
        # Tenta salvar as alterações de volta na planilha
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("Dica: Certifique-se de que a planilha está compartilhada como 'Editor' para qualquer pessoa com o link.")
