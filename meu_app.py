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
    
    # 2. Limpeza de colunas e nomes vazios
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])
    
    # Transforma "None" em texto vazio para você conseguir digitar o nome
    df["ALUNOS"] = df["ALUNOS"].fillna("").astype(str)

    st.subheader("📋 Painel de Lançamento de XP")
    
    # 3. Editor de dados
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic"
    )

    # --- MOTOR DE CÁLCULO ---
    if st.button("🧮 CALCULAR SOMAS E SALVAR"):
        # Identifica as colunas de notas (tudo que não é Aluno, Total, Anterior ou Diferença)
        colunas_para_somar = [
            c for c in df_editado.columns 
            if c not in ["ALUNOS", "TOTAL (XP)", "ANTERIOR", "DIFERENÇA"]
        ]
        
        # Converte para número (o que for texto vira 0) e faz a soma
        for col in colunas_para_somar:
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
        
        # Calcula o Total (XP)
        df_editado["TOTAL (XP)"] = df_editado[colunas_para_somar].sum(axis=1)
        
        # 4. Salva de volta na planilha
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Somas calculadas e salvas com sucesso!")
        st.balloons()
        st.rerun()

except Exception as e:
    st.error(f"Erro: {e}")
