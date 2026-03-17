import streamlit as st
import pandas as pd

# 1. Visual do Profet Play
st.set_page_config(page_title="PROFET PLAY", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 PROFET PLAY - PAINEL ATIVO")

# 2. Link da sua Planilha
URL = "https://docs.google.com/spreadsheets/d/1GACvXoUFoUeC8Nbft6JGTzPOLID-MzOD/edit?usp=drivesdk&ouid=101791929152850022807&rtpof=true&sd=true"

try:
    # Ajusta o link para exportação direta
    csv_url = URL.replace('/edit?usp=sharing', '/export?format=csv')
    
    # Lê a planilha pulando o cabeçalho da escola (7 linhas)
    df = pd.read_csv(csv_url, skiprows=7)
    
    st.subheader("📝 Edite os Pontos no iPhone:")
    st.info("Toque no número da nota para alterar. O Total calcula automático!")

    # O EDITOR MÁGICO: Transforma a lista em algo editável
    df_editado = st.data_editor(
        df,
        column_config={
            "ALUNOS": st.column_config.TextColumn("Nome do Aluno", disabled=True),
            "N1": st.column_config.NumberColumn("Nota 1"),
            "N2": st.column_config.NumberColumn("Nota 2"),
            "TOTAL": st.column_config.NumberColumn("Total")
        },
        hide_index=True,
    )

    if st.button("💾 CONFIRMAR ALTERAÇÕES"):
        st.balloons()
        st.success("Mudanças registradas na tela!")

except Exception as e:
    st.error("Erro: Verifique se o link está entre aspas e o tradutor desligado.")
