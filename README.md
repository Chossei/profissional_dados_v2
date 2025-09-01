# 🚀 Dashboard de Análise de Dados Profissionais

## 📋 Descrição do Projeto

Este projeto é um dashboard interativo desenvolvido em Streamlit para análise de dados salariais de profissionais da área de dados no Brasil. A aplicação oferece uma interface moderna e intuitiva para explorar padrões salariais, realizar análises estatísticas e executar testes de hipóteses.

## ✨ Funcionalidades Principais

### 🎯 Dashboard Interativo (`paginas/app2.py`)
- **Filtros Dinâmicos**: Filtros por idade e região geográfica
- **Análise Descritiva**: Estatísticas detalhadas com intervalos de confiança
- **Visualizações Estatísticas**: Gráficos de densidade, boxplots e barras
- **Testes de Hipóteses**: Comparação estatística entre categorias
- **Interface Responsiva**: Design moderno com identidade visual consistente

### 👨‍💻 Análise do Cientista de Dados (`paginas/cientista.py`)
- **Rotina de Trabalho**: Análise das atividades diárias
- **Técnicas e Métodos**: Uso de metodologias e abordagens
- **Tecnologias**: Stack tecnológico utilizado
- **Gestão de Tempo**: Distribuição temporal das atividades
- **Métricas de Resumo**: Top 3 categorias com frequências e percentuais

## 🏗️ Arquitetura do Projeto

```
profissional_dados_v2-main/
├── app.py                 # Arquivo principal de navegação
├── funcoes.py            # Módulo com todas as funções auxiliares
├── requirements.txt      # Dependências do projeto
├── .streamlit/          # Configurações do Streamlit
│   └── config.toml     # Tema e configurações da aplicação
├── paginas/            # Páginas da aplicação
│   ├── app2.py         # Dashboard interativo principal
│   └── cientista.py    # Análise específica do cientista de dados
├── base.csv            # Base de dados principal (salários)
├── cientista_a-c.csv   # Dados do cientista (parte A-C)
└── cientista_d.csv     # Dados do cientista (parte D)
```

## 🛠️ Tecnologias Utilizadas

- **Streamlit** >= 1.43.2 - Framework web para aplicações de dados
- **Pandas** >= 2.2.2 - Manipulação e análise de dados
- **NumPy** >= 2.0.2 - Computação numérica
- **Matplotlib** >= 3.10.0 - Criação de gráficos
- **Seaborn** >= 0.13.2 - Visualizações estatísticas avançadas
- **SciPy** >= 1.15.2 - Funções científicas e estatísticas
- **Tabulate** >= 0.9.0 - Formatação de tabelas

## 🚀 Como Executar

### 1. Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação
```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]
cd profissional_dados_v2-main

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3. Execução
```bash
# Execute a aplicação
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

## 📊 Estrutura dos Dados

### Base Principal (`base.csv`)
- **Salario**: Salário mensal em reais
- **Idade**: Idade do profissional
- **Estado**: Estado brasileiro
- **Carreira**: Nível (Júnior, Pleno, Sênior)
- **Experiencia**: Tempo de experiência
- **Genero**: Identidade de gênero
- **Raça**: Autoidentificação racial

### Bases do Cientista
- **`cientista_a-c.csv`**: Rotina, técnicas e tecnologias
- **`cientista_d.csv`**: Gestão de tempo no trabalho

## 🔧 Funcionalidades Técnicas

### Módulo `funcoes.py`
- **`ajustar_ordem()`**: Define ordem das categorias
- **`desc_ic()`**: Calcula estatísticas e intervalos de confiança
- **`grafico_density()`**: Cria gráficos de densidade
- **`graf_ic()`**: Gera gráficos de barras com ICs
- **`boxplot()`**: Cria boxplots com marcadores de média
- **`hipoteses()`**: Executa testes de hipóteses estatísticos
- **`plot_distribuicao()`**: Plota distribuições teóricas normais
- **`validar_dados()`**: Valida integridade dos dados

### Características dos Gráficos
- **Paleta de Cores Consistente**: Identidade visual unificada
- **Responsividade**: Adaptação automática ao tamanho da tela
- **Interatividade**: Elementos clicáveis e filtros dinâmicos
- **Acessibilidade**: Contraste adequado e legendas claras

## 🎨 Identidade Visual

### Paleta de Cores
- **Primária**: `#1E3A8A` (Azul escuro)
- **Secundária**: `#1E40AF` (Azul médio)
- **Destaque**: `#06B6D4` (Ciano)
- **Neutra**: `#F8FAFC` (Cinza claro)

### Design System
- **Gradientes**: Transições suaves entre cores
- **Sombras**: Profundidade visual com `box-shadow`
- **Bordas**: Cantos arredondados (`border-radius`)
- **Tipografia**: Hierarquia clara de títulos e textos

## 📈 Análises Disponíveis

### 1. Análise Descritiva
- Estatísticas básicas (média, mediana, desvio padrão)
- Intervalos de confiança (95%)
- Distribuição por categorias

### 2. Visualizações
- **Gráficos de Densidade**: Distribuição salarial por categoria
- **Boxplots**: Comparação visual entre grupos
- **Gráficos de Barras**: Frequências com intervalos de confiança

### 3. Testes de Hipóteses
- **Teste de Normalidade**: Shapiro-Wilk
- **Homogeneidade de Variâncias**: Teste de Bartlett
- **Comparação de Médias**: Teste t-Student
- **Transformações**: Log e Box-Cox para dados não normais

## 🔍 Casos de Uso

### Para Analistas de Dados
- Análise de mercado salarial
- Comparação entre diferentes perfis profissionais
- Identificação de fatores que influenciam salários

### Para Recursos Humanos
- Benchmarking salarial
- Análise de equidade salarial
- Planejamento de carreira

### Para Profissionais da Área
- Autoavaliação salarial
- Planejamento de desenvolvimento
- Negociação salarial

## 🚧 Limitações e Considerações

### Dados
- Coleta realizada em 2023
- Amostra não probabilística
- Possível viés de autodeclaração

### Análises
- Testes paramétricos assumem normalidade
- Transformações podem afetar interpretabilidade
- Correlação não implica causalidade

## 🔮 Melhorias Futuras

### Funcionalidades
- [ ] Exportação de relatórios em PDF
- [ ] Análise temporal (comparação entre anos)
- [ ] Machine Learning para predição salarial
- [ ] Dashboard mobile otimizado

### Técnicas
- [ ] Análise de cluster para segmentação
- [ ] Testes não paramétricos alternativos
- [ ] Visualizações 3D interativas
- [ ] Integração com APIs de dados externos

## 📚 Referências e Fontes

### Base de Dados
- **Dataset**: [State of Data Brazil 2023](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-2023)
- **Plataforma**: Kaggle
- **Coletor**: DataHackers

### Metodologia
- **Testes Estatísticos**: SciPy Documentation
- **Visualizações**: Matplotlib e Seaborn Guides
- **Streamlit**: Oficial Documentation

## 👥 Contribuição

### Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- **Python**: PEP 8
- **Documentação**: Docstrings Google Style
- **Commits**: Conventional Commits
- **Testes**: Pytest (quando implementado)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

- **Autor**: Átila Prudente Simões
- **Email**: chosseibr@gmail.com
- **LinkedIn**: https://br.linkedin.com/in/atila-prudente-simoes
- **GitHub**: https://github.com/Chossei

## 🙏 Agradecimentos

- **DataHackers**: Pela coleta e disponibilização dos dados
- **Streamlit**: Pela excelente ferramenta de desenvolvimento
- **Comunidade Python**: Pelas bibliotecas open-source de qualidade
- **Usuários**: Pelo feedback e sugestões de melhoria
- **Professor Dr. Ricardo Rocha**: Pela orientação em toda a elaboração do projeto

---


**⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!**
