import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA - NOME ATUALIZADO
st.set_page_config(page_title="PROF PLAY", layout="wide")
st.title("🎮 PROF PLAY - SISTEMA ATIVO")

# URL DA SUA PLANILHA GOOGLE
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LEITURA DOS DADOS
    # skiprows=7 pula o cabeçalho decorativo da sua planilha
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Limpa colunas vazias
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # 2. TRATAMENTO DE DADOS (Transforma tudo que não é nome em número)
    for c in df.columns:
        if c not in ["ALUNOS", "ALUNO", "Nº", "Número", "NOME"]:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento - PROF PLAY")
    
    # 3. EDITOR DE DADOS
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    st.divider()

    # 4. BOTÃO DE CÁLCULO E SALVAMENTO
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        with st.spinner("Calculando e enviando para o Google Sheets..."):
            col_total = "TOTAL (XP)"
            
            # Identifica as colunas de números
            colunas_numericas = df_editado.select_dtypes(include=['number']).columns.tolist()
            
            # Colunas que NÃO devem ser somadas no Total
            cols_ignoradas = [col_total, "Nº", "Número", "ANTERIOR", "DIFERENÇA"]
            cols_para_somar = [c for c in colunas_numericas if c not in cols_ignoradas]
            
            # Faz a soma horizontal
            df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

            # 5. ATUALIZA A PLANILHA (PRECISA SER 'EDITOR' NO COMPARTILHAMENTO)
            conn.update(spreadsheet=url, data=df_editado)
            
            st.success(f"✅ SOMA CONCLUÍDA! {len(cols_para_somar)} colunas de atividades somadas.")
            st.balloons()
            
            # 6. RANKING FINAL
            st.subheader("🏆 Melhores da Semana")
            # Procura a coluna de nome (pode ser ALUNOS ou ALUNO)
            col_nome = "ALUNOS" if "ALUNOS" in df_editado.columns else df_editado.columns[1]
            
            ranking = df_editado[[col_nome, col_total]].sort_values(by=col_total, ascending=False).head(10)
            st.table(ranking)

except Exception as e:
    st.error(f"⚠️ Erro no PROF PLAY: {e}")
    st.info("Dica: Verifique se a sua planilha Google está com acesso de 'Editor' para qualquer pessoa com o link.")
