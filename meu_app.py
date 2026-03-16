import streamlit as st
import os

# 1. Visual Estilo PC (Modo Escuro e Cores Profet Play)
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #ffffff; }
    .titulo { color: #2e7bcf; text-align: center; font-size: 30px; font-weight: bold; }
    .card-aluno { 
        background-color: #1e1e1e; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #333;
        margin-bottom: 10px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2e7bcf, #1a4b8c);
        color: white;
        border-radius: 8px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">🎮 PROFET PLAY PLATFORM</p>', unsafe_allow_html=True)

# 2. Lógica de Turmas (Igual ao PC)
turmas = ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"]
turma_selecionada = st.selectbox("📂 Selecione a Turma", turmas)

def carregar_dados(turma):
    arquivo = f"dados_alunos_{turma}.txt"
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return [linha.strip().split("|") for linha in f.readlines()]
    return []

# 3. Exibição dos Alunos
if turma_selecionada:
    dados = carregar_dados(turma_selecionada)
    if dados:
        st.write(f"### 👥 Alunos: {turma_selecionada.replace('_', ' ')}")
        for i, aluno in enumerate(dados):
            nome = aluno[0]
            pontos = aluno[1]
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{nome}**")
                with col2:
                    # No PC o botão somava. Aqui na web, ele precisa de um Banco de Dados
                    # para salvar "para sempre". Por enquanto, ele exibe os pontos:
                    st.button(f"🏆 {pontos}", key=f"btn_{i}")
    else:
        st.error("⚠️ Arquivo da turma não encontrado no GitHub.")

# 4. Rodapé
st.markdown("---")
st.info("💡 Para os pontos salvarem de verdade pelo celular, precisamos conectar uma Planilha Google. Quer fazer isso agora?")
