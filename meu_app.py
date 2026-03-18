import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

# Link direto para a sua aba
url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LER DADOS ( skiprows=7 pula o cabeçalho decorativo )
    df_original = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Limpa colunas fantasmas e preenche vazios com 0
    df = df_original.loc[:, ~df_original.columns.str.contains('^Unnamed')].copy()
    df = df.fillna(0)

    # 2. LIBERAR A PRIMEIRA COLUNA (ALUNOS) PARA DIGITAÇÃO
    # Isso garante que você consiga escrever nomes sem erro de 'tipo'
    df.iloc[:, 0] = df.iloc[:, 0].astype(str).replace(["0", "0.0", "nan", "None"], "")

    st.subheader("📋 Painel de Controle")
    st.info("💡 Para adicionar alunos, use a última linha da tabela. Para somar, clique no botão abaixo.")

    # 3. EDITOR DE DADOS (num_rows='dynamic' libera a inserção de novos alunos)
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True, 
        num_rows="dynamic"
    )

    st.divider()

    # 4. O BOTÃO QUE É O "CÉREBRO" DA SOMA
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        # Pegamos as posições: Primeira=Nome | Última=Total | Meio=Notas
        colunas = df_editado.columns.tolist()
        col_total = colunas[-1]
        cols_missoes = colunas[1:-1]

        # Converte as missões para números reais (se for texto, vira 0)
        for col in cols_missoes:
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)

        # A FÓRMULA: Soma horizontal de todas as missões da linha
        df_editado[col_total] = df_editado[cols_missoes].sum(axis=1)

        # 5. SALVAR DE VERDADE
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ SOMA REALIZADA E SALVA! O Total XP foi atualizado.")
        st.balloons()
        
        # Mostra o Ranking atualizado para você conferir
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado.iloc[:, [0, -1]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Ocorreu um erro técnico: {e}")
