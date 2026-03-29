import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura dos dados pulando o cabeçalho (Ajuste o skiprows se necessário)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # Limpeza para garantir que o editor aceite os dados e trate números
    for c in df.columns:
        if c not in ["ALUNOS", "Nº", "Número"]:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento")
    
    # 2. O Editor de Dados
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    st.divider()
    
    # 3. O BOTÃO DE CÁLCULO (VERSÃO REVISADA)
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        col_total = "TOTAL (XP)"
        
        # A MÁGICA: Soma tudo que for número, exceto as colunas que não devem entrar na conta
        # Ignoramos o 'Nº', 'ANTERIOR' e o próprio 'TOTAL (XP)' para não somar o total com ele mesmo
        cols_ignoradas = ["Nº", "Número", "ANTERIOR", "DIFERENÇA", col_total]
        
        # Seleciona só as colunas numéricas que sobraram (as Missões)
        cols_para_somar = [c for c in df_editado.select_dtypes(include=['number']).columns if c not in cols_ignoradas]
        
        # Faz a soma linha por linha
        df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

        # Envia de volta para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success(f"✅ SOMA REALIZADA! Colunas somadas: {', '.join(cols_para_somar)}")
        st.balloons()
        
        # Mostra o Ranking para confirmar
        st.subheader("🏆 Ranking de Lendas")
        # Pega a coluna 1 (Nome) e a coluna de Total
        ranking = df_editado.sort_values(by=col_total, ascending=False)
        st.table(ranking[["ALUNOS", col_total]].head(10))

except Exception as e:
    st.error(f"Erro técnico: {e}")
