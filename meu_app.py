import streamlit as st
import os

# Configuração de Aparência (Igual ao que fizemos no CustomTkinter)
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

# Estilo para imitar o painel do Windows
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    .titulo-pc { color: #2e7bcf; font-family: 'Segoe UI', sans-serif; font-size: 35px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .card-aluno { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7bcf; margin-bottom: 10px; }
    .stSelectbox label { color: #2e7bcf !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo-pc">🎮 PROFET PLAY PLATFORM</p>', unsafe_allow_html=True)

# Função para carregar os dados (Tenta vários nomes de arquivo para não dar erro)
def carregar_dados(turma_nome):
    # Lista de possíveis nomes que o arquivo pode ter no GitHub
    arquivos_tentar = [
        f"dados_alunos_{turma_nome}.txt",
        "dados_alunos.txt",
        f"dados_alunos_{turma_nome.replace('º', '')}.txt"
    ]
    
    for nome_arq in arquivos_tentar:
        if os.path.exists(nome_arq):
            with open(nome_arq, "r", encoding="utf-8") as f:
                linhas = f.readlines()
                return [l.strip().split("|") for l in linhas if "|" in l]
    return []

# Menu de Turmas
turmas = ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"]
turma_sel = st.selectbox("📂 SELECIONE A TURMA PARA CARREGAR", turmas)

if turma_sel:
    alunos = carregar_dados(turma_sel)
    
    if not alunos:
        st.error(f"❌ Erro ao ler dados de {turma_sel}. Verifique se os arquivos .txt foram enviados corretamente ao GitHub.")
    else:
        st.info(f"✅ {len(alunos)} Alunos carregados com sucesso!")
        
        for i, aluno in enumerate(alunos):
            nome = aluno[0]
            pontos = aluno[1]
            
            # Layout de Linha (Nome e Botão de Troféu)
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {nome}")
                with col2:
                    # O botão com os pontos do aluno
                    if st.button(f"🏆 {pontos}", key=f"btn_{i}"):
                        st.balloons() # Efeito de festa ao clicar no ponto!
                st.markdown("---")

st.write("---")
st.caption("Conectado ao GitHub de Genivaldo - Versão Mobile")
