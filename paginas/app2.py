"""
Dashboard Interativo de Análise Salarial
========================================

Este dashboard permite analisar dados salariais de profissionais da área de dados
no Brasil, com filtros interativos, visualizações estatísticas e testes de hipóteses.

Funcionalidades:
- Filtros por idade e região
- Análise descritiva com intervalos de confiança
- Visualizações estatísticas (densidade, boxplot, barras)
- Testes de hipóteses entre categorias
- Interface responsiva e estilizada

Autor: [Seu Nome]
Data: 2025
"""

# Imports necessários
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import tabulate
import re
import base64
import scipy
import scipy.stats as stats

# Importar funções auxiliares
from funcoes import (
    ajustar_ordem, desc_ic, grafico_density, graf_ic, 
    boxplot, hipoteses, plot_distribuicao
)

# Configuração da página
st.set_page_config(
    layout="wide", 
    page_title="Dashboard Interativo - Profissionais de Dados"
)

# Carregamento dos dados
try:
    # Usar base2.csv que é a base tratada e limpa
    base = pd.read_csv('base2.csv', sep=',', encoding='utf-8')
    
    # Remover colunas vazias e "Unnamed"
    colunas_para_remover = [col for col in base.columns if col.startswith('Unnamed') or col == '']
    if colunas_para_remover:
        base = base.drop(columns=colunas_para_remover)
    
    
    # Limpeza inicial dos dados
    # Converter colunas numéricas
    base['Idade'] = pd.to_numeric(base['Idade'], errors='coerce')
    base['Salario'] = pd.to_numeric(base['Salario'], errors='coerce')
    
    # Remover linhas com dados inválidos nas colunas críticas
    base = base.dropna(subset=['Idade', 'Salario'])
        
except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    st.stop()

# Header estilizado
st.markdown("""
<div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 50%, #06B6D4 100%);
            border-radius: 15px; margin-bottom: 30px; border: 2px solid #0F172A; box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3);">
    <h1 style="color: white; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-size: 2.5em;">🚀 Dashboard Interativo</h1>
    <p style="color: #E0F2FE; margin: 8px 0 0 0; font-size: 18px; font-weight: 300; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Análise de dados do profissional da área de dados no Brasil em 2023</p>
</div>
""", unsafe_allow_html=True)

# Sidebar com filtros
with st.sidebar:
    st.markdown("**🔧 Filtros**", help="Configure os filtros para análise dos dados")
    
    # Garantir que os valores de idade são numéricos (dados já foram limpos no carregamento)
    idade_min_valor = int(base['Idade'].min())
    idade_max_valor = int(base['Idade'].max())
    
    idade_min, idade_max = st.slider(
        '📊 Selecione a faixa de idade',
        min_value=idade_min_valor,
        max_value=idade_max_valor,
        value=(idade_min_valor, idade_max_valor),
        key='idade_slider'
    )
    
    # Filtro de estado
    try:
        estados_ordenados = [
            'Acre (AC)', 'Alagoas (AL)', 'Amapá (AP)', 'Amazonas (AM)', 'Bahia (BA)', 
            'Ceará (CE)', 'Distrito Federal (DF)', 'Espírito Santo (ES)', 'Goiás (GO)', 
            'Maranhão (MA)', 'Mato Grosso (MT)', 'Mato Grosso do Sul (MS)', 'Minas Gerais (MG)', 
            'Pará (PA)', 'Paraíba (PB)', 'Paraná (PR)', 'Pernambuco (PE)', 'Piauí (PI)', 
            'Rio de Janeiro (RJ)', 'Rio Grande do Norte (RN)', 'Rio Grande do Sul (RS)', 
            'Rondônia (RO)', 'Roraima (RR)', 'Santa Catarina (SC)', 'São Paulo (SP)', 'Sergipe (SE)', 
            'Tocantins (TO)'
        ]
        estados = ['Todos'] + estados_ordenados
        estado_selecionado = st.selectbox(
            '🌍 Selecione o estado:',
            estados,
            key='estado_select'
        )
    except Exception as e:
        st.error(f"Erro ao carregar estados: {str(e)}")
        st.error(f"Colunas disponíveis: {base.columns.tolist()}")
        st.stop()
    
    # Botão para aplicar filtros
    aplicar_filtros = st.button('Aplicar filtros', type='primary', use_container_width=True)

# Inicializar estado dos filtros se não existir
if 'filtros_aplicados' not in st.session_state:
    st.session_state.filtros_aplicados = False
    st.session_state.base_filtrada = base.copy()
    st.session_state.idade_filtro = (idade_min_valor, idade_max_valor)
    st.session_state.estado_filtro = 'Todos'

# Garantir que base_filtrada sempre existe no session_state
if 'base_filtrada' not in st.session_state:
    st.session_state.base_filtrada = base.copy()

# Aplicar filtros aos dados apenas quando o botão for clicado
if aplicar_filtros:
    try:
        # Aplicar filtros
        if estado_selecionado != 'Todos':
            base_filtrada = base[(base['Idade'] >= idade_min) & (base['Idade'] <= idade_max) & (base['Estados'] == estado_selecionado)]
        else:
            base_filtrada = base[(base['Idade'] >= idade_min) & (base['Idade'] <= idade_max)]
        
    except Exception as e:
        st.error(f"Erro ao aplicar filtros: {str(e)}")
        st.error(f"Tipos de dados - Idade: {base['Idade'].dtype}, Estados: {base['Estados'].dtype}")
        st.error(f"Valores únicos de Idade: {base['Idade'].unique()[:10]}")
        st.stop()
else:
    base_filtrada = base

variavel = st.selectbox('Escolha a variável para análise', ['Cargo',  'Carreira', 'Genero', 'Raça', 'Experiencia'])

col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.subheader('📋 Sumário descritivo')
    try:
        resultado_desc = desc_ic(variavel, base_filtrada)
        if not resultado_desc.empty:
            st.write(resultado_desc)
        else:
            st.warning("Não foi possível gerar estatísticas para esta variável")
    except Exception as e:
        st.error(f"Erro ao gerar estatísticas: {str(e)}")

with col2:
    st.subheader('📊 Intervalos de Confiança')
    try:
        fig_ic = graf_ic(variavel, base_filtrada)
        if fig_ic is not None:
            st.pyplot(fig_ic)
        else:
            st.warning("Não foi possível gerar gráfico de intervalos de confiança")
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {str(e)}")


col1, col2 = st.columns(2)

with col1:
    st.subheader('🌊 Distribuições estimadas dos grupos')
    try:
        fig_density = grafico_density(variavel, base_filtrada)
        if fig_density is not None:
            st.pyplot(fig_density)
        else:
            st.warning("Não foi possível gerar gráfico de densidade")
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de densidade: {str(e)}")

with col2:
    st.subheader(f'📦 Salário por categoria')
    try:
        fig_boxplot = boxplot(variavel, base_filtrada)
        if fig_boxplot is not None:
            st.pyplot(fig_boxplot)
        else:
            st.warning("Não foi possível gerar boxplot")
    except Exception as e:
        st.error(f"Erro ao gerar boxplot: {str(e)}")

# Seção de teste de hipóteses
st.divider()
st.subheader('🧪 Teste de Hipóteses')

# Inicializar estado do teste de hipóteses se não existir
if 'teste_executado' not in st.session_state:
    st.session_state.teste_executado = False
if 'categoria1_teste' not in st.session_state:
    st.session_state.categoria1_teste = None
if 'categoria2_teste' not in st.session_state:
    st.session_state.categoria2_teste = None
if 'resultado_teste' not in st.session_state:
    st.session_state.resultado_teste = None
if 'figura_distribuicao' not in st.session_state:
    st.session_state.figura_distribuicao = None

# Colunas para o teste de hipóteses
c1, c2, c3 = st.columns([2, 2, 3], border=False, vertical_alignment='top')

with c1:   
    lista = pd.Series(base_filtrada[variavel].unique()).dropna()
    categoria1 = st.selectbox('Escolha a primeira categoria da variável', lista, key='cat1')
    lista2 = lista.loc[lista != categoria1]
    categoria2 = st.selectbox('Escolha a segunda categoria da variável', lista2, key='cat2')
    
    if st.button('Executar teste', type='primary', use_container_width=True):
        st.session_state.teste_executado = True
        st.session_state.categoria1_teste = categoria1
        st.session_state.categoria2_teste = categoria2
        
        # Executar teste com spinner informativo
        with st.spinner('Executando teste de hipóteses...'):
            try:
                resultado_teste = hipoteses(variavel, categoria1, categoria2, base_filtrada)
                figura_distribuicao = plot_distribuicao(variavel, base_filtrada, categoria1, categoria2)
                
                st.session_state.resultado_teste = resultado_teste
                st.session_state.figura_distribuicao = figura_distribuicao
            except Exception as e:
                st.error(f"Erro ao executar teste de hipóteses: {str(e)}")
                st.session_state.resultado_teste = None
                st.session_state.figura_distribuicao = None
        
        st.rerun()

with c2:   
    if st.session_state.teste_executado and st.session_state.figura_distribuicao is not None:
        try:
            st.pyplot(st.session_state.figura_distribuicao)
        except Exception as e:
            st.error(f"Erro ao exibir gráfico: {str(e)}")
    else:
        st.info("Selecione as categorias e clique em 'Executar teste' para ver a distribuição")

with c3:   
    if st.session_state.teste_executado and st.session_state.resultado_teste is not None:
        try:
            st.markdown(st.session_state.resultado_teste, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro ao exibir resultados: {str(e)}")
    else:
        st.info("Selecione as categorias e clique em 'Executar teste' para ver os resultados")

# Informações sobre o processo abaixo das colunas
if st.session_state.teste_executado and st.session_state.categoria1_teste and st.session_state.categoria2_teste:
    st.divider()
    
    # Verificar dados dos grupos
    try:
        grupo1 = base_filtrada[base_filtrada[variavel] == st.session_state.categoria1_teste]['Salario'].dropna()
        grupo2 = base_filtrada[base_filtrada[variavel] == st.session_state.categoria2_teste]['Salario'].dropna()
    except Exception as e:
        st.error(f"Erro ao acessar dados dos grupos: {str(e)}")
        grupo1 = pd.Series(dtype='float64')
        grupo2 = pd.Series(dtype='float64')
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.info("👥 **Informações dos grupos:**")
        st.write(f"**{st.session_state.categoria1_teste}:** {len(grupo1)} observações")
        st.write(f"**{st.session_state.categoria2_teste}:** {len(grupo2)} observações")
    
    with col_info2:
        st.info("⚙️ **Processo executado:**")
        st.write("• Teste de normalidade (Shapiro-Wilk)")
        st.write("• Verificação de homogeneidade (Bartlett)")
        st.write("• Transformações para dados não normais")
        st.write("• Teste t-Student para comparação")

# Footer estilizado
st.markdown("""
<div style="background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%); padding: 20px; border-radius: 15px; margin-top: 40px; text-align: center; border: 2px solid #0F172A;">
    <p style="color: #B8E6F3; margin: 0; font-size: 14px;">
        Desenvolvido com Streamlit e Python | Dados acessados em fevereiro de 2025
    </p>
    <p style="color: #E0F2FE; margin: 8px 0 0 0; font-size: 12px;">
        📊 Base de dados: <a href="https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-2023" target="_blank" style="color: #87CEEB; text-decoration: underline;">State of Data Brazil 2023</a> | Kaggle
    </p>
</div>
""", unsafe_allow_html=True)

