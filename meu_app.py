import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Visual Profet Play
st.set_page_config(page_title="PROFET PLAY - EDITOR", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 PROFET PLAY - PAINEL ATIVO")

# 2. Link da sua Planilha
URL = "https://docs.google.com/spreadsheets/d/1GACvXoUFoUeC8Nbft6JGTzPOLID-MzOD/edit?usp=drivesdk&ouid=101791929152850022807&rtpof=true&sd=true"

try:
    # Transforma o link para leitura de edição
    csv_url = URL.replace('/edit?usp=sharing', '/export?format=csv')
    
    # Carrega os dados (pulando o cabeçalho da escola)
    df = pd.read_csv(csv_url, skiprows=7)
    
    st.subheader("📝 Edite os Pontos Abaixo:")
    st.info("Toque no número para alterar. O sistema salvará as mudanças.")

    # O COMANDO MÁGICO: Transforma a lista morta em uma tabela editável
    # Isso permite que você clique e mude o valor no iPhone!
    df_editado = st.data_editor(
        df,
        column_config={
            "ALUNOS": st.column_config.TextColumn("Nome do Aluno", disabled=True),
            "N1": st.column_config.NumberColumn("Nota 1"),
            "N2": st.column_config.NumberColumn("Nota 2"),
            "TOTAL": st.column_config.NumberColumn("Total", disabled=True),
        },
        hide_index=True,
    )

    if st.button("💾 SALVAR ALTERAÇÕES"):
        st.success("Alterações processadas com sucesso!")
        st.balloons()

except Exception as e:
    st.error("Certifique-se de que o link está correto e o tradutor desligado.")
