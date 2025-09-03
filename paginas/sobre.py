import streamlit as st

# --- Configuração da Página ---
st.set_page_config(page_title="Sobre o Projeto", layout = "centered")

# --- Conteúdo da Página ---

_, centro, _ = st.columns([1, 4, 1])
with centro:
    st.title("📊 Sobre o Projeto")

# Slide 1: Introdução e Fonte dos Dados
col1, col2 = st.columns(2)

with col1:
    st.header("🎯 Introdução")
    st.markdown("""
    **Apresentação do projeto de análise salarial de profissionais de dados no Brasil.**
    """)

with col2:
    st.header("📊 Fonte dos Dados")
    st.markdown("""
    **Datahackers - State of Data Brasil 2023**
    - **Período:** Novembro e dezembro de 2023
    - **Amostra:** 5.293 respondentes
    - **Metodologia:** Questionário online
    - **Foco:** Panorama do mercado de trabalho de dados no Brasil
    """)

st.divider()

# Slide 2: Agradecimentos e Streamlit
col1, col2 = st.columns(2)

with col1:
    st.header("🙏 Agradecimentos")
    st.markdown("""
    **Ricardo** - Orientação com Python e elaboração do dashboard
    """)

with col2:
    st.header("🛠️ Streamlit")
    st.markdown("""
    **Framework de código aberto para aplicações web interativas**
    - **Vantagem:** Simplicidade - sem necessidade de conhecimento em front-end
    - **Funcionalidades:** Gráficos, botões, sliders, caixas de seleção
    - **Público:** Ideal para cientistas de dados e analistas
    - **Objetivo:** Apresentar resultados de forma visual e acessível
    """)

st.divider()

# Slide 3: Metodologia
st.header("🔬 Metodologia")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Quantificação da Variável Salário")
    st.markdown("""
    - Transformação de faixas salariais em valores numéricos
    - Necessário para cálculos estatísticos
    """)

with col2:
    st.subheader("🎯 Variáveis de Análise (5)")
    st.markdown("""
    - **Cargo**
    - **Carreira**
    - **Experiência**
    - **Raça**
    - **Gênero**
    """)

st.divider()

# Slide 4: Tipos de Gráficos
st.header("📈 Tipos de Gráficos")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Gráfico de Intervalos de Confiança")
    st.markdown("""
    **Error Bar - Intervalo de Confiança 95%**
    - **Função:** Medir incerteza estatística
    - **Interpretação:** Sobreposição de barras sugere diferenças/igualdades
    - **Limitação:** Não substitui teste de hipóteses e pode cometer erro tipo I
    """)

with col2:
    st.subheader("📈 Distribuições Estimadas")
    st.markdown("""
    **Versão suavizada de histograma**
    - **Objetivo:** Mostrar distribuição dos dados de forma contínua
    - **Característica:** Distribuição teórica suavizada
    - **Uso:** Identificar forma da distribuição
    """)

with col3:
    st.subheader("📦 Boxplots")
    st.markdown("""
    **Resumo estatístico da distribuição**
    - **Outliers:** Possíveis valores atípicos
    - **Causa:** Quantificação da variável salário
    - **Interpretação:** Mediana, quartis e dispersão
    """)

st.markdown("---")

st.image('teste.png')
