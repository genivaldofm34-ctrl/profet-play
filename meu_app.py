import streamlit as st
import os

# Configuração de Layout Larga (igual ao PC)
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="wide")

# CSS para imitar os botões e cards da image_f1bd20.png
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    .card-lenda { background-color: #d4af37; padding: 20px; border-radius: 10px; text-align: center; color: black; font-weight: bold; }
    .card-superacao { background-color: #e67e22; padding: 20px; border-radius: 10px; text-align: center; color: white; font-weight: bold; }
    .stButton>button { border-radius: 5px; font-weight: bold; text-transform: uppercase; }
    .btn-turma { background-color: #6c5ce7 !important; color: white !important; }
    .btn-aluno { background-color: #2ecc71 !important; color: white !important; }
    .btn-aula { background-color: #8e44ad !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Topo com Destaques (Igual ao PC)
col_lenda, col_sup = st.columns(2)
with col_lenda:
    st.markdown('<div class="card-lenda">👑 LENDA DA SEMANA<br>---</div>', unsafe_allow_html=True)
with col_sup:
    st.markdown('<div class="card-superacao">🚀 SUPERAÇÃO DA SEMANA<br>---</div>', unsafe_allow_html=True)

st.write("---")

# Barra de Ferramentas
c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
with c1:
    turma = st.selectbox("TURMA:", ["TURMA A", "6º ANO MAT", "6º ANO ARTES"])
with c2:
    st.text_input("NOVA TURMA:", placeholder="NOME DA TURMA...")
with c3:
    st.button("+ TURMA", use_container_width=True)
with c4:
    st.button("📁 IMPORTAR", use_container_width=True)

# Área de Ação do Aluno
ca1, ca2, ca3 = st.columns([2, 1, 1])
with ca1:
    st.text_input("NOME DO ALUNO:", placeholder="DIGITE O NOME...")
with ca2:
    st.button("+ ALUNO", use_container_width=True)
with ca3:
    st.button("🚀 NOVA AULA", use_container_width=True)

# Tabela de Dados (Simulando o grid do PC)
st.markdown("### 📊 ESTÚDIO DE PONTOS")
header = st.columns([2, 1, 1, 1, 1, 1, 1])
header[0].write("**PLAYER**")
header[1].write("**N1**")
header[2].write("**N2**")
header[3].write("**TOTAL**")
header[4].write("**PROG**")
header[5].write("**%**")
header[6].write("**AÇÃO**")

# Exemplo de aluno com os dados que vimos na image_f1bd7e.png
st.divider()
aluno_col = st.columns([2, 1, 1, 1, 1, 1, 1])
aluno_col[0].write("BIANCA")
aluno_col[1].write("0")
aluno_col[2].write("0")
aluno_col[3].write("**90**")
aluno_col[4].write("📈")
aluno_col[5].write("10%")
aluno_col[6].button("🏆", key="b1")

st.info("Para que os botões de '+ TURMA' e '+ ALUNO' funcionem no iPhone e salvem na tabela, precisamos agora conectar ao Google Sheets.")
