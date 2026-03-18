import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Busca os dados originais
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 2. Painel de Lançamento
    st.subheader("📋 1. Lance as Missões (XP)")
    
    # Criamos o editor
    df_editado = st.data_editor(df, use_container_width=True, hide_index=True, key="editor_v1")

    # --- A FÓRMULA MÁGICA DA SOMA ---
    # Identificamos a coluna de nomes (ALUNOS) e a de resultado (TOTAL (XP))
    # Tudo o que sobrar no meio são as MISSÕES
    todas_as_colunas = df_editado.columns.tolist()
    
    # Definimos quem é quem
    col_aluno = "ALUNOS" if "ALUNOS" in todas_as_colunas else todas_as_colunas[0]
    col_total = "TOTAL (XP)" if "TOTAL (XP)" in todas_as_colunas else todas_as_colunas[-1]
    
    # As missões são as colunas que NÃO são o nome nem o total
    colunas_missoes = [c for c in todas_as_colunas if c != col_aluno and c != col_total]

    # Convertemos as missões para números para garantir que o Python saiba somar
    for col in colunas_missoes:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)

    # AQUI ESTÁ A FÓRMULA: O Total XP recebe a soma das linhas das missões
    df_editado[col_total] = df_editado[colunas_missoes].sum(axis=1)

    # 3. Visualização do Ranking (Para você ver a soma acontecendo)
    st.divider()
    st.subheader("🏆 2. Ranking Automático (Confirmação da Soma)")
    
    ranking_viz = df_editado[[col_aluno, col_total]].copy()
    ranking_viz = ranking_viz.sort_values(by=col_total, ascending=False)
    
    # Limpa os nomes para não aparecer 0.0
    ranking_viz[col_aluno] = ranking_viz[col_aluno].astype(str).replace(["0", "0.0", "None"], "")
    
    # EXIBE A TABELA DE SOMA
    st.table(ranking_viz)

    # 4. Botão Salvar
    if st.button("💾 3. SALVAR TUDO NO GOOGLE"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success(f"Soma de {len(colunas_missoes)} missões realizada com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no sistema: {e}")
