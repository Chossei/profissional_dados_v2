import streamlit as st

st.markdown("""graph TD
    A(Início: Comparar Médias Salariais de Grupo 1 e Grupo 2) --> B{Tamanho da Amostra < 30?}

    B -- "Sim (Amostra Pequena)" --> C{Teste de Normalidade (Shapiro-Wilk)}
    B -- "Não (Amostra Grande)" --> F["Assume-se robustez pelo Teorema do Limite Central (TLC)"]

    C --> D{Dados seguem distribuição normal? (p > 0.05)}
    D -- "Não" --> E[Aplicar Transformação para Normalizar (Box-Cox)]
    D -- "Sim" --> F

    E --> F

    F --> G{Teste de Homogeneidade de Variâncias (Levene)}

    G --> H{As variâncias são homogêneas? (p > 0.05)}
    H -- "Sim" --> I[Executar Teste t-Student Padrão]
    H -- "Não" --> J[Executar Teste t de Welch (para variâncias desiguais)]

    I --> K(Calcular p-valor final)
    J --> K

    K --> L{p-valor < 0.05?}
    L -- "Sim" --> M(Conclusão: Rejeitar H₀. A diferença entre as médias é estatisticamente significativa.)
    L -- "Não" --> N(Conclusão: Não Rejeitar H₀. A diferença entre as médias NÃO é estatisticamente significativa.)
""")