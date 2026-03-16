import streamlit as st
import os

# 1. Configuração Estilo Painel PROFET
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .card-lenda { background-color: #f1c40f; padding: 15px; border-radius: 10px; text-align: center; color: black; font-weight: bold; margin-bottom: 5px; }
    .card-sup { background-color: #e67e22; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold; margin-bottom: 5px; }
    .card-record { background-color: #1e3799; padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; border: 1px solid #2e7bcf; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 45px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Cabeçalho (Destaques e Recorde)
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="card-lenda">👑 LENDA: BIANCA</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card-sup">🚀 SUPERAÇÃO: JONAS</div>', unsafe_allow_html=True)

st.markdown('<div class="card-record">🏆 NOSSO RECORD: 1.250 PONTOS</div>', unsafe_allow_html=True)

st.divider()

# 3. Painel de Comandos (Aqui estão todos os botões que faltavam!)
st.subheader("⚙️ COMANDOS DO PROFESSOR")

# Seleção da Turma
turma_sel = st.selectbox("TURMA ATIVA:", ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"])

# Botões em Lista (Para não sumirem no iPhone)
if st.button("➕ ADICIONAR NOVO ALUNO"):
    st.info("Função de cadastro preparada.")

if st.button("🚀 INICIAR NOVA AULA"):
    st.balloons()

if st.button("📁 IMPORTAR LISTA"):
    st.warning("Pronto para importar.")

st.text_input("NOME DO ALUNO PARA CADASTRO:", placeholder="Digite aqui...")

st.divider()

# 4. Estúdio de Pontos (Tabela Simplificada)
st.subheader("📊 ESTÚDIO DE PONTOS")

def carregar_simulado():
    return [["BIANCA", "90"], ["JONAS", "200"]]

alunos = carregar_simulado()

for i, aluno in enumerate(alunos):
    col_n, col_p, col_b = st.columns([3, 1, 1])
    col_n.write(f"👤 {aluno[0]}")
    col_p.write(f"🏆 {aluno[1]}")
    if col_b.button("PONTO", key=f"p_{i}"):
        st.toast(f"Ponto para {aluno[0]}")
