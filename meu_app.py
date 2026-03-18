import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # --- O PULO DO GATO ---
    # Isso limpa os dados e garante que o editor aceite escrever nomes e números
    df = df.convert_dtypes() 
    
    st.subheader("📋 Painel de Edição")
    
    # Liberamos a edição para todas as colunas
    df_editado = st.data_editor(
        df, 
        use_container_width=True,
        num_rows="dynamic" # Permite que você adicione novos alunos se precisar
    )

    if st.button("💾 SALVAR ALTERAÇÕES"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados salvos com sucesso na planilha!")
        st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
