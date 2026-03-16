import streamlit as st
import os

# Configuração de "App de Luxo" para iPhone
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

# Estilo visual (Cores da sua marca)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #2e7bcf, #1a4b8c);
        color: white;
        border: none;
        padding: 10px;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .aluno-box {
        padding: 15px;
        border-radius: 15px;
        background-color: #1e2630;
        margin-bottom: 10px;
        border: 1px solid #3e4a5b;
    }
    h1, h2 { text-align: center; color: #2e7bcf; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 PROFET PLAY")
st.subheader("Plataforma Mobile")

def carregar_alunos():
    # Ele vai tentar abrir o arquivo principal que vi na sua imagem
    arquivo = "dados_alunos.txt"
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            lista = []
            for linha in linhas:
                if "|" in linha:
                    partes = linha.strip().split("|")
                    nome = partes[0]
                    # Pega o último valor de pontos
                    pontos = partes[-1].split(",")[-1] if "," in partes[-1] else partes[-1]
                    lista.append({"nome": nome, "pontos": pontos})
            return lista
    return []

# Interface
st.markdown("### 👥 Lista de Alunos")
alunos = carregar_alunos()

if not alunos:
    st.warning("⚠️ O arquivo 'dados_alunos.txt' ainda não foi lido corretamente.")
else:
    for i, aluno in enumerate(alunos):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{aluno['nome']}**")
            with col2:
                st.button(f"🏆 {aluno['pontos']}", key=f"btn_{i}")
        st.markdown("---")

st.caption("Versão Professor - Use no Safari")
