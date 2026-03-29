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
    
    st.subheader("📋 Painel de Lançamento")
    
    # 2. EDITOR DE DADOS
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    st.divider()

    # 3. O BOTÃO DE SOMA FORÇADA
    if st.button("🚀 CALCULAR XP E SALVAR NO GOOGLE"):
        with st.spinner("Forçando cálculos..."):
            col_total = "TOTAL (XP)"
            
            # LISTA DE COLUNAS QUE NÃO SÃO NOTAS
            cols_ignoradas = [col_total, "Nº", "Número", "ANTERIOR", "DIFERENÇA", "ALUNOS", "NOME"]
            
            # PROCESSO DE "RESSURREIÇÃO":
            for col in df_editado.columns:
                if col not in cols_ignoradas:
                    # Remove espaços, troca vírgula por ponto e força virar número
                    df_editado[col] = pd.to_numeric(
                        df_editado[col].astype(str).str.replace(',', '.').str.strip(), 
                        errors='coerce'
                    ).fillna(0)

            # AGORA SIM, SOMAMOS TUDO QUE SOBROU
            cols_para_somar = [c for c in df_editado.columns if c not in cols_ignoradas]
            df_editado[col_total] = df_editado[cols_para_somar].sum(axis=1)

            # 4. SALVAMENTO
            conn.update(spreadsheet=url, data=df_editado)
            
            st.success(f"✅ SOMA REALIZADA! Colunas somadas: {', '.join(cols_para_somar)}")
            st.balloons()

except Exception as e:
    st.error(f"Erro no PROF PLAY: {e}")
