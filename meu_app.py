import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CONFIGURAÇÃO DO PROF PLAY
st.set_page_config(page_title="PROF PLAY", layout="wide")
st.title("🎮 PROF PLAY - SISTEMA ATIVO")

# URL DA PLANILHA GOOGLE
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LEITURA (skiprows=7 pula o cabeçalho decorativo da sua planilha)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # TRATAMENTO INICIAL: Garante que o que é número seja lido como número
    for c in df.columns:
        if c not in ["ALUNOS", "Nº", "Número"]:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento")
    
    # 2. EDITOR DE DADOS
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    st.divider()

    # 3. O BOTÃO QUE FINALMENTE SOMA TUDO
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        with st.spinner("Somando missões e salvando..."):
            
            # A MÁGICA: Identifica a coluna de nomes e a de total
            # Vamos somar todas as colunas numéricas que ficarem entre elas
            col_total = "TOTAL (XP)"
            
            # Pegamos apenas as colunas que são de notas (Missões, Níveis, etc)
            # Ignoramos colunas de texto e colunas de controle
            cols_ignoradas = [col_total, "Nº", "Número", "ANTERIOR", "DIFERENÇA", "ALUNOS", "NOME"]
            cols_para_somar = [c for c in df_editado.columns if c not in cols_ignoradas and df_editado[c].dtype != 'object']
            
            # FAZ A SOMA (Agora o TOTAL vai sair do zero!)
            df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

            # 4. SALVA NO GOOGLE
            conn.update(spreadsheet=url, data=df_editado)
            
            st.success(f"✅ SOMA CONCLUÍDA! Colunas somadas: {len(cols_para_somar)}")
            st.balloons()
            
            # MOSTRA O RANKING PARA VOCÊ VER O RESULTADO NA HORA
            st.subheader("🏆 Melhores da Semana")
            ranking = df_editado.sort_values(by=col_total, ascending=False).head(10)
            st.table(ranking[["ALUNOS", col_total]])

except Exception as e:
    st.error(f"Erro no PROF PLAY: {e}")
