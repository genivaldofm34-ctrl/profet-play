import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="PROFET PLAY", layout="wide") # 'wide' para caber todas as colunas
st.title("🎮 PROFET PLAY - SISTEMA ATIVO")

url = "https://docs.google.com/spreadsheets/d/1BZi169dylkYOOqdwserIbYJ-w-ZOZXBQ04nRo6Dkufo/edit#gid=1926794755"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Lendo os dados brutos
    df = conn.read(spreadsheet=url, skiprows=7, ttl=0)
    
    # 2. Limpeza profunda das colunas
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Remove colunas fantasmas
    if "Número" in df.columns:
        df = df.drop(columns=["Número"])
    
    # 3. Garantindo que ALUNOS aceitem texto e notas aceitem números
    df["ALUNOS"] = df["ALUNOS"].astype(str).replace("0", "").replace("None", "")
    
    # 4. Interface de Edição
    st.subheader("📋 Painel de Lançamento de XP")
    df_editado = st.data_editor(
        df, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic"
    )

    # --- O MOTOR DE SOMA ---
    # Identifica todas as colunas de notas (que não são ALUNOS nem TOTAL)
    cols_notas = [c for c in df_editado.columns if "ALUNOS" not in c.upper() and "TOTAL" not in c.upper()]
    
    # Converte para número e soma linha por linha
    for col in cols_notas:
        df_editado[col] = pd.to_numeric(df_editado[col], errors='coerce').fillna(0)
    
    df_editado["TOTAL XP"] = df_editado[cols_notas].sum(axis=1)

    # 5. Ranking em Tempo Real
    st.divider()
    st.subheader("🏆 Ranking dos Ninjas")
    ranking = df_editado[["ALUNOS", "TOTAL XP"]].sort_values(by="TOTAL XP", ascending=False)
    st.dataframe(ranking, use_container_width=True, hide_index=True)

    if st.button("💾 SALVAR E SINCRONIZAR"):
        conn.update(spreadsheet=url, data=df_editado)
        st.success("Planilha atualizada com as somas!")
        st.balloons()

except Exception as e:
    st.error(f"Erro ao processar planilha: {e}")
