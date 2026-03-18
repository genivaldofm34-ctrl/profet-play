import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lê a planilha e força a limpeza de dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # Preenche vazios com 0 para evitar erro de sistema
    df = df.fillna(0)

    # 2. Mapeamento das colunas para o cadeado de segurança
    cols = df.columns.tolist()
    # Identificamos as colunas por nome ou posição
    col_num = cols[0]   # Número
    col_aluno = cols[1] # ALUNOS
    col_total = cols[-1] # TOTAL (XP)
    cols_notas = cols[2:-1] # Missões

    st.subheader("📋 Painel de Lançamento")

    # 3. O Editor com os tipos de dados corrigidos
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            col_num: st.column_config.NumberColumn("Nº", disabled=True),
            col_aluno: st.column_config.TextColumn("ALUNOS", required=True),
            col_total: st.column_config.NumberColumn("TOTAL (XP)", disabled=True),
            # Todas as outras colunas são configuradas como NUMÉRICAS
            **{c: st.column_config.NumberColumn(c, min_value=0) for c in cols_notas}
        }
    )

    # 4. Botão de Soma (L9+H9+G9...)
    st.divider()
    if st.button("🚀 CALCULAR E SALVAR"):
        # Garante que as notas sejam números
        for c in cols_notas:
            df_editado[c] = pd.to_numeric(df_editado[c], errors='coerce').fillna(0)
        
        # Faz a soma horizontal
        df_editado[col_total] = df_editado[cols_notas].sum(axis=1)

        # Envia para o Google
        conn.update(spreadsheet=url, data=df_editado)
        st.success("✅ Sistema Destravado! Dados salvos no Google Sheets.")
        st.balloons()
        st.rerun()

except Exception as e:
    st.error(f"Erro técnico detectado: {e}")
    st.info("Dica: Verifique se os nomes das colunas na Planilha são exatamente iguais aos do App.")
