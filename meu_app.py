import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # 2. LIMPEZA CRUCIAL PARA TIRAR O 'NONE'
    df = df.fillna(0) # Troca todos os Nones por 0 para permitir soma
    
    # Garante que a coluna de alunos seja tratada como texto para você conseguir digitar
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace("0", "")
    
    # Remove colunas inúteis
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    st.subheader("📋 Painel de Lançamento")
    
    # 3. Editor de dados
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True
    )

    # --- CÁLCULO DA SOMA EM TEMPO REAL ---
    # Pegamos todas as colunas, exceto a de nomes e as de totais que já existem
    colunas_para_somar = [c for c in df_editado.columns if c not in ["ALUNOS", "TOTAL (XP)", "DIFERENÇA", "ANTERIOR"]]
    
    for col in colunas_para_somar:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)

    # Criamos a soma automática na coluna TOTAL (XP)
    df_editado["TOTAL (XP)"] = df_editado[colunas_para_somar].sum(axis=1)

    st.divider()
    st.write("### 🏆 Ranking Atualizado")
    # Mostra quem tem mais pontos primeiro
    ranking = df_editado[["ALUNOS", "TOTAL (XP)"]].sort_values(by="TOTAL (XP)", ascending=False)
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    if st.button("💾 SALVAR TUDO"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Somas calculadas e salvas com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro: {e}")
