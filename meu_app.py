import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide")
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Leitura dos dados pulando o cabeçalho
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # Limpeza para garantir que o editor aceite os dados
    df.iloc[:, 1] = df.iloc[:, 1].astype(str).replace(["0", "0.0", "nan", "None"], "")
    for c in df.columns[2:]:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    st.subheader("📋 Painel de Lançamento")
    
    # 2. O Editor de Dados
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    # 3. O BOTÃO QUE FAZ A SOMA (Igual à sua fórmula do Excel)
    st.divider()
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        cols = df_editado.columns.tolist()
        
        # Identificamos a coluna de TOTAL e as colunas de notas
        # No seu print, o TOTAL (XP) é a coluna 'N' e 'EXTRA' é a 'M'
        col_total = "TOTAL (XP)"
        col_extra = "EXTRA"
        
        # Selecionamos todas as colunas de Nível e Missões para somar
        # Ignoramos as colunas de 'Nº', 'ALUNOS', 'TOTAL', 'ANTERIOR' e 'DIFERENÇA'
      if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        # 1. Selecionamos apenas as colunas que REALMENTE são números (Missões)
        # Isso evita que o Python tente somar nomes ou textos
        df_editado[col_total] = df_editado.select_dtypes(include=['number']).drop(columns=[col_total], errors='ignore').sum(axis=1)

        # 2. Envia de volta para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ AGORA FOI! O Total XP foi calculado com sucesso.")
        st.balloons()

        # Realiza a soma horizontal de cada linha
        df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

        # Envia de volta para o Google Sheets
        conn.update(spreadsheet=url, data=df_editado)
        
        st.success("✅ SOMA REALIZADA! O Total XP foi atualizado na planilha.")
        st.balloons()
        
        # Mostra o Ranking para confirmar a soma
        st.subheader("🏆 Ranking Atualizado")
        ranking = df_editado.iloc[:, [1, cols.index(col_total)]].sort_values(by=col_total, ascending=False)
        st.table(ranking)

except Exception as e:
    st.error(f"Erro técnico: {e}")
