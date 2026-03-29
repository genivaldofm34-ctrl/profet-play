import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="PROF PLAY", layout="wide")
st.title("🎮 PROF PLAY - SISTEMA ATIVO")

# URL DA SUA PLANILHA GOOGLE
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LEITURA DOS DADOS (Pulando as 7 linhas conforme seu modelo)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Remove colunas fantasmas que o Excel/Google às vezes cria no final
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # 2. PRÉ-TRATAMENTO (Garante que o editor mostre números corretamente)
    for c in df.columns:
        if c not in ["ALUNOS", "ALUNO", "Nº", "Número", "NOME"]:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento de Notas")
    
    # 3. O EDITOR DE DADOS
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    st.divider()

    # 4. O BOTÃO DE CÁLCULO "BLINDADO"
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        with st.spinner("Processando cálculos do PROF PLAY..."):
            col_total = "TOTAL (XP)"
            
            # Forçamos a conversão para número de novo (Garante a soma)
            for col in df_editado.columns:
                if col not in ["ALUNOS", "ALUNO", "Nº", "Número", "NOME"]:
                    df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
            
            # Identifica colunas numéricas
            colunas_numericas = df_editado.select_dtypes(include=['number']).columns.tolist()
            
            # Lista do que NÃO deve ser somado no XP
            cols_ignoradas = [col_total, "Nº", "Número", "ANTERIOR", "DIFERENÇA"]
            cols_para_somar = [c for c in colunas_numericas if c not in cols_ignoradas]
            
            # EXECUTA A SOMA REAL
            df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

            # 5. ENVIA DE VOLTA PARA O GOOGLE SHEETS
            conn.update(spreadsheet=url, data=df_editado)
            
            st.success(f"✅ SOMA REALIZADA! Colunas somadas: {', '.join(cols_para_somar)}")
            st.balloons()
            
            # 6. RANKING AUTOMÁTICO
            st.subheader("🏆 Top 10 Guardiões")
            # Tenta achar a coluna de nomes
            col_nome = "ALUNOS" if "ALUNOS" in df_editado.columns else df_editado.columns[1]
            
            ranking = df_editado[[col_nome, col_total]].sort_values(by=col_total, ascending=False).head(10)
            st.table(ranking)

except Exception as e:
    st.error(f"⚠️ Erro no PROF PLAY: {e}")
    st.info("Dica: Verifique se sua planilha no Google está compartilhada como 'Editor' para qualquer pessoa com o link.")
