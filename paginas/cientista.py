import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Bases de dados nova

base1 = pd.read_csv('cientista_a-c.csv', sep = ',', encoding = 'utf-8')
base2 = pd.read_csv('cientista_d.csv', sep = ',', encoding = 'utf-8')

# Definindo funções importantes

def plotar_barras(variaveis, base):
    # Separa as frequências das variáveis
    totais = base[variaveis].sum().sort_values()
    total_geral = totais.sum()

    # gera a figura e os eixos
    fig, ax = plt.subplots()
    totais.plot(kind = 'barh', color = 'steelblue', ax=ax)
    
    x_max = ax.get_xlim()[1]  # pega o valor máximo do eixo x

    for i, v in enumerate(totais):
        percentual = v / total_geral * 100
        if percentual >= 5:
            deslocamento = 0.02 * x_max  # 2% do tamanho do eixo x
            if v >= deslocamento * 4:  # se a barra for "grande o suficiente"
                x_text = v - deslocamento
                color = 'white'
            else:
                x_text = v + deslocamento
                color = 'black'

        ax.text(x_text, i, f'{percentual:.2f}%', color=color,
                fontweight='bold', va='center', fontsize=8)

    # para consertar o problema de porcentagens fora das barras
    ax.set_xlim(0, totais.max() * 1.15)
    plt.tight_layout()
    return fig

# Definindo as colunas para cada tipo de pergunta

# Quais das opções abaixo fazem parte da sua rotina no trabalho atual com ciência de dados?
variaveis_1 = base1.columns[1:13].to_list()

# Quais as técnicas e métodos listados abaixo você costuma utilizar no trabalho?
variaveis_2 = base1.columns[13:27].to_list()

# Quais dessas tecnologias fazem parte do seu dia a dia como cientista de dados?
variaveis_3 = base1.columns[27:].to_list()

# Em qual das opções abaixo você gasta a maior parte do seu tempo no trabalho?
variaveis_4 = base2.columns[1:].to_list()


# Página

st.title('Cientista de dados 👨‍💻')

graf1, graf2 = st.columns(2, border = True)

with graf1:
  st.markdown('### Rotina de trabalho')
  fig1 = plotar_barras(variaveis_1, base1)
  st.pyplot(fig1)

with graf2:
  st.markdown('### Técnicas e métodos usados no trabalho')
  fig2 = plotar_barras(variaveis_2, base1)
  st.pyplot(fig2)

graf3, graf4 = st.columns(2, border = True)

with graf3:
  st.markdown('### Tecnologias mais usadas no dia a dia')
  fig3 = plotar_barras(variaveis_3, base1)
  st.pyplot(fig3)

with graf4:
  st.markdown('### Técnicas e métodos que ocupam mais tempo no trabalho')
  fig4 = plotar_barras(variaveis_4, base2)
  st.pyplot(fig4)
