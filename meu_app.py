import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Busca os dados brutos
    df_raw = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df_raw.loc[:, ~df_raw.columns.str.contains('^Unnamed')].copy()

    # --- DESTRAVA OS TIPOS DE DADOS (Resolve o erro das imagens) ---
    # Forçamos a coluna ALUNOS a aceitar texto (JJ, Nomes, etc)
    if len(df.columns) > 1:
        df.iloc[:, 1] = df.iloc[:, 1].astype(str).replace(["0", "0.0", "nan", "None"], "")
    
    # Forçamos as colunas de missões a serem numéricas
    for c in df.columns[2:]:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento")

    # 2. O Editor com configuração manual (evita o conflito com o Sheets)
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            df.columns[0]: st.column_config.NumberColumn("Nº", disabled=True),
            df.columns[1]: st.column_config.TextColumn("ALUNOS"), # ACEITA LETRAS AQUI
            df.columns[-1]: st.column_config.NumberColumn("TOTAL (XP)", disabled=True)
        }
    )

    # 3. O Botão da Soma (L9+H9+G9...)
    st.divider()
    if st.button("🚀 CALCULAR E SALVAR"):
        cols = df_editado.columns.tolist()
        # Soma tudo que está entre o Nome e o Total
        missões = cols[2:-1]
        
        # Faz a conta matemática
        df_editado[cols[-1]] = df_editado[missões].sum(axis=1)

        # Salva no Google
        conn.update(spreadsheet=url, data=df_editado)
        st.success("✅ Erro resolvido e dados salvos!")
        st.balloons()
        st.rerun()

except Exception as e:
    st.error(f"Erro técnico: {e}")
