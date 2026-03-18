import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LEITURA BRUTA
    # Pula as 7 linhas iniciais para pegar os cabeçalhos reais
    df_raw = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # 2. LIMPEZA RADICAL (O segredo para destravar)
    # Remove colunas vazias e garante que temos dados editáveis
    df = df_raw.loc[:, ~df_raw.columns.str.contains('^Unnamed')].copy()
    
    # FORÇA a primeira coluna a ser TEXTO (para você conseguir inserir alunos)
    df.iloc[:, 0] = df.iloc[:, 0].astype(str).replace(["0", "0.0", "nan", "None"], "")
    
    # FORÇA as outras colunas a serem NÚMEROS (para permitir a soma)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento")
    st.write("👉 **Para inserir:** Clique na célula e digite. Use a última linha para novos alunos.")

    # 3. O EDITOR COM CONFIGURAÇÃO DE COLUNA (Isso destrava a digitação)
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            df.columns[0]: st.column_config.TextColumn("ALUNOS", required=True),
        }
    )

    # 4. O BOTÃO DE CÁLCULO (A soma que você quer)
    st.divider()
    if st.button("🚀 CALCULAR E SALVAR"):
        # Identifica as colunas de missões (tudo entre o nome e o total)
        cols = df_editado.columns.tolist()
        col_total = cols[-1] # TOTAL (XP)
        cols_missoes = cols[1:-1] # Níveis, Extras, etc.

        # Faz a soma horizontal exata da sua fórmula
        df_editado[col_total] = df_editado[cols_missoes].sum(axis=1)

        # Envia para o Google
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ SOMA REALIZADA! Dados enviados para o Google Sheets.")
        st.balloons()
        
        # Mostra o Ranking atualizado
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado.iloc[:, [0, -1]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro no sistema: {e}")
