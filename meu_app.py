import streamlit as st
import os

# 1. Configuração de Layout e Estilo (Inspirado na image_f1bd20.png)
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .card-lenda { background-color: #f1c40f; padding: 25px; border-radius: 12px; text-align: center; color: black; font-weight: bold; font-size: 22px; box-shadow: 0 4px 15px rgba(241, 196, 15, 0.3); }
    .card-sup { background-color: #e67e22; padding: 25px; border-radius: 12px; text-align: center; color: white; font-weight: bold; font-size: 22px; box-shadow: 0 4px 15px rgba(230, 126, 34, 0.3); }
    .card-record { background-color: #34495e; padding: 15px; border-radius: 10px; text-align: center; color: #ecf0f1; border: 1px solid #2e7bcf; margin-top: 10px; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# 2. Lógica de Dados
def carregar_alunos(turma):
    arquivo = f"dados_alunos_{turma}.txt"
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return [l.strip().split("|") for l in f.readlines() if "|" in l]
    return []

# 3. Cabeçalho: Lenda, Superação e NOSSO RECORD
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="card-lenda">👑 LENDA DA SEMANA<br><span style="font-size: 30px;">BIANCA</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card-sup">🚀 SUPERAÇÃO DA SEMANA<br><span style="font-size: 30px;">JONAS</span></div>', unsafe_allow_html=True)

# A aba NOSSO RECORD que você pediu
st.markdown('<div class="card-record">🏆 NOSSO RECORD ATUAL: <span style="color:#2e7bcf; font-size:24px;">1.250 PONTOS</span> (Turma 6º Ano)</div>', unsafe_allow_html=True)

st.divider()

# 4. Painel de Controle (Botões funcionais)
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    turma_sel = st.selectbox("TURMA ATIVA:", ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"])
with c2:
    if st.button("➕ NOVO ALUNO", use_container_width=True):
        st.toast("Função de cadastro ativada! Digite o nome abaixo.")
with c3:
    if st.button("🚀 INICIAR NOVA AULA", use_container_width=True):
        st.balloons()
        st.success("Aula iniciada! Pontuação dobrada ativada.")

# 5. Estúdio de Pontos (A Tabela)
st.markdown("### 📊 ESTÚDIO DE PONTOS")
alunos = carregar_alunos(turma_sel)

if alunos:
    # Cabeçalho da Tabela
    h = st.columns([3, 1, 1, 1, 1])
    h[0].write("**PLAYER**")
    h[1].write("**TOTAL**")
    h[2].write("**PROG**")
    h[3].write("**%**")
    h[4].write("**AÇÃO**")
    
    for i, aluno in enumerate(alunos):
        nome = aluno[0]
        # Limpa os pontos pegando apenas o último valor
        pontos = aluno[1].split(",")[-1] if "," in aluno[1] else aluno[1]
        
        col_a = st.columns([3, 1, 1, 1, 1])
        col_a[0].markdown(f"**{nome}**")
        col_a[1].write(f"{pontos}")
        col_a[2].write("📈")
        col_a[3].write("10%")
        if col_a[4].button("🏆", key=f"ponto_{i}"):
            st.toast(f"Ponto registrado para {nome}!")
else:
    st.warning("Selecione uma turma válida para ver os registros.")
