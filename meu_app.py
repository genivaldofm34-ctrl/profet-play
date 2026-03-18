import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="PROFET PLAY", layout="centered")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lendo os dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna("")
    
    # --- LIMPANDO AS COLUNAS ---
    # 1. Remove colunas fantasmas (Unnamed)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # 2. APAGA A COLUNA "Número" que vem da planilha
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])
    
    st.subheader("📋 Painel de Edição")
    
    # Exibindo o editor limpo
    df_editado = st.data_editor(
        df, 
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True 
    )

    if st.button("💾 SALVAR ALTERAÇÕES"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
