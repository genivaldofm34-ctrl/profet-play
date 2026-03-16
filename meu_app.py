import streamlit as st
import os

# Configuração visual e Modo Escuro por padrão
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

# Estilização CSS para deixar com cara de App Profissional
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e7bcf;
        color: white;
        font-weight: bold;
    }
    h1 { color: #2e7bcf; text-align: center; }
    .aluno-card {
        padding: 10px;
        border-radius: 10px;
        background-color: #1e2630;
        margin-bottom: 10px;
        border: 1px solid #3e4a5b;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 PROFET PLAY")
st.write("---")

def carregar_dados(turma):
    arquivo = f"dados_alunos_{turma}.txt"
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            lista = []
            for linha in linhas:
                if "|" in linha:
                    partes = linha.strip().split("|")
                    nome = partes[0]
                    pontos = partes[-1]
                    lista.append([nome, pontos])
            return lista
    return []

# Menu de seleção bonito
st.subheader("📁 Selecione sua Turma")
turma_sel = st.selectbox("", ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"], label_visibility="collapsed")

if turma_sel:
    alunos = carregar_dados(turma_sel)
    if not alunos:
        st.error(f"⚠️ O arquivo 'dados_alunos_{turma_sel}.txt' não foi encontrado no GitHub.")
    else:
        st.success(f"Turma: {turma_sel.replace('_', ' ')}")
        for i, aluno in enumerate(alunos):
            nome, pontos = aluno
            # Criando um "card" para cada aluno
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{nome}**")
                with col2:
                    st.button(f"🏆 {pontos}", key=f"btn_{i}")

st.divider()
st.caption("Acesse do Safari e 'Adicione à tela de início'")
