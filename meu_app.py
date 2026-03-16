import streamlit as st
import os

# Configuração para o App parecer profissional no iPhone
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

st.title("🎮 PROFET PLAY")
st.subheader("Painel do Professor")

# Função para carregar os alunos dos seus arquivos .txt
def carregar_dados(turma):
    arquivo = f"dados_alunos_{turma}.txt"
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            # Lógica para ler seus dados (ajustada para o seu formato)
            linhas = f.readlines()
            lista = []
            for linha in linhas:
                partes = linha.strip().split("|")
                if len(partes) >= 2:
                    lista.append([partes[0], partes[1]])
            return lista
    return []

# Interface
turma_sel = st.selectbox("Selecione a Turma", ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"])

if turma_sel:
    alunos = carregar_dados(turma_sel)
    if not alunos:
        st.warning("Nenhum dado encontrado. Verifique se os arquivos .txt estão no GitHub.")
    else:
        for i, aluno in enumerate(alunos):
            nome, pontos = aluno
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**{nome}**")
            with col2:
                st.button(f"🏆 {pontos}", key=f"btn_{i}")

st.info("Para dar pontos pelo celular, precisaremos conectar um banco de dados depois. Por enquanto, veja se os nomes aparecem!")
