"""
Aplicação Streamlit - Dashboard de Análise de Dados Profissionais
===============================================================

Este é o arquivo principal que configura a navegação entre as diferentes páginas
da aplicação de análise de dados de profissionais da área de dados no Brasil.

Autor: Átila Prudente Simões
Data: 28/08/2025
"""

import streamlit as st

# Configuração da página principal
st.set_page_config(
    page_title="Dashboard Profissionais de Dados",
    page_icon="🚀",
    layout="wide"
)

# Configuração da navegação entre páginas
paginas = {
    'Análise de dados': [
        st.Page('paginas/app2.py', title='Dashboard Interativo da Faixa Salarial', default=True),
        st.Page('paginas/cientista.py', title='Sobre o Cientista de Dados', default=False)
    ]
}

# Execução da navegação
pag = st.navigation(paginas)
pag.run()
