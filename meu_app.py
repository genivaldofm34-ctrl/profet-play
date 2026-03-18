import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LEITURA DOS DADOS
    # Pula as 7 linhas iniciais. ttl=0 garante que pegue sempre o dado mais novo.
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Limpa colunas sem nome (fantasmas)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # Preenche os vazios com algo neutro para não travar o editor
    df = df.fillna("")

    st.subheader("📋 Painel de Lançamento")
    st.info("💡 Digite os nomes e as notas. Depois, clique no botão lá embaixo para calcular.")

    # 2. EDITOR DE DADOS TOTALMENTE LIBERADO
    # Removemos as configurações rígidas de coluna para o navegador não bloquear nada
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic" # Permite inserir novos alunos
    )

    # 3. O BOTÃO QUE FAZ A MÁGICA
    st.divider()
    if st.button("🚀 CALCULAR E SALVAR NO GOOGLE"):
        # Pegamos as posições das colunas
        cols = df_editado.columns.tolist()
        col_nome = cols[0]
        col_total = cols[-1] # Assume que TOTAL (XP) é a última coluna à direita
        cols_missoes = cols[1:-1] # Tudo que está no meio

        # Faz a conversão apenas agora, na hora de calcular
        for col in cols_missoes:
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
        
        # A FÓRMULA DE SOMA (Soma as missões de cada linha)
        df_editado[col_total] = df_editado[cols_missoes].sum(axis=1)

        # Envia de volta para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ SOMA REALIZADA! Os dados foram enviados com sucesso.")
        st.balloons()
        
        # Mostra o ranking atualizado
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado[[col_nome, col_total]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro no sistema: {e}")
