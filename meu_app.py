import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Busca os dados e limpa o básico
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.fillna(0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 2. Garante que a coluna de Alunos seja texto
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace(["0", "0.0"], "")

    st.subheader("📋 Painel de Lançamento")
    
    # 3. Editor de dados
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic"
    )

    # --- MOTOR DE SOMA "FORÇA BRUTA" ---
    # Pegamos todas as colunas que são números reais
    for col in df_editado.columns:
        if col != "ALUNOS":
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    # Identifica qual coluna é o TOTAL (independente de como está escrita)
    col_total = [c for c in df_editado.columns if "TOTAL" in c.upper()]
    # Identifica as colunas de missões (tudo que não é ALUNO nem TOTAL)
    col_missoes = [c for c in df_editado.columns if c != "ALUNOS" and c not in col_total]

    if col_total:
        # Faz a soma de todas as missões e joga no Total
        df_editado[col_total[0]] = df_editado[col_missoes].sum(axis=1)

    # 4. RANKING VISÍVEL (Para você ter certeza que somou)
    st.divider()
    st.subheader("🏆 Ranking dos Ninjas")
    if col_total:
        ranking = df_editado[["ALUNOS", col_total[0]]].copy()
        ranking = ranking.sort_values(by=col_total[0], ascending=False)
        st.dataframe(ranking, use_container_width=True, hide_index=True)

    # 5. Salvar
    if st.button("💾 SALVAR TUDO"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Soma realizada e salva com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no sistema: {e}")
