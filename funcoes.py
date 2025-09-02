"""
Módulo de Funções para Dashboard de Análise de Dados
===================================================

Este módulo contém todas as funções auxiliares utilizadas no dashboard interativo
para análise de dados de profissionais da área de dados no Brasil.

Funções incluídas:
- Ajuste de ordem de categorias
- Cálculo de estatísticas descritivas e intervalos de confiança
- Criação de gráficos (densidade, boxplot, barras)
- Testes de hipóteses estatísticos
- Validação de dados

Autor: Átila Prudente Simões
Data: 28/08/2025
"""

# Imports necessários
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
from scipy import stats

def ajustar_ordem(variavel):
    # Função para definir a ordem de exibição das categorias da variável
    if variavel == 'Cargo':
        ordem = ['Engenheiro de dados', 'Analista de Dados', 'Cientista de dados', 'Analista de BI', 'Outra opção']
    elif variavel == 'Experiencia':
        ordem = ['Até 2 anos', 'de 3 a 4 anos', 'de 4 a 6 anos', 'de 7 a 10 anos',
              'Mais de 10 anos']
    elif variavel == 'Genero':
        ordem = ['Masculino', 'Feminino', 'Outro']
    elif variavel == 'Raça':
        ordem = ['Parda', 'Branca', 'Preta', 'Amarela', 'Indígena', 'Outra', 'Não informado']
    elif variavel == 'Carreira':
        ordem = ['Júnior', 'Pleno', 'Sênior']
    else:
        # Se não encontrar uma ordem específica, retornar lista vazia
        return []
    return ordem


def desc_ic(variavel, base):

  # Ajustando a ordem das categorias
  ordem = ajustar_ordem(variavel)
  if not ordem:  # Se não houver ordem definida, usar valores únicos da base
      ordem = base[variavel].unique().tolist()
  
  base[variavel] = pd.Categorical(base[variavel], categories = ordem, ordered=True)

  # Agrupar a base pela variável e calcular as estatísticas
  tabela = base.groupby(variavel)['Salario'].agg(['count', 'mean', 'std'])

  # Listas para armazenar os intervalos de confiança
  icinf = []
  icsup = []

  # Lista para armazenar os coeficientes de variação
  cv = []

  # Iterando sobre as linhas de tabela usando o índice real (não o índice numérico)
  for idx in tabela.index:
        media = tabela.loc[idx, 'mean']
        std = tabela.loc[idx, 'std']
        n = tabela.loc[idx, 'count']

        # Cálculo do intervalo de confiança inferior e superior
        icinf.append(media - 1.96 * std / np.sqrt(n))
        icsup.append(media + 1.96 * std / np.sqrt(n))

        # Cálculo do CV
        cv.append(100 * np.round(std/media, 4))



  # Adiciona as colunas de intervalo de confiança e do cv
  tabela['cv'] = cv
  tabela['ic inf'] = icinf
  tabela['ic sup'] = icsup

  tabela.rename(columns = {
      'count': 'Frequência',
      'mean': 'Média',
      'std': 'Desvio Padrão',
      'cv': 'Coef. de Variação (%)',
      'ic inf': 'I.C Inferior',
      'ic sup': 'I.C Superior'
  })

  tabela.columns = ['Tamanho', 'Média', 'Desvio padrão', 'Coef. de Variação (%)', 'I.C Inferior', 'I.C Superior']


  return tabela.round(2)

def grafico_density(variavel, base):

    # Ajustando a ordem das categorias da variavel
    ordem = ajustar_ordem(variavel)
    if not ordem:  # Se não houver ordem definida, usar valores únicos da base
        ordem = base[variavel].unique().tolist()
    
    base[variavel] = pd.Categorical(base[variavel], categories=ordem, ordered=True)

    # Criando a figura
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plotando a curva de densidade de Kernel para cada categoria
    sns.kdeplot(data=base, x='Salario', hue=variavel, fill=True, common_norm=False, alpha=0.25, ax=ax)

    # Configurações do gráfico
    ax.set_title('Curvas de Densidade de Kernel por Categoria')
    ax.set_xlabel('Salário')
    ax.set_ylabel('Densidade')
    ax.grid(True)

    # Retornando a figura
    return fig

def graf_ic(variavel, base):
    # Criando a tabela
    tabela = desc_ic(variavel, base)

    # Reordena a tabela pela ordem das categorias do índice
    tabela = tabela.sort_index()

    # Inverte a ordem das categorias para o gráfico (para o primeiro ficar no topo)
    tabela = tabela.iloc[::-1]
    
    # Supondo que o índice do DataFrame sejam as categorias
    categorias = tabela.index
    medias = tabela['Média']
    ic_inferior = tabela['I.C Inferior']
    ic_superior = tabela['I.C Superior']

    # Calculando os erros
    erro_inferior = medias - ic_inferior
    erro_superior = ic_superior - medias

    # Criando a figura
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plotando barras horizontais
    ax.barh(categorias, medias, xerr=[erro_inferior, erro_superior], capsize=5, color='lightblue', edgecolor='black')
    ax.set_xlabel('Média')
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Retornando a figura
    return fig


def boxplot(variavel, base):

    ordem = ajustar_ordem(variavel)
    if not ordem:  # Se não houver ordem definida, usar valores únicos da base
        ordem = base[variavel].unique().tolist()

    base[variavel] = pd.Categorical(base[variavel], categories = ordem, ordered = True)

    # cria uma paleta com o mesmo número de cores das categorias
    paleta = sns.color_palette(n_colors=len(ordem))

    # mapeia as cores para cada categoria da variável
    cores_dict = dict(zip(ordem, paleta))
    
    # Criando a figura
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Criando o boxplot
    sns.boxplot(
        x=variavel, y='Salario', data=base, showmeans=True, palette=cores_dict,
        meanprops={'marker': 'D', 'markerfacecolor': 'red', 'markeredgecolor': 'black', 'markersize': 7},
        ax=ax
    )

    # Ajustes visuais
    ax.set_xlabel(variavel, fontsize=10)
    ax.set_ylabel('R$', fontsize=10)
    ax.set_title(f'Salário por {variavel}', fontsize=12)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    
    # Retornando a figura
    return fig



def hipoteses(variavel, categoria1, categoria2, base):
    try:
        texto_final = ''
        grupo1 = base[base[variavel] == categoria1]['Salario'].dropna()
        grupo2 = base[base[variavel] == categoria2]['Salario'].dropna()

        # Verificar se os grupos têm dados suficientes
        if len(grupo1) < 10 or len(grupo2) < 10:
            return f'''<div style="padding: 1.5rem; background-color: #fff3cd; border-radius: 10px; border: 1px solid #ffeaa7; font-size: 16px;">
<strong>⚠️ Dados insuficientes:</strong> (...)
</div>'''
        
        # Define o limite para considerar uma amostra "grande"
        LIMITE_AMOSTRA_GRANDE = 30 
        
        # 1. Lógica condicional baseada no tamanho da amostra
        # Se a amostra for pequena, verificamos a normalidade. Se for grande, confiamos no TLC.
        if len(grupo1) < LIMITE_AMOSTRA_GRANDE or len(grupo2) < LIMITE_AMOSTRA_GRANDE:
            # AMOSTRAS PEQUENAS: obrigatório testar normalidade
            norm1 = scipy.stats.shapiro(grupo1)
            norm2 = scipy.stats.shapiro(grupo2)

            if norm1[1] < 0.05 or norm2[1] < 0.05:
                # Dados não normais em amostra pequena -> TRANSFORMAÇÃO
                texto_final += 'Amostras pequenas e dados não-normais. Aplicando transformação Box-Cox para normalizar.'
                grupo1, _ = scipy.stats.boxcox(grupo1) # Usando a atribuição dupla para pegar só o array
                grupo2, _ = scipy.stats.boxcox(grupo2)
            else:
                texto_final = 'Amostras pequenas com dados normais.'
        else:
            # AMOSTRAS GRANDES: confiamos no Teorema do Limite Central
            texto_final = 'Amostras grandes detectadas. O Teste T é robusto devido ao Teorema do Limite Central, mesmo com pequenos desvios da normalidade.'
        
        # 2. Teste de Levene e Teste T (procedimento agora é o mesmo para ambos os casos)
        teste_levene = scipy.stats.levene(grupo1, grupo2)[1]

        if teste_levene > 0.05:
            p_value = scipy.stats.ttest_ind(grupo1, grupo2, equal_var=True)[1]
        else:
            p_value = scipy.stats.ttest_ind(grupo1, grupo2, equal_var=False)[1]
            
        # 3. Conclusão (mesma lógica de antes)
        # (O código para gerar o texto final com o p-valor seria o mesmo da sua função original)
        if p_value < 0.0001: # ... etc
             texto_final2 = f'''<div style="padding: 1.5rem; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
<strong>Contexto da Análise:</strong> {texto_final}<br><br>
<strong>H₀:</strong> μ<sub>{categoria1}</sub> = μ<sub>{categoria2}</sub><br>
<strong>H₁:</strong> μ<sub>{categoria1}</sub> ≠ μ<sub>{categoria2}</sub><br><br>
Como o p-valor é <i>&lt; 0.0001</i>, <strong>rejeitamos H₀</strong> e afirmamos que as médias salariais são diferentes.
</div>'''
        elif p_value > 0.0001 and p_value < 0.05:
             texto_final2 = f'''<div style="padding: 1.5rem; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
<strong>H₀:</strong> μ<sub>{categoria1}</sub> = μ<sub>{categoria2}</sub><br>
<strong>H₁:</strong> μ<sub>{categoria1}</sub> ≠ μ<sub>{categoria2}</sub><br><br>
Como o p-valor é <i>{p_value:.4f}</i>, <strong>menor que o nível de significância 0.05</strong>, 
há evidências estatísticas suficientes para <strong>rejeitar H₀</strong> e afirmar que as médias salariais são diferentes.
</div>
'''
        else: # Exemplo simplificado
            texto_final2 = f'''<div style="padding: 1.5rem; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
<strong>Contexto da Análise:</strong> {texto_final}<br><br>
<strong>H₀:</strong> μ<sub>{categoria1}</sub> = μ<sub>{categoria2}</sub><br>
<strong>H₁:</strong> μ<sub>{categoria1}</sub> ≠ μ<sub>{categoria2}</sub><br><br>
Como o p-valor é <i>{p_value:.4f}</i>, maior que o nível de significância de 5%, não há evidências estatísticas suficientes para <strong>rejeitar H₀</strong> e concluir que existe uma diferença significativa entre as médias salariais.
</div>'''

        return texto_final2

    except Exception as e:
        return f'''<div style="padding: 1.5rem; background-color: #f8d7da; border-radius: 10px; border: 1px solid #f5c6cb; font-size: 16px;">
<strong>❌ Erro ao executar teste de hipóteses:</strong> (...)
</div>'''

def plot_distribuicao(variavel, base, categoria1, categoria2):
    try:
        # Filtrando os dados e calculando estatísticas para a primeira categoria
        grupo1 = base[base[variavel] == categoria1]['Salario'].dropna()
        n_1 = len(grupo1)
        
        if n_1 < 2:
            raise ValueError(f"Grupo {categoria1} tem dados insuficientes: {n_1} observações")
            
        grupo1_mean = grupo1.mean()
        grupo1_std = grupo1.std() / np.sqrt(n_1)

        # Filtrando os dados e calculando estatísticas para a segunda categoria
        grupo2 = base[base[variavel] == categoria2]['Salario'].dropna()
        n_2 = len(grupo2)
        
        if n_2 < 2:
            raise ValueError(f"Grupo {categoria2} tem dados insuficientes: {n_2} observações")
            
        grupo2_mean = grupo2.mean()
        grupo2_std = grupo2.std() / np.sqrt(n_2)

        # Criando os eixos x para as distribuições
        x_1 = np.linspace(grupo1_mean - 4 * grupo1_std, grupo1_mean + 4 * grupo1_std, 1000)
        x_2 = np.linspace(grupo2_mean - 4 * grupo2_std, grupo2_mean + 4 * grupo2_std, 1000)

        # Calculando as funções de densidade de probabilidade (PDF)
        pdf_1 = stats.norm.pdf(x_1, loc=grupo1_mean, scale=grupo1_std)
        pdf_2 = stats.norm.pdf(x_2, loc=grupo2_mean, scale=grupo2_std)

        # Criando a figura
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Plotando as distribuições
        sns.lineplot(x=x_1, y=pdf_1, color='black', label=categoria1, ax=ax)
        sns.lineplot(x=x_2, y=pdf_2, color='red', label=categoria2, ax=ax)

        # Ajustes visuais
        ax.set_title(f'Distribuição de Salários para {categoria1} e {categoria2}')
        ax.set_xlabel('Salário')
        ax.set_ylabel('Densidade')
        ax.legend()

        # Retornando a figura
        return fig
        
    except Exception as e:
        # Retornar None em caso de erro para que o dashboard possa tratar adequadamente
        print(f"Erro na função plot_distribuicao: {str(e)}")
        return None
