import streamlit as st
import os

# 1. Configuração de Sistema
st.set_page_config(page_title="PROFET PLAY", page_icon="🎮", layout="centered")

# Estilo para os Cards de Cálculo (Igual ao seu Excel/PC)
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .status-bom { color: #2ecc71; font-weight: bold; }
    .status-alerta { color: #f1c40f; font-weight: bold; }
    .record-box { background: linear-gradient(90deg, #1e3799, #2e7bcf); padding: 10px; border-radius: 8px; text-align: center; }
    .tabela-header { background-color: #1e1e1e; padding: 10px; border-radius: 5px; font-weight: bold; border-bottom: 2px solid #2e7bcf; }
    </style>
    """, unsafe_allow_html=True)

# 2. Topo com Recordes
st.markdown('<div class="record-box">🏆 NOSSO RECORD: 1.250 PONTOS</div>', unsafe_allow_html=True)
st.divider()

# 3. Lógica das Fórmulas (O Coração do App)
def calcular_metricas(n1, n2):
    total = n1 + n2
    porcentagem = (total / 1000) * 100  # Exemplo: meta de 1000 pontos
    progresso = "📈" if total > 100 else "📉"
    return total, porcentagem, progresso

# 4. Estúdio de Pontos com Cálculos Reais
st.subheader("📊 ESTÚDIO DE PONTOS (Fórmulas Ativas)")

# Cabeçalho da Tabela
h = st.columns([2, 1, 1, 1, 1])
h[0].write("PLAYER")
h[1].write("N1")
h[2].write("N2")
h[3].write("TOTAL")
h[4].write("PROG")

# Simulação de Dados (Onde as fórmulas vão agir)
# No futuro, esses números virão do seu arquivo ou planilha
dados_alunos = [
    {"nome": "BIANCA", "n1": 40, "n2": 50},
    {"nome": "JONAS", "n1": 100, "n2": 100},
]

for i, aluno in enumerate(dados_alunos):
    # Executando as fórmulas
    total, media, prog = calcular_metricas(aluno["n1"], aluno["n2"])
    
    c = st.columns([2, 1, 1, 1, 1])
    c[0].write(f"**{aluno['nome']}**")
    c[1].write(f"{aluno['n1']}")
    c[2].write(f"{aluno['n2']}")
    c[3].write(f"**{total}**") # Resultado da fórmula
    c[4].write(f"{prog}")      # Emojis automáticos

st.divider()

# 5. Botões de Ação
if st.button("🚀 PROCESSAR NOTAS E RECORDES"):
    st.balloons()
    st.success("Cálculos atualizados com sucesso!")
