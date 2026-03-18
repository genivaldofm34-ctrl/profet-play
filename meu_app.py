import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura e Limpeza de Cabeçalho
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()

    # --- DESTRAVA TOTAL ---
    # Remove os "None", "nan" e "0.0" que estão bloqueando as células
    df = df.astype(str).replace(["None", "nan", "0.0", "0,0", "0"], "")

    st.subheader("📋 Painel de Lançamento")
    st.info("💡 Digite os nomes e notas. Se a célula estiver vazia, basta clicar e digitar.")

    # 2. Editor de Dados (Liberado para Inserção)
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic" # Permite adicionar novos alunos na última linha
    )

    # 3. Botão de Processamento
    st.divider()
    if st.button("🚀 CALCULAR XP E ATUALIZAR GOOGLE"):
        # Identifica as colunas para a conta
        cols = df_editado.columns.tolist()
        col_nome = cols[0]
        col_total = "TOTAL (XP)" if "TOTAL (XP)" in cols else cols[-1]
        
        # Colunas de missões são tudo o que está entre o nome e o total
        idx_nome = 0
        idx_total = cols.index(col_total)
        cols_missoes = cols[idx_nome + 1 : idx_total]

        # Converte para número apenas na hora de somar
        for col in cols_missoes:
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
        
        # Faz a soma horizontal (A fórmula da sua planilha)
        df_editado[col_total] = df_editado[cols_missoes].sum(axis=1)

        # Salva no Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ Tudo somado e salvo com sucesso!")
        st.balloons()
        
        # Mostra o Ranking Real
        st.subheader("🏆 Ranking de XP")
        ranking = df_editado[[col_nome, col_total]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
