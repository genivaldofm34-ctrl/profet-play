import streamlit as st
import os

# Configuração para o iPhone
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮")

st.title("🎮 PROFET PLAY")
st.subheader("Painel do Professor")

def carregar_dados(turma):
    # Ajustei aqui para buscar o nome exato do arquivo que está no seu GitHub
    arquivo = f"dados_alunos_{turma}.txt"
    
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            lista = []
            for linha in linhas:
                if "|" in linha:
                    partes = linha.strip().split("|")
                    nome = partes[0]
                    # Pega o último número da lista de pontos
                    pontos = partes[-1].split(",")[-1] if "," in partes[-1] else partes[-1]
                    lista.append([nome, pontos])
            return lista
    return []

# As turmas conforme aparecem nos seus arquivos .txt
opcoes_turmas = [
    "6º_ANO_MATEMÁTICA", 
    "6º_ANO_ARTES", 
    "TURMA_A"
]

turma_sel = st.selectbox("Selecione a Turma", opcoes_turmas)

if turma_sel:
    alunos = carregar_dados(turma_sel)
    if not alunos:
        st.error(f"Arquivo 'dados_alunos_{turma_sel}.txt' não encontrado no GitHub.")
    else:
        for i, aluno in enumerate(alunos):
            nome, pontos = aluno
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"👤 **{nome}**")
            with col2:
                st.button(f"🏆 {pontos}", key=f"btn_{i}")

st.divider()
st.caption("PROFET PLAY v1.0 - Acesse do seu iPhone")
