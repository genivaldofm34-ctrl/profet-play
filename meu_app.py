import streamlit as st
import os

# 1. Configuração de Layout
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .card-lenda { background-color: #f1c40f; padding: 20px; border-radius: 12px; text-align: center; color: black; font-weight: bold; margin-bottom: 10px; }
    .card-sup { background-color: #e67e22; padding: 20px; border-radius: 12px; text-align: center; color: white; font-weight: bold; margin-bottom: 10px; }
    .card-record { background: linear-gradient(90deg, #1e3799, #2e7bcf); padding: 15px; border-radius: 10px; text-align: center; color: white; margin-bottom: 20px; border: 1px solid #4a69bd; }
    
    /* Estilo dos Botões Grandes */
    .stButton>button {
        width: 100%;
        height: 50px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Topo (Lenda, Superação e Record)
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="card-lenda">👑 LENDA<br>BIANCA</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card-sup">🚀 SUPERAÇÃO<br>JONAS</div>', unsafe_allow_html=True)

st.markdown('<div class="card-record">🏆 NOSSO RECORD: 1.250 PONTOS</div>', unsafe_allow_html=True)

# 3. Painel de Ações (Botões um embaixo do outro para não sumirem)
st.markdown("### ⚙️ COMANDOS DO PROFESSOR")

# Turma primeiro
turma_sel = st.selectbox("TURMA ATIVA:", ["6º_ANO_MATEMÁTICA", "6º_ANO_ARTES", "TURMA_A"])

# Botões em lista vertical (garante que apareçam no iPhone)
if st.button("➕ ADICIONAR NOVO ALUNO"):
    st.info("Digite o nome no campo abaixo para cadastrar.")

nome_novo = st.text_input("NOME DO ALUNO:", placeholder="Ex: Lucas Silva")

if st.button("🚀 INICIAR NOVA AULA (PONTOS 2X)"):
    st.balloons()
    st.success("Modo Aula Ativado!")

if st.button("📂 IMPORTAR LISTA DO EXCEL"):
    st.warning("Conecte ao Google Sheets para importar arquivos.")

st.divider()

# 4. Tabela de Pontos
st.markdown("### 📊 ESTÚDIO DE PONTOS")
# Simulando a lista para você ver a cara da tabela
st.markdown(f"**Exibindo: {turma_sel}**")
col_p, col_v, col_a = st.columns([3, 1, 1])
col_p.write("**PLAYER**")
col_v.write("**TOTAL**")
col_a.write("**ADD**")

# Exemplo Bianca
c_p, c_v, c_a = st.columns([3, 1, 1])
c_p.markdown("👤 BIANCA")
c_v.markdown("**90**")
if c_a.button("🏆", key="b_bianca"):
    st.toast("Ponto para Bianca!")
