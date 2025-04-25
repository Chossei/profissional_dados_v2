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

# Padrão, expansão da página

st.set_page_config(
    page_title="Análise Salarial",
    layout="wide",
    page_icon="💸",
    initial_sidebar_state="collapsed"  # opcional, se quiser a sidebar já aberta
)

# Carregando a base de dados
base = pd.read_csv('base2.csv', sep = ',', encoding = 'utf-8')

# Título e seleção das variáveis a serem analisadas
st.title('Análise de dados do profissional da área de dados no Brasil em 2023')

variavel = st.selectbox('Escolha a variável para análise', ['Cargo',  'Carreira', 'Genero', 'Raça', 'Experiencia'])

# Filtro para idade -----------------------------------------------------------------------------------------------

filtro1, filtro2 = st.columns(2, border = True)

with filtro1: 
    idad_valor = st.checkbox('Deseja filtrar por idade?')
    idade_min, idade_max = st.slider(label = 'Selecione a idade:',
                           min_value = int(np.min(base['Idade'])),
                           max_value = int(np.max(base['Idade'])),
                           value = [int(np.min(base['Idade'])), int(np.max(base['Idade']))],
                           disabled = not idad_valor)
    if idad_valor:
        base = base[(base['Idade'] >= idade_min) & (base['Idade'] <= idade_max)]

# Filtro por região -----------------------------------------------------------------------------------------------
with filtro2:
    estado_valor = st.checkbox('Deseja filtrar por Estado?')
    estados_ordenados = [
        'Acre (AC)', 'Alagoas (AL)', 'Amapá (AP)', 'Amazonas (AM)', 'Bahia (BA)', 
        'Ceará (CE)', 'Distrito Federal (DF)', 'Espírito Santo (ES)', 'Goiás (GO)', 
        'Maranhão (MA)', 'Mato Grosso (MT)', 'Mato Grosso do Sul (MS)', 'Minas Gerais (MG)', 
        'Pará (PA)', 'Paraíba (PB)', 'Paraná (PR)', 'Pernambuco (PE)', 'Piauí (PI)', 
        'Rio de Janeiro (RJ)', 'Rio Grande do Norte (RN)', 'Rio Grande do Sul (RS)', 
        'Rondônia (RO)', 'Roraima (RR)', 'Santa Catarina (SC)', 'São Paulo (SP)', 'Sergipe (SE)', 
        'Tocantins (TO)'
        ]
    estados = st.multiselect(label = 'Selecione os Estados de interesse:', options = estados_ordenados,
                      disabled = not estado_valor, placeholder = 'UF...')
    if estado_valor and estados:
        base = base[base['Estados'].isin(estados)] # o isin retorna True para cada observação com o elemento da lista estados



# definindo as funções que serão usadas

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
    return ordem


def desc_ic(variavel, base):

  # Ajustando a ordem das categorias
  ordem = ajustar_ordem(variavel)
  base[variavel] = pd.Categorical(base[variavel], categories = ordem, ordered=True)

  # Agrupar a base pela variável e calcular as estatísticas
  tabela = base.groupby(variavel)['Salario'].agg(['count', 'mean', 'std'])

  # Listas para armazenar os intervalos de confiança
  icinf = []
  icsup = []

  # Iterando sobre as linhas de tabela usando o índice real (não o índice numérico)
  for idx in tabela.index:
        media = tabela.loc[idx, 'mean']
        std = tabela.loc[idx, 'std']
        n = tabela.loc[idx, 'count']

        # Cálculo do intervalo de confiança inferior e superior
        icinf.append(media - 1.96 * std / np.sqrt(n))
        icsup.append(media + 1.96 * std / np.sqrt(n))

  # Adiciona as colunas de intervalo de confiança
  tabela['ic inf'] = icinf
  tabela['ic sup'] = icsup
  tabela.rename(columns = {
      'count': 'Frequência',
      'mean': 'Média',
      'std': 'Desvio padrão',
      'ic inf': 'I.C Inferior',
      'ic sup': 'I.C Superior'
  })

  tabela.columns = ['Tamanho', 'Média', 'Desvio padrão', 'I.C Inferior', 'I.C Superior']


  return tabela.round(2)

# def ajustar_caminho_imagem(texto_markdown):
#     # Expressão regular pra encontrar imagens no markdown
#     padrao = r"!\[.*?\]\((.*?)\)"
    
#     # Função auxiliar pra converter imagem pra base64
#     def converter_para_base64(match):
#         caminho_imagem = match.group(1)
#         try:
#             with open(caminho_imagem, "rb") as img_file:
#                 encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
#             return f'![Imagem](data:image/png;base64,{encoded_string})'
#         except Exception as e:
#             return f"Erro ao carregar imagem: {str(e)}"

#     # Substitui os caminhos de imagem pelo formato base64
#     texto_corrigido = re.sub(padrao, converter_para_base64, texto_markdown)
#     return texto_corrigido

 

def grafico_density(variavel, base):

    # Ajustando a ordem das categorias da variavel
    ordem = ajustar_ordem(variavel)
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

# Exemplo de uso no Streamlit
# fig = grafico_density('Cargo', base_dados)
# st.pyplot(fig)


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

    texto_final = ''
    grupo1 = base[base[variavel] == categoria1]['Salario'].dropna().to_list()
    grupo2 = base[base[variavel] == categoria2]['Salario'].dropna().to_list()

    # Teste Shapiro para normalidade
    norm1 = scipy.stats.shapiro(grupo1)
    norm2 = scipy.stats.shapiro(grupo2)

    if norm1[1] < 0.05 or norm2[1] < 0.05:
        texto_final += '''Os dados das categorias não seguem uma distribuição normal. Serão aplicadas transformações para realizar o teste de hipóteses.'''
        if np.mean(grupo1) > np.median(grupo1) and np.mean(grupo2) > np.median(grupo2):
            texto_final += '''\n\nComo os grupos são assimétricos à direita, para se aproximar de uma normal, utilizaremos transformação logarítmica.'''
            grupo1 = np.log(grupo1)
            grupo2 = np.log(grupo2)
        else:
            texto_final += '''Os dados são assimétricos. Será aplicada a transformação Box-Cox.
                '''
            grupo1 = scipy.stats.boxcox(grupo1)[0]
            grupo2 = scipy.stats.boxcox(grupo2)[0]
    else:
        texto_final = '''Os dados seguem uma distribuição normal.'''

    # Teste de Bartllet para verificar a variância
    teste_bartlett = scipy.stats.bartlett(grupo1, grupo2)[1]

    if teste_bartlett > 0.05:
        p_value = scipy.stats.ttest_ind(grupo1, grupo2)[1]
    else:
        p_value = scipy.stats.ttest_ind(grupo1, grupo2, equal_var=False)[1]

    if p_value < 0.0001:         
        texto_final2 = f'''<div style="padding: 1.5rem; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
<strong>H₀:</strong> μ<sub>{categoria1}</sub> = μ<sub>{categoria2}</sub><br>
<strong>H₁:</strong> μ<sub>{categoria1}</sub> ≠ μ<sub>{categoria2}</sub><br><br>
Como o p-valor é <i> < 0.0001 </i>, <strong>muito pequeno</strong>, com um nível de significância de 0.05, 
há evidências estatísticas suficientes para <strong>rejeitar H₀</strong> e afirmar que as médias salariais são diferentes.
</div>'''
    elif p_value > 0.0001 and p_value < 0.05:
        texto_final2 = f'''<div style="padding: 1.5rem; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
<strong>H₀:</strong> μ<sub>{categoria1}</sub> = μ<sub>{categoria2}</sub><br>
<strong>H₁:</strong> μ<sub>{categoria1}</sub> ≠ μ<sub>{categoria2}</sub><br><br>
Como o p-valor é <i>{p_value:.4f}</i>, <strong>menor que o nível de significância 0.05,</strong>, 
há evidências estatísticas suficientes para <strong>rejeitar H₀</strong> e afirmar que as médias salariais são diferentes.
</div>
''' 
    else:
        texto_final2 = f'''<div style="padding: 1.5rem; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd; font-size: 16px;">
<strong>H₀:</strong> μ<sub>{categoria1}</sub> = μ<sub>{categoria2}</sub><br>
<strong>H₁:</strong> μ<sub>{categoria1}</sub> ≠ μ<sub>{categoria2}</sub><br><br>
Como o p-valor é <i>{p_value:.4f}</i>, <strong>maior que o nível de significância 0.05</strong>, 
há evidências estatísticas suficientes para <strong>não rejeitar H₀</strong> e afirmar que as médias salariais são iguais.
</div>
'''

    return texto_final2

def plot_distribuicao(variavel, base, categoria1, categoria2):
    # Filtrando os dados e calculando estatísticas para a primeira categoria
    grupo1 = base[base[variavel] == categoria1]['Salario'].dropna()
    n_1 = len(grupo1)
    grupo1_mean = grupo1.mean()
    grupo1_std = grupo1.std() / np.sqrt(n_1)

    # Filtrando os dados e calculando estatísticas para a segunda categoria
    grupo2 = base[base[variavel] == categoria2]['Salario'].dropna()
    n_2 = len(grupo2)
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

texto_col1 = f'{desc_ic(variavel, base).to_markdown()}'
texto_col12 = f'{graf_ic(variavel, base)}'
texto_col3 = f'{grafico_density(variavel, base)}'
texto_col4 = f'{boxplot(variavel, base)}'


# # Criando as colunas
# col1, col2, col3, col4 = st.columns(4)

# col1.subheader('📊 Análise descritiva e Intervalos de confiança')
# col1.markdown(texto_col1)
# col1.markdown('---')
# col1.markdown(texto_col12)

# col2.subheader('🔍 Teste de Hipóteses')
# col2.markdown(texto_col2)


# col3.subheader('📈 Visualização da densidade')
# col3.markdown(texto_col3)

# col4.subheader('📊 Visualização dos boxplots')
# col4.markdown(texto_col4)
    

col1, col2 = st.columns([3,2], border = False, gap = 'medium')
with col1:
    
    #c1, c2 = st.columns(2, border = False)
    #with c1:
        st.subheader('📊 Sumário descritivo') 
        st.write(desc_ic(variavel, base))

    #with c2:
        #st.subheader('Intervalos de confiança')
        #fig_2 = graf_ic(variavel, base)
        #st.pyplot(fig_2)

with col2:
    fig_2 = graf_ic(variavel, base)
    st.subheader('🎯 Intervalos de confiança')
    st.pyplot(fig_2)
    #st.subheader('📈 Boxplots')
    #fig_3 = boxplot(variavel, base)
    #st.pyplot(fig_3)

st.divider()
    
col1, col2 = st.columns(2, border = False)

with col1:
    st.subheader('🌊 Distribuições estimadas dos grupos') 
    fig = grafico_density(variavel, base)
    st.pyplot(fig)

with col2: 
    st.subheader(f'📦 Salário por categoria')
    fig_3 = boxplot(variavel, base)
    st.pyplot(fig_3)

st.divider()
st.subheader('🧪 Teste de Hipóteses')
c1, c2, c3 = st.columns([2, 2, 3], border = False, vertical_alignment = 'top')
with c1: 
    lista = pd.Series(base[variavel].unique()).dropna()
    categoria1 = st.selectbox('Escolha a primeira categoria da variável', lista, key = 'cat1')
    lista2 = lista.loc[lista != categoria1]
    categoria2 = st.selectbox('Escolha a segunda categoria da variável', lista2, key = 'cat2')
    texto_col2 = hipoteses(variavel, categoria1, categoria2, base)
with c2:
    fig_4 = plot_distribuicao(variavel, base, categoria1, categoria2)
    st.pyplot(fig_4)
    #gera_curva_testes(variavel, base)
with c3:
      st.markdown(texto_col2, unsafe_allow_html = True)
