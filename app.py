import streamlit as st

st.set_page_config(page_title='Profissional da Área de Dados',
                   layout='wide', page_icon = '📊',
                   initial_sidebar_state='expanded')

paginas = {
    'Análise de dados': [st.Page('paginas/app2.py', title='Dashboard Interativo da Faixa Salarial', default=True),
                        st.Page('paginas/cientista.py', title = 'Sobre o Cientista de Dados', default=False),
                        st.Page('paginas/teste.py', title = 'Programação em quatro mãos, 20 dedos', default=False)]
}

pag = st.navigation(paginas)
pag.run()
