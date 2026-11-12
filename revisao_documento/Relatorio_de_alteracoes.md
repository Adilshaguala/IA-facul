# Relatório de alterações — IA trabalho 11.docx

## Resultado

O documento foi completado no ficheiro original. Uma cópia integral anterior à edição está guardada em `IA trabalho 11 - original.docx` nesta pasta.

Foram preservados os títulos, a sua ordem e níveis, as duas secções de página, as margens, a capa, a folha de rosto e as cinco tabelas existentes, incluindo as suas quantidades de linhas e colunas. O conteúdo acrescentado altera naturalmente o número de páginas. Não foram criados capítulos novos.

## Conteúdo completado e corrigido

- Resultados reais, sobreajuste, validação cruzada, discussão, resumo e conclusão quantitativa.
- Metodologia actualizada de 80/20 para 75/25; validação cruzada apenas no treino; remoção das descrições de uma experiência com árvore sem limite.
- A terceira linha já existente na tabela de resultados foi reaproveitada para a referência constante 'sempre 0'. Não é um terceiro modelo: acerta 60/105 casos, sem reconhecer qualquer positivo. Isto preserva a estrutura da tabela e contextualiza a exactidão.
- Implementação modular, interface, persistência, avaliação com rótulos opcionais e testes automatizados descritos segundo o código actual.
- Frase interrompida em 'Com isto' completada; acrescentado o enquadramento PEAS na secção existente de formulação. Remissões antigas para números de capítulos foram substituídas pelos títulos correspondentes.
- Limitações e benefícios potenciais distinguidos de resultados efectivamente medidos.
- Bibliografia original mantida e complementada com documentação oficial e documentos da disciplina. A referência Bigonha (2024) foi confirmada no PDF do autor, incluindo o ano.

## Figuras

1. `01_sigmoide` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.
2. `02_arvore_excerto` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.
3. `03_protocolo_experimental` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.
4. `04_metricas_teste` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.
5. `05_matrizes_confusao` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.
6. `06_treino_teste` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.
7. `07_validacao_cruzada` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.

## Validação

- 315 casos de treino e 105 de teste, sem identificadores partilhados; 179/136 e 60/45 casos das classes 0/1, respectivamente.
- Nova inferência concorda com resultados_grupo9.csv; treino em memória dos dois modelos reproduz as previsões guardadas.
- Validação cruzada recalculada com semente 42; médias e desvios-padrão conferidos. Os cinco valores por modelo constam de validacao_cruzada_verificada.csv.
- 11 testes automatizados do projecto executados com sucesso nesta revisão. Foram usados bancos temporários, sem adicionar exemplos ao histórico de utilização.
- Títulos, níveis, margens, secções, dimensões das tabelas e sete imagens conferidos por inspecção do documento. Ausência dos marcadores de preenchimento verificada.
- Os CSV, código da aplicação, modelos guardados e resultados originais não foram alterados. Os hashes constam do JSON de auditoria.

## Operações e ficheiros auxiliares

Foram instalados python-docx 1.2.0, lxml 6.1.3 e PyMuPDF 1.28.2 no ambiente virtual existente, exclusivamente para editar e verificar o documento. requirements.txt da aplicação não foi alterado.
A pasta contém o script de edição, os gráficos, os CSV verificados, a cópia original, uma cópia de trabalho e o registo detalhado de cada substituição e inserção. A edição não altera as bases de dados de testes individuais.

Formatação do conteúdo novo: figuras em linha com largura de 14,7 cm e texto alternativo; legendas de 10 pontos com espaçamento simples; excerto de código em Consolas de 9 pontos; células preenchidas da tabela de resultados com texto de 10 pontos; referências acrescentadas com avanço pendente de 0,6 cm. Estas definições não alteram os estilos globais, os títulos ou as dimensões das tabelas.

## Pontos que continuam a depender dos autores

1. A folha de rosto ainda contém o título 'Processo e Metodologia de Processo', diferente do tema da capa. Foi preservada conforme o pedido; os autores devem confirmar o título correcto.
2. Não há um conjunto próprio do problema do grupo disponível. A exigência dessa avaliação adicional está explicitada em Limitações; não foram inventados dados ou resultados.
3. A declaração de uso de IA exigida pela disciplina está preparada em ficheiro separado, como minuta. Os autores devem indicar apenas as verificações que efectivamente fizeram e juntar a declaração à submissão segundo a orientação da docente.
4. O texto teórico preexistente foi preservado, excepto na frase incompleta e nas passagens incompatíveis com o método executado. Recomenda-se rever com os autores a definição geral de inferência (que inicialmente descreve apenas a dedução) e as generalizações sobre a fiabilidade da indução.

## Registo integral

### Alteração 1 — substituição

Secção: Resumo.

**Motivo:** Incluir método actual e resultados efectivamente verificados no resumo.

**Antes:** Este trabalho aborda os fundamentos do Aprendizado Supervisionado, situando-o no quadro mais amplo da inferência lógica dedutiva e indutiva, e aplica esses fundamentos à construção de um classificador para pedidos de apoio académico submetidos por estudantes universitários. Dois algoritmos foram implementados e comparados — Regressão Logística e Árvore de Decisão — treinados e avaliados sobre o conjunto de dados de referência da turma (dados_referencia.csv, 420 registos), com recurso a validação cruzada e às métricas de exactidão, precisão, revocação e F1-score. Discute-se ainda uma limitação central do exercício: o modelo aprende a reproduzir decisões históricas, e não um critério objectivo de mérito, o que levanta questões de viés que devem ser consideradas na interpretação dos resultados.

**Depois:** Este trabalho aborda os fundamentos do Aprendizado Supervisionado, articulando a inferência dedutiva e indutiva com a construção de um classificador de pedidos de apoio académico. Comparam-se Regressão Logística e Árvore de Decisão com profundidade máxima de 5, sobre 420 pedidos fictícios do conjunto de referência da turma. A divisão estratificada reservou 315 casos para treino e 105 para teste, com semente 42; a validação cruzada de 5 partes foi realizada exclusivamente no treino. No teste, a Regressão Logística obteve 73,33% de exactidão e F1 de 0,659, enquanto a Árvore de Decisão atingiu 64,76% e 0,519, respectivamente. O protótipo inclui interface gráfica para testes em massa e individuais, com histórico persistente. A discussão considera a diferença treino/teste, os erros por classe e a limitação de aprender decisões históricas, que não constituem um critério independente de necessidade ou justiça.

### Alteração 2 — substituição

Secção: Introdução.

**Motivo:** Actualizar o roteiro, que omitia capítulos existentes e usava numeração desactualizada.

**Antes:** O trabalho está organizado da seguinte forma: o Capítulo 2 introduz os conceitos fundamentais de Inteligência Artificial; o Capítulo 3 aborda os tipos de inferência lógica — dedutiva e indutiva — e a sua relação com a IA; o Capítulo 4 apresenta o Aprendizado de Máquina, os seus tipos e, em particular, a metodologia, os algoritmos e os desafios do Aprendizado Supervisionado; por fim, apresentam-se as considerações finais.

**Depois:** O trabalho apresenta inicialmente a Introdução e os conceitos de Inteligência Artificial. Seguem-se os tipos de inferência e o Aprendizado de Máquina, a fundamentação dos algoritmos escolhidos, a descrição do problema e do artefacto, a implementação e os resultados. As secções finais discutem o desempenho, o impacto potencial, as limitações, as melhorias futuras e as conclusões, seguindo-se a bibliografia.

### Alteração 3 — substituição

Secção: Fundamentação Teórica dos Algoritmos Escolhidos.

**Motivo:** Substituir a remissão numérica desactualizada pelo título da secção existente.

**Antes:** Para além do enquadramento geral apresentado no capítulo anterior, importa aprofundar os dois algoritmos concretamente seleccionados para a construção do artefacto deste trabalho: a Regressão Logística e a Árvore de Decisão. A escolha destes dois algoritmos, em detrimento de outros referidos na secção 4.2.3, prende-se com o facto de ambos serem suficientemente distintos nos seus pressupostos e mecanismos de decisão — um linear e probabilístico, o outro hierárquico e baseado em regras —, permitindo uma comparação pedagogicamente rica sem introduzir a complexidade adicional de modelos como redes neurais ou métodos de ensemble.

**Depois:** Para além do enquadramento geral apresentado no capítulo anterior, importa aprofundar os dois algoritmos seleccionados para este artefacto: a Regressão Logística e a Árvore de Decisão. Entre os métodos referidos em «Metodologia: Algoritmos e Abordagens», estes dois possuem mecanismos de decisão distintos — um linear e probabilístico, o outro hierárquico e baseado em regras —, permitindo comparar duas abordagens sem acrescentar a complexidade de redes neurais ou conjuntos de modelos.

### Alteração 4 — substituição

Secção: Limitações relevantes para este trabalho:.

**Motivo:** Ligar a explicação à secção correcta e clarificar o papel da escala.

**Antes:** É sensível à escala das características — motivo pelo qual, na implementação, as variáveis numéricas foram normalizadas antes do treino (cf. Capítulo 7).

**Depois:** A escala das características influencia a optimização e a regularização; por isso, as entradas numéricas foram normalizadas durante o treino, conforme descrito em «Metodologia de Construção do Artefacto».

### Alteração 5 — substituição

Secção: Problema Social e Beneficiários.

**Motivo:** Corrigir a remissão antiga para o Capítulo 9.

**Antes:** Importa sublinhar, desde já, que o artefacto se destina a apoiar a decisão humana, e não a substituí-la — questão que é retomada, com maior profundidade crítica, no Capítulo 9.

**Depois:** O artefacto destina-se a apoiar a análise humana dos pedidos. As implicações e os limites deste uso são retomados nas secções «Discussão» e «Limitações».

### Alteração 6 — substituição

Secção: Metodologia de Construção do Artefacto.

**Motivo:** Substituir a remissão antiga para 4.2.4 pelo título da secção preservada.

**Antes:** A construção do artefacto seguiu o protocolo experimental descrito na secção 4.2.4, com as seguintes especificações concretas:

**Depois:** A construção do artefacto seguiu o enquadramento apresentado em «Protocolo Experimental», com as seguintes especificações concretas:

### Alteração 7 — substituição

Secção: Conclusão.

**Motivo:** Corrigir a remissão antiga para o Capítulo 4 e formular a conclusão sem equiparar formalmente o treino a um silogismo.

**Antes:** Verificou-se, em particular, que a aprendizagem supervisionada segue, na prática, uma estrutura semelhante à de um silogismo indutivo: a partir de exemplos rotulados (a premissa específica) e da suposição de que existe uma função capaz de generalizar esse mapeamento (a premissa geral), o algoritmo infere um modelo que permite prever resultados para novas entradas. Contudo, essa inferência nunca é absolutamente certa: está sempre sujeita a limitações como o overfitting, o underfitting, o desequilíbrio de classes e a qualidade dos dados rotulados, discutidas no Capítulo 4.

**Depois:** A aprendizagem supervisionada generaliza a partir de exemplos rotulados e de pressupostos sobre a relação entre entradas e saídas. O algoritmo ajusta uma função para produzir previsões em novas entradas; estas continuam sujeitas a incerteza e às limitações discutidas em «Desafios e Limitações», incluindo sobreajuste, subajuste, desequilíbrio de classes e qualidade dos rótulos.

### Alteração 8 — substituição

Secção: Silogismo.

**Motivo:** Completar a frase interrompida em «Com isto».

**Antes:** Em dedução a conclusão é sempre aceite como derivada de regras formais lógicas. Com isto 

**Depois:** Na dedução, a conclusão decorre das regras de inferência aplicadas às premissas. Com isto, a garantia de verdade exige simultaneamente um argumento válido e premissas verdadeiras; a validade da forma lógica, por si só, não demonstra que as premissas descrevem correctamente a realidade.

### Alteração 9 — substituição

Secção: Protocolo Experimental.

**Motivo:** Clarificar o protocolo de validação e distinguir possibilidades teóricas do procedimento executado.

**Antes:** Otimização de hiperparâmetros — utilizando validação cruzada (k-fold cross-validation) sobre o conjunto de validação.

**Depois:** Optimização de hiperparâmetros — pode recorrer a validação cruzada dentro do conjunto de treino, mantendo o teste isolado para a avaliação final. Neste trabalho, comparam-se configurações fixas; não foi realizada uma pesquisa de hiperparâmetros (scikit-learn developers, 2026c).

### Alteração 10 — inserção de texto

Secção: Regressão Logística.

**Texto:** Na configuração usada, o optimizador é L-BFGS, max_iter=1000 e C=1,0, com regularização L2 por omissão. Assim, a implementação acrescenta uma penalização dos coeficientes à perda apresentada, procurando limitar soluções excessivamente ajustadas ao treino (scikit-learn developers, 2026a). A Figura 1 ilustra a função sigmoide; não representa uma curva ajustada a uma única variável do conjunto de dados.

### Alteração 11 — inserção de figura

Secção: Regressão Logística.

**Ficheiro:** figuras/01_sigmoide.png

**Legenda:** Figura 1 — Função sigmoide e limiar de decisão. Ilustração matemática produzida para este trabalho, a partir de σ(z)=1/(1+e⁻ᶻ).

### Alteração 12 — inserção de legenda

Secção: Regressão Logística.

**Texto:** Figura 1 — Função sigmoide e limiar de decisão. Ilustração matemática produzida para este trabalho, a partir de σ(z)=1/(1+e⁻ᶻ).

### Alteração 13 — substituição

Secção: Árvore de Decisão.

**Motivo:** Retirar a experiência com um terceiro modelo que não faz parte da implementação actual.

**Antes:** É precisamente este último ponto que torna a Árvore de Decisão particularmente adequada aos objectivos pedagógicos deste trabalho: sem um limite de profundidade, o algoritmo continua a dividir os dados até que cada folha contenha um número muito reduzido de observações — no limite, uma única amostra —, memorizando efectivamente o conjunto de treino. Este comportamento é o exemplo mais directo e visualmente demonstrável de sobreajuste (cf. secção 4.2.5), razão pela qual, na implementação, se comparam explicitamente uma árvore com profundidade limitada e uma árvore sem qualquer limite (cf. Capítulo 8).

**Depois:** A profundidade limita o número de decisões sucessivas e ajuda a controlar a complexidade da árvore. Neste trabalho utiliza-se apenas max_depth=5, com critério de Gini e semente 42; o sobreajuste é analisado comparando o desempenho no treino, na validação cruzada e no teste. Não foi realizada uma experiência com árvore sem limite de profundidade (scikit-learn developers, 2026b).

### Alteração 14 — inserção de figura

Secção: Limitações relevantes para este trabalho:.

**Ficheiro:** figuras/02_arvore_excerto.png

**Legenda:** Figura 2 — Raiz e primeiro nível da Árvore de Decisão treinada. Os nós assinalados com reticências continuam até à profundidade máxima de 5. Os limiares numéricos usam a escala normalizada; values segue a ordem [0, 1]. Fonte: modelo guardado em artefactos/modelos.joblib.

### Alteração 15 — inserção de legenda

Secção: Limitações relevantes para este trabalho:.

**Texto:** Figura 2 — Raiz e primeiro nível da Árvore de Decisão treinada. Os nós assinalados com reticências continuam até à profundidade máxima de 5. Os limiares numéricos usam a escala normalizada; values segue a ordem [0, 1]. Fonte: modelo guardado em artefactos/modelos.joblib.

### Alteração 16 — inserção de texto

Secção: Formulação do Problema.

**Texto:** Como enquadramento PEAS, a medida de desempenho é dada pelas métricas de classificação e pelos erros por classe; o ambiente corresponde aos pedidos e ao processo de análise dos serviços académicos; os actuadores são as previsões, probabilidades e relatórios apresentados; e os sensores são as colunas recebidas por CSV ou formulário. O classificador aplica uma função aprendida a cada perfil, sem executar uma pesquisa de caminhos ou alterar automaticamente a situação administrativa do estudante. O histórico da interface serve à análise, sem actualizar os parâmetros dos modelos.

### Alteração 17 — substituição

Secção: Metodologia de Construção do Artefacto.

**Motivo:** Descrever os pipelines independentes e o isolamento do pré-processamento.

**Antes:** Pré-processamento: normalização (StandardScaler) das características numéricas e codificação one-hot (OneHotEncoder) das características categóricas (curso, ano, regime), integradas num pipeline único através de um ColumnTransformer da biblioteca scikit-learn.

**Depois:** Pré-processamento: StandardScaler para as sete entradas numéricas e OneHotEncoder para curso, ano e regime. Cada algoritmo possui um ColumnTransformer e um Pipeline independentes. A preparação é ajustada apenas nos dados usados no respectivo treino, incluindo cada parte da validação cruzada, para evitar fuga de informação (scikit-learn developers, 2026d).

### Alteração 18 — substituição

Secção: Metodologia de Construção do Artefacto.

**Motivo:** Actualizar 80/20 para a divisão 75/25 autorizada e executada.

**Antes:** Divisão treino/teste: 80% para treino e 20% para teste, com estratificação pela variável-alvo (garantindo proporções semelhantes de cada classe em ambos os conjuntos) e semente aleatória fixa (random_state = 42), assegurando a reprodutibilidade dos resultados.

**Depois:** Divisão treino/teste: 75% para treino (315 pedidos) e 25% para teste (105 pedidos), seleccionados aleatoriamente com estratificação por apoio_concedido e random_state=42. O treino contém 179 casos da classe 0 e 136 da classe 1; o teste contém 60 e 45, respectivamente. O ficheiro de referência é preservado; as partições são guardadas em dados_treino.csv e dados_teste.csv. Os documentos da disciplina não fixam uma percentagem de teste, exigindo que esta seja reportada (Rangel, 2026b).

### Alteração 19 — substituição

Secção: Metodologia de Construção do Artefacto.

**Motivo:** Corrigir a afirmação de validação sobre a totalidade dos dados.

**Antes:** Validação cruzada: 5-fold, aplicada sobre a totalidade dos dados, para obter uma estimativa mais robusta do desempenho de cada modelo.

**Depois:** Validação cruzada: StratifiedKFold com n_splits=5, shuffle=True e random_state=42, aplicado apenas aos 315 casos de treino. Em cada parte, 252 casos são usados no ajuste e 63 na validação; nenhum dos 105 casos de teste participa neste processo. Reportam-se média e desvio-padrão da exactidão entre as cinco partes.

### Alteração 20 — substituição

Secção: Metodologia de Construção do Artefacto.

**Motivo:** Registar exactamente os dois modelos e o âmbito da experiência.

**Antes:** Modelos treinados: Regressão Logística; Árvore de Decisão com profundidade máxima limitada (max_depth = 5); e Árvore de Decisão sem limite de profundidade, esta última incluída especificamente para demonstrar empiricamente o fenómeno de sobreajuste.

**Depois:** Modelos treinados: Regressão Logística (max_iter=1000) e Árvore de Decisão (max_depth=5), ambos com random_state=42 e restantes parâmetros por omissão. Não foram usados pesos de classe, reamostragem, procura automática de hiperparâmetros ou ajuste do limiar com os dados de teste.

### Alteração 21 — inserção de figura

Secção: Metodologia de Construção do Artefacto.

**Ficheiro:** figuras/03_protocolo_experimental.png

**Legenda:** Figura 3 — Protocolo experimental. A divisão externa usa semente 42 e estratificação; a validação cruzada ocorre dentro do treino. Fonte: dados.py e treino.py.

### Alteração 22 — inserção de legenda

Secção: Metodologia de Construção do Artefacto.

**Texto:** Figura 3 — Protocolo experimental. A divisão externa usa semente 42 e estratificação; a validação cruzada ocorre dentro do treino. Fonte: dados.py e treino.py.

### Alteração 23 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Actualizar a descrição para a aplicação modular com interface e persistência.

**Antes:** A implementação foi realizada em Python, recorrendo às bibliotecas pandas (manipulação de dados), scikit-learn (pré-processamento, modelos e métricas) e matplotlib (visualização). A lógica principal está organizada em sete etapas sequenciais:

**Depois:** A implementação foi realizada em Python 3.13, utilizando pandas e NumPy para os dados, scikit-learn para modelos e métricas, Matplotlib para gráficos exportados, Streamlit e Plotly para a interface, joblib para guardar os modelos e SQLite para o histórico. A lógica principal organiza-se nas sete etapas seguintes, distribuídas por módulos especializados:

### Alteração 24 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Actualizar a etapa de carregamento.

**Antes:** 1. Carregamento dos dados a partir do ficheiro dados_referencia.csv, com definição de uma semente aleatória fixa.

**Depois:** 1. Leitura e validação de dados_referencia.csv em dados.py, verificando o esquema, os tipos, os valores permitidos e os identificadores; definição da semente 42.

### Alteração 25 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Distinguir definição e ajuste para evitar uma descrição ambígua de fuga de informação.

**Antes:** 2. Definição do pré-processador: um ColumnTransformer que aplica StandardScaler às colunas numéricas e OneHotEncoder às colunas categóricas.

**Depois:** 2. Definição, em modelos.py, dos dois algoritmos e dos respectivos pré-processadores. Definir um Pipeline não o ajusta aos dados: esse ajuste ocorre apenas durante fit.

### Alteração 26 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Actualizar a divisão usada.

**Antes:** 3. Separação treino/teste (80/20), estratificada pela variável-alvo apoio_concedido.

**Depois:** 3. Divisão estratificada 75/25, sem sobreposição de identificadores, e gravação dos 315 casos de treino e 105 casos de teste nos ficheiros correspondentes.

### Alteração 27 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Alinhar a sequência com treino.py.

**Antes:** 4. Definição dos três modelos (Regressão Logística, Árvore de Decisão limitada e Árvore de Decisão sem limite), cada um encapsulado, em conjunto com o pré-processador, num Pipeline do scikit-learn — garantindo que o pré-processamento é ajustado apenas com os dados de treino, evitando fuga de informação (data leakage) do conjunto de teste.

**Depois:** 4. Validação cruzada de 5 partes exclusivamente nos dados de treino, através de cross_val_score e StratifiedKFold. O scikit-learn ajusta uma cópia independente de todo o Pipeline em cada parte.

### Alteração 28 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Explicitar o treino final e a avaliação externa.

**Antes:** 5. Treino de cada modelo (método fit) e cálculo das previsões sobre os conjuntos de treino e de teste.

**Depois:** 5. Ajuste final de cada Pipeline aos 315 casos de treino e previsão sobre treino e teste, mantendo os 105 casos de teste fora do ajuste dos parâmetros.

### Alteração 29 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Actualizar a avaliação e qualificar a interpretação da diferença treino/teste.

**Antes:** 6. Cálculo das métricas (exactidão, precisão, revocação, F1-score, matriz de confusão) e da validação cruzada de 5 folds; comparação entre a exactidão de treino e de teste, com sinalização automática quando a diferença sugere sobreajuste.

**Depois:** 6. Cálculo de exactidão, precisão, revocação, F1 e matrizes de confusão em avaliacao.py, e comparação da exactidão de treino com a de teste. A interface assinala uma diferença superior a 0,10 como indício a discutir, sem a tratar como prova estatística de sobreajuste.

### Alteração 30 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Descrever os artefactos e a interface actual.

**Antes:** 7. Produção de uma tabela final de resultados, no formato definido pelo guia de ficheiros de referência da turma, e de um gráfico comparativo das métricas entre os três modelos.

**Depois:** 7. Exportação dos resultados, gráficos, metadados e modelos. A interface app.py carrega os modelos ajustados para inferência em CSV ou formulário; os testes individuais são guardados por historico.py, sem voltar a treinar os classificadores.

### Alteração 31 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Substituir o excerto antigo de três modelos pelo fluxo actual; treino e teste são as partições já carregadas.

**Antes:** modelos = { 
    "Regressao Logistica": Pipeline([ 
        ("prep", pre_processador), 
        ("clf", LogisticRegression(max_iter=1000, random_state=SEED)), 
    ]), 
    "Arvore de Decisao": Pipeline([ 
        ("prep", pre_processador), 
        ("clf", DecisionTreeClassifier(max_depth=5, random_state=SEED)), 
    ]), 
    "Arvore de Decisao (sem limite)": Pipeline([ 
        ("prep", pre_processador), 
        ("clf", DecisionTreeClassifier(random_state=SEED)), 
    ]), 
}

**Depois:** from modelos import criar_modelos
from dados import ENTRADAS, ALVO, SEMENTE
from sklearn.model_selection import StratifiedKFold, cross_val_score

modelos = criar_modelos()
cv = StratifiedKFold(n_splits=5, shuffle=True,
                    random_state=SEMENTE)
for nome, modelo in modelos.items():
    scores = cross_val_score(
        modelo, treino[ENTRADAS], treino[ALVO],
        cv=cv, scoring="accuracy")
    modelo.fit(treino[ENTRADAS], treino[ALVO])
    previsoes = modelo.predict(teste[ENTRADAS])

### Alteração 32 — substituição

Secção: Descrição do Algoritmo Implementado em Python.

**Motivo:** Corrigir a indicação de que todo o código permanece num único ficheiro.

**Antes:** O código completo, incluindo o carregamento dos dados, o pré-processamento, o treino, a avaliação e a geração de gráficos, encontra-se no ficheiro classificador_apoio_academico.py, entregue em anexo a este artigo, conforme exigido pela estrutura do artefacto definida no programa da disciplina.

**Depois:** O ficheiro classificador_apoio_academico.py é a entrada de linha de comandos. O código completo distribui-se por dados.py (esquema e divisão), modelos.py (algoritmos), treino.py (ajuste e exportação), avaliacao.py (inferência e métricas), historico.py (persistência) e app.py (interface). As versões das dependências constam de requirements.txt, e as instruções de execução constam do README.md.

### Alteração 33 — inserção de texto

Secção: Descrição do Algoritmo Implementado em Python.

**Texto:** Na área de testes em massa, o utilizador carrega um CSV e recebe, para cada pedido, as previsões dos dois algoritmos, a probabilidade da classe 1, o resultado real quando disponível e a indicação de acerto. A análise inclui divergências, distribuição das previsões, comparação das probabilidades, métricas, matrizes de confusão e exportação CSV. A área individual apresenta um formulário; cada submissão acrescenta os resultados ao histórico SQLite e actualiza a análise acumulada. O formulário envia os valores em conjunto após a submissão (Streamlit, 2026).

### Alteração 34 — inserção de texto

Secção: Descrição do Algoritmo Implementado em Python.

**Texto:** As métricas do histórico utilizam apenas casos com resultado real conhecido e excluem entradas coincidentes com o treino. Os registos são separados por versão dos modelos, permanecem disponíveis após reiniciar a interface e não são duplicados por um simples recarregamento. Uma nova submissão, mesmo repetida, conta como um novo teste; a análise manual é exploratória e não substitui o teste reservado.

### Alteração 35 — inserção de texto

Secção: Descrição do Algoritmo Implementado em Python.

**Texto:** A verificação automatizada executou 11 testes com sucesso, cobrindo a separação e reprodutibilidade dos dados, o isolamento do pré-processamento e da validação, a igualdade entre inferência individual e em massa, a validação de CSV, casos sem rótulo, métricas conhecidas, persistência e fluxos da interface. Os testes de interface usaram o AppTest do Streamlit e bases temporárias; não constituem uma avaliação de usabilidade com estudantes.

### Alteração 36 — substituição

Secção: Apresentação e Discussão dos Resultados.

**Motivo:** Substituir o aviso de preenchimento por uma descrição verificável da experiência.

**Antes:** [ESTA SECÇÃO DEVE SER PREENCHIDA COM OS RESULTADOS REAIS, APÓS A EXECUÇÃO DO SCRIPT SOBRE O FICHEIRO dados_referencia.csv OFICIAL. A tabela e o texto abaixo são um modelo de preenchimento — os valores apresentados são ilustrativos e NÃO devem ser usados no artigo final.]

**Depois:** Os resultados apresentados nesta secção foram recalculados a partir dos dados e modelos do projecto, verificando a concordância com resultados_grupo9.csv. A comparação utiliza exactamente os mesmos 105 pedidos reservados para teste, sem introduzir valores ilustrativos. Os dados de referência são fictícios; a classe 1 representa a decisão histórica de conceder apoio.

### Alteração 37 — substituição

Secção: Resultados no conjunto de dados de referência.

**Motivo:** Introduzir os resultados reais e preservar as dimensões da tabela, substituindo a linha obsoleta por uma referência constante explícita.

**Antes:** A tabela seguinte apresenta os resultados obtidos pelos três modelos treinados sobre o conjunto de teste (20% dos dados, semente aleatória 42), no formato definido pelo guia de ficheiros de referência da turma:

**Depois:** A tabela seguinte apresenta o desempenho no conjunto de teste (25% dos 420 pedidos), com semente 42. A terceira linha fornece uma referência simples: prever sempre a classe 0, maioritária no treino. Esta regra não é um terceiro modelo treinado; permite avaliar se os dois classificadores superam uma previsão constante. Precisão, revocação e F1 referem-se à classe positiva 1.

### Alteração 38 — célula da tabela de resultados

**Antes:** dados_referencia

**Depois:** dados_referencia

### Alteração 39 — célula da tabela de resultados

**Antes:** Regressão Logística

**Depois:** Regressão Logística

### Alteração 40 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 73,33%

### Alteração 41 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 72,97%

### Alteração 42 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 60,00%

### Alteração 43 — célula da tabela de resultados

**Antes:** [X,XX]

**Depois:** 0,659

### Alteração 44 — célula da tabela de resultados

**Antes:** dados_referencia

**Depois:** dados_referencia

### Alteração 45 — célula da tabela de resultados

**Antes:** Árvore de Decisão (max_depth=5)

**Depois:** Árvore de Decisão
(max_depth=5)

### Alteração 46 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 64,76%

### Alteração 47 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 62,50%

### Alteração 48 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 44,44%

### Alteração 49 — célula da tabela de resultados

**Antes:** [X,XX]

**Depois:** 0,519

### Alteração 50 — célula da tabela de resultados

**Antes:** dados_referencia

**Depois:** dados_referencia

### Alteração 51 — célula da tabela de resultados

**Antes:** Árvore de Decisão (sem limite)

**Depois:** Referência: sempre 0
(sem treino)

### Alteração 52 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 57,14%

### Alteração 53 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 0,00%

### Alteração 54 — célula da tabela de resultados

**Antes:** [XX,X %]

**Depois:** 0,00%

### Alteração 55 — célula da tabela de resultados

**Antes:** [X,XX]

**Depois:** 0,000

### Alteração 56 — inserção de legenda

Secção: Resultados no conjunto de dados de referência.

**Texto:** Fonte: dados_referencia.csv; conjunto: teste; divisão treino/teste: 75%/25%; n=105; semente: 42. Na referência constante, a precisão é definida como zero por não haver previsões positivas, seguindo zero_division=0.

### Alteração 57 — inserção de figura

Secção: Resultados no conjunto de dados de referência.

**Ficheiro:** figuras/04_metricas_teste.png

**Legenda:** Figura 4 — Métricas dos dois classificadores no teste reservado. Os valores do gráfico são percentagens; na tabela, F1 é apresentado na escala de 0 a 1. Fonte: métricas recalculadas do projecto.

### Alteração 58 — inserção de legenda

Secção: Resultados no conjunto de dados de referência.

**Texto:** Figura 4 — Métricas dos dois classificadores no teste reservado. Os valores do gráfico são percentagens; na tabela, F1 é apresentado na escala de 0 a 1. Fonte: métricas recalculadas do projecto.

### Alteração 59 — inserção de texto

Secção: Resultados no conjunto de dados de referência.

**Texto:** A Regressão Logística classificou correctamente 77 dos 105 pedidos, contra 68 da Árvore de Decisão. A diferença de exactidão foi de 8,57 pontos percentuais; as diferenças de precisão, revocação e F1 foram de 10,47, 15,56 e 13,91 pontos percentuais, respectivamente, em favor da Regressão Logística. A referência constante acertou 60 pedidos (57,14%), mas não identificou nenhum dos 45 apoios concedidos.

### Alteração 60 — inserção de figura

Secção: Resultados no conjunto de dados de referência.

**Ficheiro:** figuras/05_matrizes_confusao.png

**Legenda:** Figura 5 — Matrizes de confusão com contagens absolutas. Linhas: classe real; colunas: classe prevista; ordem [0, 1]. Fonte: inferência dos modelos nos 105 pedidos de teste.

### Alteração 61 — inserção de legenda

Secção: Resultados no conjunto de dados de referência.

**Texto:** Figura 5 — Matrizes de confusão com contagens absolutas. Linhas: classe real; colunas: classe prevista; ordem [0, 1]. Fonte: inferência dos modelos nos 105 pedidos de teste.

### Alteração 62 — inserção de texto

Secção: Resultados no conjunto de dados de referência.

**Texto:** Na Regressão Logística, a matriz contém 50 verdadeiros negativos, 10 falsos positivos, 18 falsos negativos e 27 verdadeiros positivos. Na Árvore de Decisão, as contagens são 48, 12, 25 e 20, respectivamente. Assim, a árvore falhou 25 dos 45 casos historicamente concedidos (55,56%), enquanto a regressão falhou 18 (40,00%). Um falso negativo significa discordância com uma concessão histórica, não demonstra, isoladamente, uma decisão injusta. Por exemplo, na regressão: precisão=27/(27+10)=72,97%; revocação=27/(27+18)=60,00%; F1=54/(54+10+18)=0,659.

### Alteração 63 — substituição

Secção: Análise do sobreajuste.

**Motivo:** Preencher a análise de sobreajuste com resultados reais dos dois modelos.

**Antes:** [Preencher com a comparação real entre a exactidão de treino e de teste para cada modelo, e comentar se o gap observado confirma o comportamento teórico esperado (secção 4.2.5): a árvore sem limite de profundidade deverá apresentar exactidão próxima de 100% no treino e uma queda no teste.]

**Depois:** A Regressão Logística apresentou exactidão de 77,78% no treino e 73,33% no teste, com uma diferença de 4,44 pontos percentuais. Na Árvore de Decisão, a exactidão passou de 82,54% para 64,76%, uma diferença de 17,78 pontos percentuais. A árvore ajustou melhor os casos de treino, mas apresentou pior desempenho em dados não usados no ajuste. O padrão sugere maior sobreajuste nesta configuração, mesmo com max_depth=5; uma divisão única não permite provar a sua causa. Como não foram comparadas outras profundidades, estes resultados não medem o efeito causal de alterar max_depth.

### Alteração 64 — inserção de figura

Secção: Análise do sobreajuste.

**Ficheiro:** figuras/06_treino_teste.png

**Legenda:** Figura 6 — Exactidão no treino e no teste. Diferenças: 4,44 pontos percentuais na Regressão Logística e 17,78 na Árvore de Decisão. Fonte: resultados_grupo9.csv, verificado por nova inferência.

### Alteração 65 — inserção de legenda

Secção: Análise do sobreajuste.

**Texto:** Figura 6 — Exactidão no treino e no teste. Diferenças: 4,44 pontos percentuais na Regressão Logística e 17,78 na Árvore de Decisão. Fonte: resultados_grupo9.csv, verificado por nova inferência.

### Alteração 66 — substituição

Secção: Validação cruzada.

**Motivo:** Preencher a média, dispersão e interpretação da validação cruzada.

**Antes:** [Preencher com a média e o desvio-padrão da exactidão obtida na validação cruzada de 5 folds, para cada modelo, e comentar a estabilidade dos resultados face à divisão única treino/teste.]

**Depois:** Na validação cruzada de 5 partes dentro do treino, a Regressão Logística atingiu exactidão média de 75,24%, com desvio-padrão de 2,15 pontos percentuais. A Árvore de Decisão obteve 67,62%, com desvio-padrão de 4,56 pontos percentuais. A Regressão Logística teve maior média e menor dispersão entre as partes, coerentemente com o teste reservado. Estes desvios-padrão descrevem a variação entre cinco partes com treinos sobrepostos; não são intervalos de confiança nem demonstram significância estatística da diferença (scikit-learn developers, 2026c).

### Alteração 67 — inserção de figura

Secção: Validação cruzada.

**Ficheiro:** figuras/07_validacao_cruzada.png

**Legenda:** Figura 7 — Exactidão em cada parte da validação cruzada. As linhas tracejadas indicam a média de cada modelo. Cada parte valida 63 dos 315 casos de treino; os 105 casos de teste ficam excluídos. Fonte: validacao_cruzada_verificada.csv.

### Alteração 68 — inserção de legenda

Secção: Validação cruzada.

**Texto:** Figura 7 — Exactidão em cada parte da validação cruzada. As linhas tracejadas indicam a média de cada modelo. Cada parte valida 63 dos 315 casos de treino; os 105 casos de teste ficam excluídos. Fonte: validacao_cruzada_verificada.csv.

### Alteração 69 — substituição

Secção: Discussão.

**Motivo:** Substituir instruções de redacção por uma discussão apoiada nos resultados.

**Antes:** [Discutir qual dos dois modelos oficiais (Regressão Logística vs. Árvore de Decisão limitada) obteve melhor desempenho, relacionando o resultado com as características teóricas de cada algoritmo descritas no Capítulo 5 — por exemplo, se a fronteira de decisão for aproximadamente linear nos dados reais, espera-se que a Regressão Logística tenha vantagem; se existirem interacções não-lineares fortes entre variáveis (por exemplo, entre disciplinas_em_atraso e regime), a Árvore de Decisão poderá ter vantagem.]

**Depois:** Entre as duas configurações avaliadas, a Regressão Logística apresentou o melhor resultado nas quatro métricas de teste e na exactidão média da validação cruzada. A menor diferença treino/teste e a menor dispersão entre partes sugerem uma generalização mais estável neste conjunto. Esta evidência favorece a Regressão Logística como referência experimental do protótipo; não demonstra que ela seja superior em qualquer população ou que a relação verdadeira entre entradas e decisão seja necessariamente linear.

### Alteração 70 — inserção de texto

Secção: Discussão.

**Texto:** A árvore permite representar interacções por regras sucessivas, mas a sua flexibilidade pode capturar particularidades dos dados. A regularização da Regressão Logística e a fronteira linear constituem hipóteses compatíveis com o resultado observado; não foi realizada uma experiência que isolasse essas causas. Tampouco se pode concluir que toda árvore de decisão tenha pior desempenho: profundidade, tamanho mínimo das folhas e poda não foram optimizados neste trabalho.

### Alteração 71 — inserção de texto

Secção: Discussão.

**Texto:** Para o contexto de apoio académico, a revocação merece atenção: mesmo o melhor modelo omitiu 18 concessões históricas. A interpretação deve, por isso, considerar o custo de cada tipo de erro e o contexto de cada pedido, mantendo avaliação humana. A comparação com necessidade_avaliada continua a ser uma análise futura: a sua exclusão do treino não prova ausência de viés e as métricas globais apresentadas não constituem uma auditoria de equidade.

### Alteração 72 — inserção de texto

Secção: Impacto potencial.

**Texto:** Os benefícios descritos são potenciais. A experiência realizada não mediu tempos de atendimento, produtividade dos serviços, satisfação dos estudantes ou efeitos sobre a distribuição efectiva de apoios. O contributo demonstrado é um protótipo funcional que compara previsões e torna os erros observáveis, com registo cumulativo dos testes individuais.

### Alteração 73 — inserção de texto

Secção: Limitações.

**Texto:** Âmbito da avaliação: a experiência utiliza apenas o conjunto de referência fictício. Não foi disponibilizado nem avaliado um conjunto próprio do problema do grupo; o programa exige essa componente adicional. Consequentemente, o artigo não apresenta resultados de aplicação em dados reais ou de uma avaliação externa independente (Rangel, 2026a; 2026b).

### Alteração 74 — inserção de texto

Secção: Limitações.

**Texto:** Protocolo e histórico: os resultados dependem de uma divisão externa fixa, de dois conjuntos de hiperparâmetros e do rótulo histórico. Não foram realizados testes de significância, calibração das probabilidades ou auditoria por subgrupos. O histórico individual pode conter exemplos escolhidos manualmente e submissões repetidas; as suas métricas são exploratórias e só incluem casos rotulados que não coincidam com o treino.

### Alteração 75 — inserção de texto

Secção: Melhorias futuras.

**Texto:** Completar a avaliação no problema próprio do grupo, documentando a origem e as condições de uso dos dados; experimentar profundidade, poda e tamanho mínimo das folhas por validação dentro do treino; e avaliar os erros por classe e a calibração das probabilidades num conjunto externo. Qualquer escolha posterior de parâmetros deve manter os novos dados de avaliação fora do ajuste.

### Alteração 76 — substituição

Secção: Conclusão.

**Motivo:** Completar a conclusão quantitativa e retirar a alegação de ter medido o efeito de diferentes profundidades.

**Antes:** A componente prática deste trabalho — a construção e comparação de dois classificadores (Regressão Logística e Árvore de Decisão) aplicados à triagem de pedidos de apoio académico — permitiu observar estas limitações teóricas de forma concreta e mensurável, nomeadamente o efeito da profundidade da árvore de decisão sobre o sobreajuste. Permitiu ainda, e talvez mais importante, evidenciar que a qualidade de um modelo supervisionado é indissociável da qualidade e da natureza dos rótulos utilizados no seu treino: um modelo tecnicamente correcto pode, ainda assim, reproduzir e perpetuar enviesamentos presentes nas decisões humanas que lhe serviram de base.

**Depois:** A componente prática comparou dois classificadores nos mesmos 105 pedidos de teste. A Regressão Logística obteve exactidão de 73,33% e F1 de 0,659, superando a Árvore de Decisão com profundidade 5, que atingiu 64,76% e 0,519. A árvore apresentou uma diferença treino/teste de 17,78 pontos percentuais, contra 4,44 na regressão, sugerindo maior sobreajuste nesta configuração. A interface permite testar lotes e casos individuais e acompanhar resultados acumulados. Estas conclusões limitam-se aos dados fictícios de referência e à reprodução de decisões históricas; permanecem por avaliar o problema próprio do grupo e os resultados por subgrupos de necessidade equivalente.

### Alteração 77 — inserção de texto

Secção: Conclusão.

**Texto:** Bigonha (2024): versão consultada disponível em https://homepages.dcc.ufmg.br/~bigonha/Livros/ia-aprendizado.pdf (consulta em 15 de Setembro de 2026).

### Alteração 78 — inserção de texto

Secção: Conclusão.

**Texto:** Rangel, S. A. S. (2026a). Programa de Actividades – Inteligência Artificial. Universidade Pedagógica de Maputo. Material da disciplina: Programa_Actividades_IA_2026-Revisto.pdf.

### Alteração 79 — inserção de texto

Secção: Conclusão.

**Texto:** Rangel, S. A. S. (2026b). Guia de Ficheiros de Referência – Inteligência Artificial. Universidade Pedagógica de Maputo. Material da disciplina: Guia Ficheiros Referencia.pdf.

### Alteração 80 — inserção de texto

Secção: Conclusão.

**Texto:** scikit-learn developers. (2026a). LogisticRegression. Documentação scikit-learn, versão 1.9.1. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html (consulta em 15 de Setembro de 2026).

### Alteração 81 — inserção de texto

Secção: Conclusão.

**Texto:** scikit-learn developers. (2026b). DecisionTreeClassifier. Documentação scikit-learn, versão 1.9.1. https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html (consulta em 15 de Setembro de 2026).

### Alteração 82 — inserção de texto

Secção: Conclusão.

**Texto:** scikit-learn developers. (2026c). StratifiedKFold. Documentação scikit-learn, versão 1.9.1. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html (consulta em 15 de Setembro de 2026).

### Alteração 83 — inserção de texto

Secção: Conclusão.

**Texto:** scikit-learn developers. (2026d). Common pitfalls and recommended practices. Documentação scikit-learn. https://scikit-learn.org/stable/common_pitfalls.html (consulta em 15 de Setembro de 2026).

### Alteração 84 — inserção de texto

Secção: Conclusão.

**Texto:** Streamlit. (2026). Using forms. Documentação Streamlit. https://docs.streamlit.io/develop/concepts/architecture/forms (consulta em 15 de Setembro de 2026).

### Alteração 85 — campo do documento

**Descrição:** Activada a actualização dos campos ao abrir; o índice será actualizado no Word, preservando o campo e os títulos.


## Fecho da revisão e limite da verificação visual

O Word instalado abriu e guardou o DOCX e actualizou o índice, preservando os 39 títulos existentes. A verificação posterior confirmou as sete figuras incorporadas, as cinco tabelas com as dimensões originais, a capa, a folha de rosto e as margens. O texto fora dos campos de índice/bibliografia permaneceu idêntico ao da revisão preparada pelo script.

A tentativa adicional de exportar um PDF completo bloqueou com os métodos ExportAsFixedFormat e SaveAs2. Foram consultadas apenas as instâncias do Word iniciadas para esta tarefa e estas foram encerradas (processos 9472 e 12716); as outras instâncias não foram terminadas. Não foi produzido um PDF completo do artigo. Os PDF individuais dos gráficos estão disponíveis na pasta figuras.

Os gráficos foram inspeccionados directamente como imagens. A paginação final do Word não foi conferida visualmente em PDF; recomenda-se conferir a vista de impressão antes da entrega. Os hashes finais e o resultado dos controlos constam de verificacao_final.json. Nenhum capítulo novo foi acrescentado.

As fontes externas efectivamente consultadas são as entradas de documentação oficial e o PDF de Bigonha indicados na bibliografia. A minuta da declaração de uso de IA permanece separada e necessita de confirmação dos autores. O script de diagnóstico de janelas e o script de paginação foram conservados nesta pasta para documentar as operações realizadas.
