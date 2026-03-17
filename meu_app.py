import streamlit as st
import pandas as pd

# 1. Configuração Visual
st.set_page_config(page_title="PROFET PLAY", layout="wide")

st.markdown("<style>.stApp { background-color: #0c0c0c; color: white; }</style>", unsafe_allow_html=True)
st.title("🎮 PROFET PLAY - EDITAR NOTAS")

# 2. SEU LINK DA PLANILHA (COLE ENTRE AS ASPAS)
URL = "https://docs.google.com/spreadsheets/d/1GACvXoUFoUeC8Nbft6JGTzPOLID-MzOD/edit?usp=drivesdk&ouid=101791929152850022807&rtpof=true&sd=true"

try:
    # Link para ler a planilha
    csv_url = URL.replace('/edit?usp=sharing', '/export?format=csv')
    
    # Lê a planilha pulando o cabeçalho (7 linhas)
    df = pd.read_csv(csv_url, skiprows=7)
    
    # Seleciona só as colunas que importam para não ficar bagunçado
    # Vamos focar na coluna B (Nome) e nas de notas
    df_resumo = df.iloc[:, [1, 2, 3, 4]] # Pega as colunas B, C, D, E
    df_resumo.columns = ['ALUNO', 'N1', 'N2', 'TOTAL']

    st.write("### 📝 Altere os valores abaixo:")
    
    # O COMANDO QUE TIRA O APP DO ESTADO "MORTO"
    # Ele cria uma tabela onde você toca e digita no iPhone
    tabela_viva = st.data_editor(df_resumo, hide_index=True)

    if st.button("✅ CONFIRMAR ALTERAÇÕES"):
        st.balloons()
        st.success("Dados atualizados na tela!")

except Exception as e:
    st.error("⚠️ Link incorreto ou tradutor ligado. Verifique o código.")
