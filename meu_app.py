import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados (pulando as 7 linhas iniciais)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # Preenche vazios com 0 para não dar erro no editor numérico
    df = df.fillna(0)

    # --- CONFIGURAÇÃO DE SEGURANÇA ---
    # Aqui a gente separa: Quem é texto e quem é número
    colunas = df.columns.tolist()
    nome_col_aluno = colunas[0] # A primeira coluna (Alunos)
    col_total = colunas[-1]     # A última coluna (Total XP)
    cols_notas = colunas[1:-1]  # Todas as do meio (Missões)

    st.subheader("📋 Painel de Lançamento")
    
    # 2. O Editor com "Cadeado" por coluna
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            # COLUNA DE ALUNOS: Permite letras (Texto)
            nome_col_aluno: st.column_config.TextColumn("ALUNOS", required=True),
            # COLUNAS DE NOTAS: Só permitem números (Number)
            **{c: st.column_config.NumberColumn(c, min_value=0, format="%d") for c in cols_notas},
            # COLUNA TOTAL: Protegida (Apenas leitura)
            col_total: st.column_config.NumberColumn(col_total, disabled=True, format="%d")
        }
    )

    # 3. Botão de Cálculo (Fórmula L9+H9+G9...)
    st.divider()
    if st.button("🚀 CALCULAR E SALVAR NO GOOGLE"):
        # Garante que tudo nas missões seja número antes de somar
        for c in cols_notas:
            df_editado[c] = pd.to_numeric(df_editado[c], errors='coerce').fillna(0)
        
        # SOMA DAS MISSÕES
        df_editado[col_total] = df_editado[cols_notas].sum(axis=1)

        # Envia para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ Calculado! Agora os números estão protegidos.")
        st.balloons()
        st.rerun()

except Exception as e:
    st.error(f"Erro na tabela: {e}")
