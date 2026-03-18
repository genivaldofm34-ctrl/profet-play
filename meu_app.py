import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY - EDITOR", layout="centered")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# 1. Link da sua planilha (ajustado para o formato de exportação de dados)
url = "https://docs.google.com/spreadsheets/d/1wytV0LyDt5PXe-35T_X3zfsZKaXGKNaWlRWCEeZ_dlM/edit#gid=1926794755"

# 2. Cria a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 3. Lê os dados pulando as linhas iniciais (cabeçalho da escola)
    # Se a sua tabela de alunos começar em uma linha diferente, ajuste o 'skiprows'
    df = conn.read(spreadsheet=url, skiprows=7)
    
    st.write("### 📝 Edite as notas e clique em Salvar")
    
    # 4. Área de edição interativa
    df_editado = st.data_editor(df)

    if st.button("💾 SALVAR NA PLANILHA"):
        # 5. Envia as alterações de volta para a nuvem
        # IMPORTANTE: Para o .update funcionar, você precisa ter configurado 
        # as credenciais (Service Account) nos Secrets do Streamlit.
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Planilha atualizada com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.info("Dica: Verifique se a planilha está no formato 'Planilhas Google' e se o acesso está liberado.")
