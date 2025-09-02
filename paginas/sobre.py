import streamlit as st

# --- Configuração da Página ---
# Usar o layout "wide" dá mais espaço para o texto.
st.set_page_config(layout="wide", page_title="Guia da Apresentação")

# --- Início do Conteúdo da Apresentação ---

# Título Principal
st.title("📊 Análise Salarial de Profissionais de Dados no Brasil")
st.markdown("---") # Linha divisória

# Bloco 1: Introdução e Contexto
st.header("1. Introdução e Motivação")
st.markdown("""
Bem-vindo(a) ao nosso dashboard interativo!

O objetivo deste projeto é mergulhar no universo de dados para entender melhor o perfil e a remuneração dos profissionais que estão moldando o futuro da tecnologia no Brasil. Através desta análise, vamos explorar de forma dinâmica e visual o panorama salarial do setor, buscando insights que possam nos ajudar a compreender as tendências de mercado.
""")

st.divider() # Divisor visual para a próxima seção

# Bloco 2: Fonte dos Dados
st.header("2. 💾 A Fonte dos Dados: State of Data Brazil 2023")
st.markdown("""
Toda a nossa análise é baseada em uma fonte de dados pública, robusta e extremamente relevante: a pesquisa **"State of Data Brazil"**, realizada pelo **DataHackers**, uma das maiores e mais ativas comunidades de Ciência de Dados do país.

- **Período da Coleta:** Novembro e Dezembro de 2023.
- **Participantes:** **5.293 respondentes** de todo o Brasil.
- **Método:** Questionário online abrangendo perfil demográfico, formação, remuneração, satisfação e outros indicadores essenciais do mercado de trabalho.
""")

st.divider()

# Bloco 3: A Ferramenta
st.header("3. 🛠️ A Ferramenta: Por que Streamlit?")
st.markdown("""
Para dar vida a esses dados, a ferramenta escolhida foi o **Streamlit**, um framework open-source em Python que facilita a criação de aplicações web interativas.

A sua grande vantagem é a **simplicidade**. Ele permite que analistas e cientistas de dados transformem scripts de análise em interfaces visuais e acessíveis, sem a necessidade de conhecimento aprofundado em desenvolvimento front-end (HTML, CSS ou JavaScript).

Com o Streamlit, podemos criar gráficos, filtros e botões de forma rápida, permitindo que qualquer pessoa, mesmo sem conhecimento técnico, possa **explorar os dados e tirar suas próprias conclusões**.
""")

st.divider()

# Bloco 4: Metodologia e Foco da Análise
st.header("4. 🔬 Metodologia e Foco da Análise")
st.markdown("""
Antes de explorarmos os gráficos, é fundamental entender um passo importante da nossa metodologia.
""")

# Usando colunas para destacar a metodologia
col1, col2 = st.columns(2)

with col1:
    st.subheader("Quantificação da Variável Salarial")
    st.markdown("""
    Na pesquisa original, a remuneração era uma variável categórica, apresentada em **faixas salariais** (ex: "R$ 4.001 a R$ 6.000"). Para viabilizar cálculos estatísticos como a média, foi necessário **quantificar** esses dados, ou seja, transformar cada faixa em um valor numérico único (utilizamos o ponto médio de cada intervalo).
    """)

with col2:
    st.subheader("Foco da Análise")
    st.markdown("""
    Com os dados preparados, nosso foco de análise no dashboard será o cruzamento da remuneração com cinco **variáveis-chave** para entender as dinâmicas do mercado:
    - **Cargo**
    - **Nível de Carreira** (Júnior, Pleno, Sênior)
    - **Anos de Experiência**
    - **Raça**
    - **Gênero**
    """)

st.divider()

# Bloco 5: Guia de Interpretação dos Gráficos
st.header("5. 📈 Como Interpretar os Gráficos do Dashboard")
st.info("Abaixo estão as definições dos três tipos de visualização que você encontrará no dashboard. Entendê-los irá enriquecer sua exploração.")

# Explicação de cada gráfico
st.subheader("Gráfico de Intervalos de Confiança")
st.markdown("""
Este gráfico mostra a **média salarial** de cada grupo (a barra colorida) e o seu **intervalo de confiança de 95%** (a linha preta, ou *error bar*).

- **O que ele mede?** A incerteza estatística da nossa estimativa. Ele nos ajuda a visualizar se a diferença salarial entre dois grupos é estatisticamente significativa.
- **Como interpretar?** Uma grande sobreposição entre as barras de erro de dois grupos sugere que a diferença observada na amostra pode não existir na população geral.
""")
st.warning("**Atenção:** Uma análise visual não substitui um teste de hipótese formal. Ela é um forte indicativo, mas não uma prova estatística.", icon="⚠️")


st.subheader("Distribuições Estimadas (Gráfico de Densidade)")
st.markdown("""
Pense neste gráfico como uma **versão suavizada de um histograma**.

- **O que ele mostra?** A distribuição dos salários dentro de cada grupo, permitindo ver onde os salários se concentram mais.
- **Como interpretar?** Picos na curva indicam as faixas salariais mais comuns para aquele grupo. A largura da curva mostra a dispersão: curvas mais largas indicam maior variação salarial.
""")


st.subheader("Boxplots")
st.markdown("""
O boxplot é um resumo estatístico da distribuição salarial.

- **O que ele mostra?**
    - A **linha no meio da caixa** é a mediana (o salário do meio).
    - A **caixa** representa o intervalo interquartil (onde estão 50% dos salários).
    - As **linhas (ou bigodes)** mostram o alcance dos dados.
    - Os **pontos individuais** são considerados *outliers* (valores atipicamente altos ou baixos).
""")
st.warning("Alguns *outliers*, especialmente os mais altos, podem ser um artefato da metodologia de quantificação das faixas salariais.", icon="💡")

st.markdown("---")

_, centro, _ = st.columns([1, 3, 1])

with centro:
    st.image('teste.png', width = 500)