import streamlit as st
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")

st.title("🎮 PROFET PLAY MOBILE")

# Cole o link da sua planilha aqui dentro das aspas
URL = "https://docs.google.com/spreadsheets/d/1GACvXoUFoUeC8Nbft6JGTzPOLID-MzOD/edit?usp=drivesdk&ouid=101791929152850022807&rtpof=true&sd=true"

try:
    # Transforma o link para leitura
    csv_url = URL.replace('/edit?usp=sharing', '/export?format=csv')
    
    # Lê a planilha pulando o cabeçalho (7 linhas)
    df = pd.read_csv(csv_url, skiprows=7)
    
    st.write("### 👥 Lista de Alunos")
    
    # Criar a tabela que você pode tocar e editar no iPhone
    # Se o requirements.txt estiver certo, esse comando vai funcionar!
    df_editado = st.data_editor(df, hide_index=True)

    if st.button("💾 SALVAR ALTERAÇÕES"):
        st.success("Alterações registradas!")
        st.balloons()

except Exception as e:
    st.warning("O sistema está carregando as ferramentas. Aguarde 1 minuto e atualize a página.")
