"""
Página de Análise do Cientista de Dados
=======================================

Esta página apresenta uma análise detalhada das práticas, técnicas e tecnologias
utilizadas pelos cientistas de dados no mercado brasileiro, com visualizações
interativas e métricas de resumo.

Autor: Átila Prudente Simões
Data: 28/08/2025
"""

# Imports necessários
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle

# Configurar estilo dos gráficos
plt.style.use('default')
sns.set_palette("husl")

# Carregamento dos dados
try:
    base1 = pd.read_csv('cientista_a-c.csv', sep=',', encoding='utf-8')
    base2 = pd.read_csv('cientista_d.csv', sep=',', encoding='utf-8')
except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    st.stop()


def plotar_barras_melhorado(variaveis, base, titulo, cor_principal='#2E86AB'):
    """
    Função melhorada para plotar gráficos de barras horizontais com design aprimorado.
    
    Args:
        variaveis (list): Lista de variáveis para análise
        base (pd.DataFrame): DataFrame com os dados
        titulo (str): Título do gráfico
        cor_principal (str): Cor principal das barras
        
    Returns:
        plt.Figure: Figura matplotlib com o gráfico
        
    Example:
        >>> fig = plotar_barras_melhorado(variaveis, df, "Título")
        >>> st.pyplot(fig)
    """
    try:
        # Separa as frequências das variáveis
        totais = base[variaveis].sum().sort_values(ascending=True)
        total_geral = totais.sum()
        
        # Filtrar apenas variáveis com dados
        totais = totais[totais > 0]
        
        if totais.empty:
            st.warning("Nenhum dado encontrado para esta categoria")
            return None
        
        # Criar figura com tamanho otimizado
        fig, ax = plt.subplots(figsize=(8, max(4, len(totais) * 0.3)))
        
        # Criar cor única para todas as barras
        cor_unica = cor_principal
        
        # Plotar barras horizontais
        bars = ax.barh(range(len(totais)), totais, color=cor_unica, alpha=0.8, 
                      edgecolor='white', linewidth=0.5)
        
        # Adicionar valores e percentuais nas barras
        for i, (v, bar) in enumerate(zip(totais, bars)):
            percentual = v / total_geral * 100
            # Posicionar apenas o percentual dentro da barra
            ax.text(v * 0.5, i, f'{percentual:.1f}%', 
                   ha='center', va='center', fontweight='bold', 
                   fontsize=7, color='white')
        
        # Configurações do gráfico
        ax.set_yticks(range(len(totais)))
        ax.set_yticklabels([var.replace('_', ' ').title() for var in totais.index], fontsize=8)
        ax.set_xlabel('Frequência', fontsize=10, fontweight='bold')
        
        # Adicionar grid sutil
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Remover bordas
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Ajustar layout
        plt.tight_layout()
        
        return fig
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico: {str(e)}")
        return None


def criar_metricas_resumo(variaveis, base, titulo):
    """
    Criar métricas de resumo para cada categoria.
    
    Args:
        variaveis (list): Lista de variáveis para análise
        base (pd.DataFrame): DataFrame com os dados
        titulo (str): Título da seção
        
    Example:
        >>> criar_metricas_resumo(variaveis, df, "Título")
    """
    try:
        totais = base[variaveis].sum().sort_values(ascending=False)
        total_geral = totais.sum()
        
        # Top 3 mais frequentes
        top3 = totais.head(3)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total de respostas",
                value=f"{total_geral:,}",
                delta=None
            )
        
        with col2:
            if len(top3) > 0:
                st.metric(
                    label=top3.index[0].replace('_', ' ').title(),
                    value=f"{top3.iloc[0]:,}",
                    delta=None
                )
                st.caption(f"{(top3.iloc[0]/total_geral*100):.1f}% do total")
        
        with col3:
            if len(top3) > 1:
                st.metric(
                    label=top3.index[1].replace('_', ' ').title(),
                    value=f"{top3.iloc[1]:,}",
                    delta=None
                )
                st.caption(f"{(top3.iloc[1]/total_geral*100):.1f}% do total")
        
        with col4:
            if len(top3) > 2:
                st.metric(
                    label=top3.index[2].replace('_', ' ').title(),
                    value=f"{top3.iloc[2]:,}",
                    delta=None
                )
                st.caption(f"{(top3.iloc[2]/total_geral*100):.1f}% do total")
            
    except Exception as e:
        st.error(f"Erro ao criar métricas: {str(e)}")


# Definição das variáveis para cada tipo de pergunta
variaveis_1 = base1.columns[1:13].to_list()   # Rotina de trabalho
variaveis_2 = base1.columns[13:27].to_list()  # Técnicas e métodos
variaveis_3 = base1.columns[27:].to_list()    # Tecnologias
variaveis_4 = base2.columns[1:].to_list()     # Tempo no trabalho

# Configuração da página
st.set_page_config(layout="wide", page_title="Cientista de Dados - Análise")

# Header estilizado
st.markdown("""
<div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 50%, #06B6D4 100%); 
            border-radius: 15px; margin-bottom: 30px; border: 2px solid #0F172A; box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3);">
    <h1 style="color: white; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-size: 2.5em;">👨‍💻 Cientista de Dados</h1>
    <p style="color: #E0F2FE; margin: 8px 0 0 0; font-size: 18px; font-weight: 300; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Análise das práticas e tecnologias do mercado</p>
</div>
""", unsafe_allow_html=True)

# Primeira seção: Rotina de trabalho
st.markdown("---")
st.markdown("## Quais das opções abaixo fazem parte da sua rotina no trabalho atual com ciência de dados?")

# Métricas de resumo
criar_metricas_resumo(variaveis_1, base1, "Rotina de Trabalho")

# Gráfico principal
fig1 = plotar_barras_melhorado(variaveis_1, base1, "Rotina de Trabalho", "#2E86AB")
if fig1:
    st.pyplot(fig1)

# Segunda seção: Técnicas e métodos
st.markdown("---")
st.markdown("## Quais as técnicas e métodos listados abaixo você costuma utilizar no trabalho?")

# Métricas de resumo
criar_metricas_resumo(variaveis_2, base1, "Técnicas e Métodos")

# Gráfico principal
fig2 = plotar_barras_melhorado(variaveis_2, base1, "Técnicas e Métodos", "#A23B72")
if fig2:
    st.pyplot(fig2)

# Terceira seção: Tecnologias
st.markdown("---")
st.markdown("## Quais dessas tecnologias fazem parte do seu dia a dia como cientista de dados?")

# Métricas de resumo
criar_metricas_resumo(variaveis_3, base1, "Tecnologias")

# Gráfico principal
fig3 = plotar_barras_melhorado(variaveis_3, base1, "Tecnologias", "#F18F01")
if fig3:
    st.pyplot(fig3)

# Quarta seção: Tempo no trabalho
st.markdown("---")
st.markdown("## Em qual das opções abaixo você gasta a maior parte do seu tempo no trabalho?")

# Métricas de resumo
criar_metricas_resumo(variaveis_4, base2, "Tempo no Trabalho")

# Gráfico principal
fig4 = plotar_barras_melhorado(variaveis_4, base2, "Tempo no Trabalho", "#C73E1D")
if fig4:
    st.pyplot(fig4)

# Footer informativo
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 15px; background-color: #f0f2f6; border-radius: 8px;">
    <p style="margin: 0; color: #666; font-size: 14px;">
        📊 Dados coletados em 2023 | 📈 Análise interativa | 🎨 Visualizações aprimoradas
    </p>
</div>
""", unsafe_allow_html=True)
