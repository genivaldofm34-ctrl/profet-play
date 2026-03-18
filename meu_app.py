import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura dos dados (pula as 7 linhas iniciais)
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # Limpeza básica
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    df = df.fillna(0)

    # Garante que a primeira coluna seja texto (para os nomes que você já destravou)
    df.iloc[:, 0] = df.iloc[:, 0].astype(str).replace(["0", "0.0", "nan", "None"], "")

    st.subheader("📋 Painel de Lançamento")
    
    # 2. O Editor de Dados
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="editor_v3"
    )

    # --- O MOTOR DA SOMA (Fórmula das Linhas) ---
    # Pegamos todas as colunas de missões (entre o nome e o total)
    cols = df_editado.columns.tolist()
    col_nome = cols[0]
    col_total = cols[-1] # Assume que TOTAL (XP) é a última
    cols_para_somar = cols[1:-1] # Tudo o que for nota no meio

    # 3. O Botão que aciona a matemática
    st.divider()
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        # Converte tudo que é nota para número real
        for col in cols_para_somar:
            df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
        
        # AQUI É A SOMA: Ele soma a linha inteira e joga na última coluna
        df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

        # Envia para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ CÁLCULO REALIZADO! Os totais foram atualizados na planilha.")
        st.balloons()
        
        # Mostra o Ranking para você ver que funcionou
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado[[col_nome, col_total]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro no sistema: {e}")
