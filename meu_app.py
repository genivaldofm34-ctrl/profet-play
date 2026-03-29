import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROF PLAY", layout="wide")
st.title("🎮 PROF PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. LEITURA
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')].copy()
    
    # LIMPEZA INICIAL (Troca None por 0 e vírgula por ponto)
    for c in df.columns:
        if c not in ["ALUNOS", "Nº", "Número"]:
            df[c] = df[c].astype(str).replace(['None', 'nan', 'nan '], '0')
            df[c] = df[c].str.replace(',', '.')
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

    # 3. O BOTÃO QUE NÃO ACEITA DESCULPAS (SOMA TUDO)
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        with st.spinner("Calculando XP..."):
            col_total = "TOTAL (XP)"
            
            # Lista de colunas para ignorar na soma
            cols_ignoradas = [col_total, "Nº", "Número", "ANTERIOR", "DIFERENÇA", "ALUNOS"]
            
            # Pega todas as colunas que sobraram e garante que são números
            cols_para_somar = [c for c in df_editado.columns if c not in cols_ignoradas]
            
            for c in cols_para_somar:
                df_editado[c] = pd.to_numeric(df_editado[c], errors='coerce').fillna(0)
            
            # FAZ A SOMA LINHA POR LINHA
            df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

            # 4. SALVA NO GOOGLE
            conn.update(spreadsheet=url, data=df_editado)
            
            st.success(f"✅ SOMA REALIZADA! Colunas detectadas: {len(cols_para_somar)}")
            st.balloons()
            
            # MOSTRA O RANKING PARA CONFIRMAR
            st.table(df_editado[["ALUNOS", col_total]].sort_values(by=col_total, ascending=False).head(5))

except Exception as e:
    st.error(f"Erro: {e}")
