import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")

st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# 🔗 ID da planilha (mais estável)
SPREADSHEET_ID = "1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo"
ABA = "FICHA_MODELO"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 📥 CARREGAR DADOS
    df = conn.read(
        spreadsheet=SPREADSHEET_ID,
        worksheet=ABA,
        skiprows=7,
        ttl=0
    )

    df = df.fillna(0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    st.subheader("📋 Lançamento de Pontos")

    # 🧠 Editor
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    # 🔁 FORÇAR CÓPIA (ESSENCIAL)
    df_editado = df_editado.copy()

    # 📊 IDENTIFICAR COLUNAS
    colunas = df_editado.columns.tolist()
    col_nome = colunas[0]
    col_total = colunas[-1]
    cols_para_somar = colunas[1:-1]

    # 🔢 CONVERTER PARA NÚMERO
    df_editado[cols_para_somar] = df_editado[cols_para_somar].apply(
        pd.to_numeric, errors='coerce'
    ).fillna(0)

    # 🧮 SOMA AUTOMÁTICA
    df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

    # 📊 PROGRESSO DA TURMA
    st.divider()
    st.subheader("📈 Progresso da Turma")

    total_geral = df_editado[col_total].sum()
    maximo = len(df_editado) * 100  # ajuste se quiser

    progresso = total_geral / maximo if maximo > 0 else 0

    st.progress(progresso)
    st.write(f"XP Total da Turma: **{int(total_geral)}**")

    # 🏆 RANKING
    st.divider()
    st.subheader("🏆 Ranking dos Alunos")

    ranking = df_editado[[col_nome, col_total]].copy()
    ranking = ranking.sort_values(by=col_total, ascending=False).reset_index(drop=True)

    # 🥇🥈🥉 medalhas
    medalhas = ["🥇", "🥈", "🥉"]

    def get_medalha(i):
        return medalhas[i] if i < 3 else ""

    ranking["Posição"] = ranking.index + 1
    ranking["🏅"] = ranking.index.map(get_medalha)

    ranking = ranking[["Posição", "🏅", col_nome, col_total]]

    st.dataframe(ranking, use_container_width=True, hide_index=True)

    # 💾 SALVAR AUTOMÁTICO
    st.divider()

    if st.button("💾 SALVAR NO GOOGLE"):
        conn.update(
            spreadsheet=SPREADSHEET_ID,
            worksheet=ABA,
            data=df_editado
        )
        st.success("Dados salvos com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no sistema: {e}")
