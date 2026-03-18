import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados originais
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Limpeza de colunas fantasmas
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # IMPORTANTE: Converte a primeira coluna para TEXTO para permitir digitar nomes
    # E preenche o resto com 0 para permitir somar
    df.iloc[:, 0] = df.iloc[:, 0].astype(str).replace(["0", "0.0", "None", "nan"], "")
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Controle (Digite os nomes e notas)")
    
    # 2. Editor de dados LIBERADO
    # O num_rows="dynamic" permite que você adicione novos alunos na última linha
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic" 
    )

    st.divider()

    # 3. O Botão que PROCESSA TUDO
    if st.button("🚀 CALCULAR SOMAS E SALVAR NO GOOGLE"):
        # Pegamos as colunas por posição para não errar o nome
        # Primeira = Aluno | Última = Total | Meio = Missões
        cols = df_editado.columns.tolist()
        col_total = cols[-1]
        cols_missoes = cols[1:-1]

        # Faz a soma horizontal (Fórmula que você queria)
        df_editado[col_total] = df_editado[cols_missoes].sum(axis=1)

        # Envia para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ Alunos salvos e XP somado com sucesso!")
        st.balloons()
        
        # Mostra o Ranking atualizado abaixo
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado.iloc[:, [0, -1]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro no sistema: {e}")
