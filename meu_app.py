import streamlit as st
import os

# Configuração de App Profissional
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

# Estilos CSS para esconder a "sujeira" e deixar bonito
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .titulo { color: #2e7bcf; text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    .card-aluno {
        background-color: #1c2128;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #2e7bcf;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nome-aluno { color: #adbac7; font-size: 20px; font-weight: bold; }
    .stButton>button {
        background: linear-gradient(135deg, #2e7bcf, #1a4b8c);
        color: white;
        border-radius: 12px;
        border: none;
        font-size: 18px;
        padding: 10px 25px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">🎮 PROFET PLAY PLATFORM</p>', unsafe_allow_html=True)

def limpar_pontos(texto_sujo):
    # Essa função remove as vírgulas e zeros extras e pega só o último número (o total)
    partes = texto_sujo.strip().split(',')
    return partes[-1] if partes else "0"

def carregar_dados(turma):
    # Tenta achar o arquivo mesmo com nomes diferentes no GitHub
    possibilidades = [f"dados_alunos_{turma}.txt", "dados_alunos.txt"]
    for p in possibilidades:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return [linha.strip().split("|") for linha in f.readlines() if "|" in linha]
    return []

# Menu
turmas = ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"]
turma_sel = st.selectbox("📂 SELECIONE A TURMA", turmas)

if turma_sel:
    dados = carregar_dados(turma_sel)
    if not dados:
        st.error("Arquivo não encontrado. Verifique os nomes no GitHub.")
    else:
        st.success(f"Turma {turma_sel.replace('_', ' ')} carregada!")
        
        for i, aluno in enumerate(dados):
            nome = aluno[0]
            # Aqui limpamos aquela "coisa ridícula" de zeros e vírgulas
            pontos = limpar_pontos(aluno[1])
            
            # Criando o visual limpo
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"<div style='padding-top:10px'><span class='nome-aluno'>{nome}</span></div>", unsafe_allow_html=True)
                with col2:
                    if st.button(f"🏆 {pontos}", key=f"btn_{i}"):
                        st.toast(f"Ponto registrado para {nome}!")
                st.markdown("---")

st.caption("Versão Professor Protegida - Genivaldo")
