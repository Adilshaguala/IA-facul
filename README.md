# Classificação de pedidos de apoio académico

Comparação de **Regressão Logística** e **Árvore de Decisão** (profundidade máxima 5), com interface Streamlit e gráficos Plotly. O histórico de testes individuais é guardado localmente em SQLite.

## Executar no Windows / PowerShell

Com o ambiente virtual existente:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe classificador_apoio_academico.py
.\venv\Scripts\python.exe -m streamlit run app.py
```

Abra o endereço local mostrado no terminal (normalmente http://localhost:8501).
Para uma instalação nova, crie primeiro o ambiente com `python -m venv venv`. Ambiente validado: Python 3.13.

## Dados e método

- Os documentos exigem registar a divisão, mas não fixam uma percentagem. Usamos **75% treino (315 casos)** e **25% teste (105 casos)**, com divisão aleatória estratificada pelo alvo e semente **42**.
- `dados_referencia.csv` é apenas lido. A execução do treino gera `dados_treino.csv` e `dados_teste.csv`, com as mesmas colunas e valores dos registos seleccionados. Nova execução reproduz e substitui estas partições e os artefactos.
- Os modelos aprendem apenas com os 315 casos de treino. A validação cruzada estratificada de 5 partes também usa apenas esses casos. Cada pipeline tem o seu próprio pré-processador, ajustado dentro de cada treino.
- O alvo é `apoio_concedido`. Excluímos `id` e `necessidade_avaliada`: o primeiro identifica o pedido; a segunda é uma medida independente, mantida no CSV para comparações posteriores, sem entrar no treino. A interface não realiza uma auditoria de equidade.
- Usamos `predict` para a decisão e `predict_proba` para a probabilidade de apoio (classe 1). Os testes não alteram nem voltam a treinar os modelos.
- As decisões históricas não representam necessariamente a decisão mais justa. As métricas medem reprodução dessas decisões.

## Interface

### Treino e resultados

Tabela de métricas, comparação de exactidão no treino, validação cruzada e teste, diferença treino/teste e explicação dos parâmetros.

### Testes em massa

Use o teste reservado ou carregue um CSV UTF-8 separado por vírgulas. Clique **Analisar CSV**. A saída contém uma linha por caso e modelo, decisão prevista, probabilidade, decisão real (quando conhecida) e indicação de acerto.

As entradas obrigatórias são:

```text
curso,ano,regime,media_anterior,disciplinas_em_atraso,horas_trabalho_semanal,distancia_campus_km,tem_computador,acesso_internet_casa,pedidos_anteriores
```

`apoio_concedido` é opcional e aceita 0, 1 ou vazio. `id` e `necessidade_avaliada` também são opcionais na inferência. Categorias de curso novas são aceites e ignoradas pela codificação de categorias desconhecidas. Campos de entrada em falta, vazios ou inválidos são rejeitados.

Disponíveis: filtro de divergências, distribuição das previsões, comparação das probabilidades, exactidão, precisão, revocação, F1 e matrizes de confusão. Os gráficos permitem exportar PNG pelo botão da câmara; tabelas e previsões têm download CSV. Ao mudar o CSV, é necessário analisá-lo novamente.

### Testes individuais

Preencha o formulário e clique **Inferir e guardar**. Cada submissão guarda os dados, as duas previsões, as probabilidades, o resultado real opcional e a data UTC. O histórico é cumulativo e sobrevive a recarregamentos e reinícios da aplicação, no ficheiro `artefactos/historico.sqlite3`.

A análise apresenta o último teste, todos os casos, métricas acumuladas e evolução da exactidão. Sem resultados reais, mostra apenas previsões e comparações; nunca trata previsões como rótulos verdadeiros. Métricas sem denominador são apresentadas como zero.

O histórico é local e comum aos utilizadores desta instalação. Cada nova submissão conta como um teste, mesmo repetindo os dados; um simples recarregamento não acrescenta registos. Os resultados são agrupados pela versão dos modelos, para não misturar treinos diferentes; os registos de versões anteriores permanecem na base de dados.

Casos que coincidam com o treino (pelo identificador ou pelas entradas) são assinalados e excluídos das métricas de teste, nas duas modalidades. A análise de exemplos introduzidos manualmente é exploratória e não substitui a avaliação nos 105 casos reservados.

## Organização do código

| Ficheiro | Responsabilidade |
| --- | --- |
| `dados.py` | Esquema, validação e divisão dos dados |
| `modelos.py` | Definição dos algoritmos e pipelines |
| `treino.py` | Treino, validação cruzada e gravação dos modelos |
| `avaliacao.py` | Inferência, métricas e evolução acumulada |
| `historico.py` | Persistência dos testes individuais |
| `app.py` | Formulários, tabelas e gráficos |
| `classificador_apoio_academico.py` | Comando para preparar e treinar |

Artefactos gerados: `resultados_grupo9.csv`, `comparacao_modelos.png`, `artefactos/modelos.joblib`, `artefactos/treino.json`, `artefactos/previsoes_teste.csv` e `artefactos/matrizes_confusao.json`. O JSON do treino regista os identificadores das partições, semente, versão e hash do CSV original.

## Verificação

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes usam pastas temporárias para não adicionar exemplos ao histórico de utilização.

## Enquadramento académico

O conjunto de referência é uma parte do trabalho: os documentos também exigem resultados do problema próprio do grupo. O artigo e os slides devem justificar o método, discutir os resultados e declarar o uso de ferramentas de IA.
