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
    # 1. LEITURA DOS DADOS (Pulando as 7 linhas de cabeçalho do seu modelo)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Remove colunas vazias que o pandas às vezes cria (Unnamed)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # 2. LIMPEZA E FORMATAÇÃO
    # Garante que as colunas de pontos sejam tratadas como números para a soma funcionar
    for c in df.columns:
        if c not in ["ALUNOS", "Nº", "Número"]:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento de Notas")
    st.info("💡 Dica: Altere os valores na tabela abaixo e depois clique no botão no final da página para calcular e salvar.")
    
    # 3. O EDITOR DE DADOS (Onde você digita as notas)
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    st.divider()

    # 4. O BOTÃO DE CÁLCULO E SALVAMENTO
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        with st.spinner("Processando cálculos e atualizando Google Sheets..."):
            col_total = "TOTAL (XP)"
            
            # LÓGICA DE SOMA INTELIGENTE:
            # Pegamos todas as colunas que possuem números
            colunas_numericas = df_editado.select_dtypes(include=['number']).columns.tolist()
            
            # Lista de colunas que NÃO devem entrar na soma do XP total
            # Adicione aqui qualquer outra coluna que você não queira somar
            cols_ignoradas = [col_total, "Nº", "Número", "ANTERIOR", "DIFERENÇA"]
            
            # Filtramos para sobrar apenas as Missões/Extras
            cols_para_somar = [c for c in colunas_numericas if c not in cols_ignoradas]
            
            # Executa a soma horizontal (linha por linha)
            df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

            # 5. ENVIA OS DADOS DE VOLTA PARA O GOOGLE SHEETS
            conn.update(spreadsheet=url, data=df_editado)
            
            st.success(f"✅ SUCESSO! Somamos {len(cols_para_somar)} colunas de atividades.")
            st.balloons()
            
            # EXIBE UM RANKING RÁPIDO PARA CONFERÊNCIA
            st.subheader("🏆 Top 10 Guardiões (Ranking Atual)")
            ranking = df_editado[["ALUNOS", col_total]].sort_values(by=col_total, ascending=False).head(10)
            st.table(ranking)

except Exception as e:
    st.error(f"Ocorreu um erro
