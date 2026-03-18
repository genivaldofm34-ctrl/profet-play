import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados brutos
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # 2. Limpeza Total de 'None' e Colunas Fantasmas
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])
    
    # Troca o 'None' por 0 nos números e texto vazio nos alunos
    df = df.fillna(0)
    if "ALUNOS" in df.columns:
        df["ALUNOS"] = df["ALUNOS"].astype(str).replace(["0", "0.0"], "")

    st.subheader("📋 Painel de Lançamento")
    
    # 3. O Editor de Dados
    # O segredo: ele agora mostra a tabela e permite editar
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic"
    )

    # --- MOTOR DE SOMA ---
    # Pegamos todas as colunas que PODEM ter números (Níveis, Extras, etc)
    # Ignoramos apenas a coluna 'ALUNOS'
    cols_para_somar = [c for c in df_editado.columns if "ALUNO" not in c.upper() and "TOTAL" not in c.upper()]
    
    # Converte para número e calcula o TOTAL (XP)
    for col in cols_para_somar:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    # Força a soma na coluna TOTAL (XP)
    df_editado["TOTAL (XP)"] = df_editado[cols_para_somar].sum(axis=1)

    # 4. Exibição do Ranking (Onde você confirma a soma)
    st.divider()
    st.subheader("🏆 Ranking dos Ninjas")
    
    # Criamos uma tabela de ranking que ordena do maior para o menor
    ranking = df_editado[["ALUNOS", "TOTAL (XP)"]].copy()
    ranking = ranking.sort_values(by="TOTAL (XP)", ascending=False)
    
    # Exibe o ranking com cores
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    # 5. Botão de Salvar
    if st.button("💾 SALVAR E SINCRONIZAR"):
        # Antes de salvar, garantimos que a coluna ALUNOS não tenha zeros chatos
        df_editado["ALUNOS"] = df_editado["ALUNOS"].replace("0", "")
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Tudo somado e salvo com sucesso!")
        st.balloons()

except Exception as e:
    st.error(f"Erro no sistema: {e}")
