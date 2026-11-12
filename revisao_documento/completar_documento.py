"""Completa o artigo existente, preservando os seus títulos e registando as alterações."""

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import shutil
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.table import Table
from docx.text.paragraph import Paragraph
from lxml import etree
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import plot_tree

from avaliacao import METRICAS, calcular_metricas, inferir, matrizes_confusao
from dados import ALVO, ENTRADAS, SEMENTE, ler_csv
from modelos import criar_modelos

PASTA = BASE / "revisao_documento"
FIGURAS = PASTA / "figuras"
ORIGINAL = BASE / "IA trabalho 11.docx"
BACKUP = PASTA / "IA trabalho 11 - original.docx"
FIGURAS.mkdir(parents=True, exist_ok=True)
if not BACKUP.exists():
    shutil.copy2(ORIGINAL, BACKUP)

ficheiros_protegidos = ["dados_referencia.csv", "dados_treino.csv", "dados_teste.csv",
                        "modelos.py", "treino.py", "avaliacao.py", "app.py",
                        "artefactos/modelos.joblib", "resultados_grupo9.csv"]
hashes = {f: sha256((BASE / f).read_bytes()).hexdigest() for f in ficheiros_protegidos}
treino = ler_csv(BASE / "dados_treino.csv", exigir_alvo=True)
teste = ler_csv(BASE / "dados_teste.csv", exigir_alvo=True)
pacote = joblib.load(BASE / "artefactos/modelos.joblib")
assert not set(treino.id) & set(teste.id)
assert (len(treino), len(teste)) == (315, 105)
assert pacote["referencia_sha256"] == hashes["dados_referencia.csv"]
previsoes = inferir(pacote, teste)
metricas = calcular_metricas(previsoes)
resultados = pd.read_csv(BASE / "resultados_grupo9.csv")
np.testing.assert_allclose(metricas[METRICAS], resultados[METRICAS])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
scores_cv = {}
for nome, modelo in criar_modelos().items():
    scores = cross_val_score(modelo, treino[ENTRADAS], treino[ALVO], cv=cv, scoring="accuracy")
    modelo.fit(treino[ENTRADAS], treino[ALVO])
    np.testing.assert_array_equal(modelo.predict(teste[ENTRADAS]), pacote["modelos"][nome].predict(teste[ENTRADAS]))
    row = resultados[resultados.Modelo == nome].iloc[0]
    np.testing.assert_allclose([scores.mean(), scores.std()], [row["CV exactidão (média)"], row["CV exactidão (desvio padrão)"]])
    scores_cv[nome] = scores
pd.DataFrame(scores_cv, index=range(1, 6)).rename_axis("Parte").to_csv(PASTA / "validacao_cruzada_verificada.csv")
metricas.to_csv(PASTA / "metricas_verificadas.csv", index=False)
matrizes = matrizes_confusao(previsoes)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titleweight": "bold", "savefig.facecolor": "white"})
CORES = ["#137C8B", "#CE7524"]
ficheiros_figuras = []


def guardar_figura(nome):
    plt.savefig(FIGURAS / f"{nome}.png", dpi=300, bbox_inches="tight")
    plt.savefig(FIGURAS / f"{nome}.pdf", bbox_inches="tight")
    plt.close()
    ficheiros_figuras.append(nome)


# Ilustração conceptual, explicitamente distinta dos resultados do modelo ajustado.
fig, ax = plt.subplots(figsize=(8, 3.5))
z = np.linspace(-6, 6, 301)
ax.plot(z, 1 / (1 + np.exp(-z)), color=CORES[0], linewidth=2.7)
ax.axhline(0.5, color="#777777", linestyle="--", linewidth=1)
ax.axvline(0, color="#777777", linestyle="--", linewidth=1)
ax.scatter([0], [0.5], color=CORES[1], s=45, zorder=4)
ax.set(xlabel="Pontuação linear z = w·x + b", ylabel="Probabilidade σ(z)", ylim=(-0.03, 1.03))
ax.text(-5.7, 0.77, "Classe 0\npara z ≤ 0", fontsize=12)
ax.text(2.6, 0.21, "Classe 1\npara z > 0", fontsize=12)
ax.grid(alpha=0.16)
fig.tight_layout()
guardar_figura("01_sigmoide")

modelo_arvore = pacote["modelos"]["Árvore de Decisão"]
nomes_atributos = [n.replace("num__", "").replace("cat__", "")
                  for n in modelo_arvore["prep"].get_feature_names_out()]
fig, ax = plt.subplots(figsize=(11, 5.1))
plot_tree(modelo_arvore["clf"], max_depth=1, feature_names=nomes_atributos,
          class_names=["Não concedido", "Concedido"], filled=True, rounded=True,
          proportion=False, impurity=True, precision=2, fontsize=12, ax=ax)
fig.tight_layout()
guardar_figura("02_arvore_excerto")

fig, ax = plt.subplots(figsize=(9, 4))
ax.set(xlim=(0, 10), ylim=(0, 5))
ax.axis("off")


def caixa(x, y, w, h, texto, cor):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", facecolor=cor,
                                edgecolor="#526773", linewidth=1.1))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=12)


caixa(3.4, 3.8, 3.2, 0.85, "420 pedidos de referência\nCSV original preservado", "#F0F3F4")
caixa(0.1, 2.1, 4.4, 1.1, "315 casos de treino (75%)\nValidação cruzada: 5 partes\n252 treino / 63 validação por parte", "#E1F1F2")
caixa(5.6, 2.1, 4.3, 1.1, "105 casos de teste (25%)\nReservados para a avaliação\nNão usados no ajuste", "#FFF0DF")
caixa(0.4, 0.25, 3.8, 1.1, "Ajuste final nos 315 casos\nRegressão Logística\nÁrvore de Decisão", "#E1F1F2")
caixa(5.8, 0.25, 3.9, 1.1, "Previsões nos mesmos 105 casos\nMétricas e matrizes de confusão\nComparação entre modelos", "#F0F3F4")
for ponto_a, ponto_b in [((4, 3.8), (2.3, 3.25)), ((6, 3.8), (7.7, 3.25)),
                          ((2.3, 2.05), (2.3, 1.4)), ((7.7, 2.05), (7.7, 1.4)),
                          ((4.3, 0.8), (5.7, 0.8))]:
    ax.annotate("", xy=ponto_b, xytext=ponto_a, arrowprops={"arrowstyle": "->", "lw": 1.7, "color": "#526773"})
fig.tight_layout()
guardar_figura("03_protocolo_experimental")

fig, ax = plt.subplots(figsize=(8, 4.1))
x = np.arange(4)
for i, (_, row) in enumerate(resultados.iterrows()):
    barras = ax.bar(x + (i - 0.5) * 0.35, row[METRICAS].to_numpy(dtype=float) * 100,
                    width=0.35, color=CORES[i], label=row.Modelo)
    ax.bar_label(barras, labels=[f"{v:.1f}".replace(".", ",") for v in row[METRICAS].to_numpy(dtype=float) * 100], padding=3, fontsize=11)
ax.set(xticks=x, xticklabels=METRICAS, ylim=(0, 100), ylabel="Valor (%)")
ax.legend(loc="upper right", frameon=False)
ax.grid(axis="y", alpha=0.15)
ax.set_axisbelow(True)
fig.tight_layout()
guardar_figura("04_metricas_teste")

fig, eixos = plt.subplots(1, 2, figsize=(9, 4.2), layout="constrained")
for ax, (nome, matriz) in zip(eixos, matrizes.items()):
    ax.imshow(matriz, cmap="Blues", vmin=0, vmax=60)
    ax.set(title=nome, xticks=[0, 1], yticks=[0, 1], xticklabels=["0", "1"], yticklabels=["0", "1"],
           xlabel="Classe prevista", ylabel="Classe real")
    for (i, j), n in np.ndenumerate(matriz):
        ax.text(j, i, f"{n}", ha="center", va="center", fontsize=21,
                color="white" if n >= 35 else "#172B35")
fig.supxlabel("0 = não concedido | 1 = concedido · 105 casos em cada matriz", fontsize=12)
guardar_figura("05_matrizes_confusao")

fig, ax = plt.subplots(figsize=(8, 4.1))
x = np.arange(2)
for i, (_, row) in enumerate(resultados.iterrows()):
    valores = np.array([row["Exactidão (treino)"], row["Exactidão"]]) * 100
    barras = ax.bar(x + (i - 0.5) * 0.34, valores, width=0.34, color=CORES[i], label=row.Modelo)
    ax.bar_label(barras, labels=[f"{v:.2f}".replace(".", ",") for v in valores], padding=3, fontsize=11)
ax.set(xticks=x, xticklabels=["Treino (315 casos)", "Teste (105 casos)"], ylim=(0, 104), ylabel="Exactidão (%)")
ax.legend(loc="upper right", frameon=False)
ax.grid(axis="y", alpha=0.15)
ax.set_axisbelow(True)
fig.tight_layout()
guardar_figura("06_treino_teste")

fig, ax = plt.subplots(figsize=(8, 4.1))
for i, (nome, scores) in enumerate(scores_cv.items()):
    ax.plot(range(1, 6), scores * 100, "o-", color=CORES[i], label=nome, linewidth=2.0, markersize=7)
    ax.axhline(scores.mean() * 100, color=CORES[i], linestyle="--", alpha=0.7)
ax.set(xlabel="Parte de validação cruzada", ylabel="Exactidão (%)", xticks=range(1, 6), ylim=(0, 100))
ax.legend(loc="lower left", frameon=False)
ax.grid(alpha=0.15)
fig.tight_layout()
guardar_figura("07_validacao_cruzada")

doc = Document(BACKUP)
body = list(doc.element.body)
alteracoes = []


def texto(elemento):
    return "".join(elemento.itertext()) if False else "".join(t.text or "" for t in elemento.iter(qn("w:t")))


def titulos(documento):
    return [(p.find(qn("w:pPr")).find(qn("w:pStyle")).get(qn("w:val")), texto(p))
            for p in documento.element.body.iter(qn("w:p"))
            if p.find(qn("w:pPr")) is not None
            and p.find(qn("w:pPr")).find(qn("w:pStyle")) is not None
            and p.find(qn("w:pPr")).find(qn("w:pStyle")).get(qn("w:val")).startswith("Heading")]


titulos_originais = titulos(doc)
seccoes_originais = [etree.tostring(e) for e in doc.element.body.iter(qn("w:sectPr"))]
tabelas_originais = [(len(t.rows), len(t.columns)) for t in doc.tables]


def seccao(indice):
    for i in range(indice, -1, -1):
        ppr = body[i].find(qn("w:pPr"))
        if ppr is not None and ppr.find(qn("w:pStyle")) is not None:
            if ppr.find(qn("w:pStyle")).get(qn("w:val")).startswith("Heading") and texto(body[i]):
                return texto(body[i])
    return "Elementos pré-textuais"


def substituir(indice, novo, motivo):
    p = Paragraph(body[indice], doc._body)
    anterior = p.text
    rpr = deepcopy(p.runs[0]._r.rPr) if p.runs and p.runs[0]._r.rPr is not None else None
    p.clear()
    run = p.add_run(novo)
    if rpr is not None:
        run._r.insert(0, rpr)
    alteracoes.append({"tipo": "substituição", "bloco_original": indice, "secção": seccao(indice),
                       "motivo": motivo, "antes": anterior, "depois": novo})
    return p


def acrescentar(ancora, texto_novo, indice, legenda=False):
    elemento = OxmlElement("w:p")
    ancora.addnext(elemento)
    p = Paragraph(elemento, doc._body)
    p.add_run(texto_novo)
    p.paragraph_format.space_after = Pt(6)
    if legenda:
        p.paragraph_format.line_spacing = 1
        p.paragraph_format.keep_together = True
        for run in p.runs:
            run.font.size = Pt(10)
            run.italic = True
    alteracoes.append({"tipo": "inserção de legenda" if legenda else "inserção de texto",
                       "após_bloco_original": indice, "secção": seccao(indice), "texto": texto_novo})
    return elemento


def figura(ancora, nome, legenda, indice):
    elemento = OxmlElement("w:p")
    ancora.addnext(elemento)
    p = Paragraph(elemento, doc._body)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    desenho = p.add_run().add_picture(str(FIGURAS / f"{nome}.png"), width=Cm(14.7))
    desenho._inline.docPr.set("descr", legenda)
    alteracoes.append({"tipo": "inserção de figura", "após_bloco_original": indice,
                       "secção": seccao(indice), "ficheiro": f"figuras/{nome}.png", "legenda": legenda})
    return acrescentar(elemento, legenda, indice, legenda=True)


substituir(6,
    "Este trabalho aborda os fundamentos do Aprendizado Supervisionado, articulando a inferência dedutiva e indutiva com a construção de um classificador de pedidos de apoio académico. Comparam-se Regressão Logística e Árvore de Decisão com profundidade máxima de 5, sobre 420 pedidos fictícios do conjunto de referência da turma. A divisão estratificada reservou 315 casos para treino e 105 para teste, com semente 42; a validação cruzada de 5 partes foi realizada exclusivamente no treino. No teste, a Regressão Logística obteve 73,33% de exactidão e F1 de 0,659, enquanto a Árvore de Decisão atingiu 64,76% e 0,519, respectivamente. O protótipo inclui interface gráfica para testes em massa e individuais, com histórico persistente. A discussão considera a diferença treino/teste, os erros por classe e a limitação de aprender decisões históricas, que não constituem um critério independente de necessidade ou justiça.",
    "Incluir método actual e resultados efectivamente verificados no resumo.")
substituir(12,
    "O trabalho apresenta inicialmente a Introdução e os conceitos de Inteligência Artificial. Seguem-se os tipos de inferência e o Aprendizado de Máquina, a fundamentação dos algoritmos escolhidos, a descrição do problema e do artefacto, a implementação e os resultados. As secções finais discutem o desempenho, o impacto potencial, as limitações, as melhorias futuras e as conclusões, seguindo-se a bibliografia.",
    "Actualizar o roteiro, que omitia capítulos existentes e usava numeração desactualizada.")
substituir(93,
    "Para além do enquadramento geral apresentado no capítulo anterior, importa aprofundar os dois algoritmos seleccionados para este artefacto: a Regressão Logística e a Árvore de Decisão. Entre os métodos referidos em «Metodologia: Algoritmos e Abordagens», estes dois possuem mecanismos de decisão distintos — um linear e probabilístico, o outro hierárquico e baseado em regras —, permitindo comparar duas abordagens sem acrescentar a complexidade de redes neurais ou conjuntos de modelos.",
    "Substituir a remissão numérica desactualizada pelo título da secção existente.")
substituir(105,
    "A escala das características influencia a optimização e a regularização; por isso, as entradas numéricas foram normalizadas durante o treino, conforme descrito em «Metodologia de Construção do Artefacto».",
    "Ligar a explicação à secção correcta e clarificar o papel da escala.")
substituir(127,
    "O artefacto destina-se a apoiar a análise humana dos pedidos. As implicações e os limites deste uso são retomados nas secções «Discussão» e «Limitações».",
    "Corrigir a remissão antiga para o Capítulo 9.")
substituir(136,
    "A construção do artefacto seguiu o enquadramento apresentado em «Protocolo Experimental», com as seguintes especificações concretas:",
    "Substituir a remissão antiga para 4.2.4 pelo título da secção preservada.")
substituir(182,
    "A aprendizagem supervisionada generaliza a partir de exemplos rotulados e de pressupostos sobre a relação entre entradas e saídas. O algoritmo ajusta uma função para produzir previsões em novas entradas; estas continuam sujeitas a incerteza e às limitações discutidas em «Desafios e Limitações», incluindo sobreajuste, subajuste, desequilíbrio de classes e qualidade dos rótulos.",
    "Corrigir a remissão antiga para o Capítulo 4 e formular a conclusão sem equiparar formalmente o treino a um silogismo.")
substituir(35,
    "Na dedução, a conclusão decorre das regras de inferência aplicadas às premissas. Com isto, a garantia de verdade exige simultaneamente um argumento válido e premissas verdadeiras; a validade da forma lógica, por si só, não demonstra que as premissas descrevem correctamente a realidade.",
    "Completar a frase interrompida em «Com isto».")
substituir(80,
    "Optimização de hiperparâmetros — pode recorrer a validação cruzada dentro do conjunto de treino, mantendo o teste isolado para a avaliação final. Neste trabalho, comparam-se configurações fixas; não foi realizada uma pesquisa de hiperparâmetros (scikit-learn developers, 2026c).",
    "Clarificar o protocolo de validação e distinguir possibilidades teóricas do procedimento executado.")
ancora = acrescentar(body[101],
    "Na configuração usada, o optimizador é L-BFGS, max_iter=1000 e C=1,0, com regularização L2 por omissão. Assim, a implementação acrescenta uma penalização dos coeficientes à perda apresentada, procurando limitar soluções excessivamente ajustadas ao treino (scikit-learn developers, 2026a). A Figura 1 ilustra a função sigmoide; não representa uma curva ajustada a uma única variável do conjunto de dados.", 101)
figura(ancora, "01_sigmoide", "Figura 1 — Função sigmoide e limiar de decisão. Ilustração matemática produzida para este trabalho, a partir de σ(z)=1/(1+e⁻ᶻ).", 101)
substituir(115,
    "A profundidade limita o número de decisões sucessivas e ajuda a controlar a complexidade da árvore. Neste trabalho utiliza-se apenas max_depth=5, com critério de Gini e semente 42; o sobreajuste é analisado comparando o desempenho no treino, na validação cruzada e no teste. Não foi realizada uma experiência com árvore sem limite de profundidade (scikit-learn developers, 2026b).",
    "Retirar a experiência com um terceiro modelo que não faz parte da implementação actual.")
figura(body[119], "02_arvore_excerto",
       "Figura 2 — Raiz e primeiro nível da Árvore de Decisão treinada. Os nós assinalados com reticências continuam até à profundidade máxima de 5. Os limiares numéricos usam a escala normalizada; values segue a ordem [0, 1]. Fonte: modelo guardado em artefactos/modelos.joblib.", 119)
ancora = acrescentar(body[134],
    "Como enquadramento PEAS, a medida de desempenho é dada pelas métricas de classificação e pelos erros por classe; o ambiente corresponde aos pedidos e ao processo de análise dos serviços académicos; os actuadores são as previsões, probabilidades e relatórios apresentados; e os sensores são as colunas recebidas por CSV ou formulário. O classificador aplica uma função aprendida a cada perfil, sem executar uma pesquisa de caminhos ou alterar automaticamente a situação administrativa do estudante. O histórico da interface serve à análise, sem actualizar os parâmetros dos modelos.", 134)
substituir(138,
    "Pré-processamento: StandardScaler para as sete entradas numéricas e OneHotEncoder para curso, ano e regime. Cada algoritmo possui um ColumnTransformer e um Pipeline independentes. A preparação é ajustada apenas nos dados usados no respectivo treino, incluindo cada parte da validação cruzada, para evitar fuga de informação (scikit-learn developers, 2026d).",
    "Descrever os pipelines independentes e o isolamento do pré-processamento.")
substituir(139,
    "Divisão treino/teste: 75% para treino (315 pedidos) e 25% para teste (105 pedidos), seleccionados aleatoriamente com estratificação por apoio_concedido e random_state=42. O treino contém 179 casos da classe 0 e 136 da classe 1; o teste contém 60 e 45, respectivamente. O ficheiro de referência é preservado; as partições são guardadas em dados_treino.csv e dados_teste.csv. Os documentos da disciplina não fixam uma percentagem de teste, exigindo que esta seja reportada (Rangel, 2026b).",
    "Actualizar 80/20 para a divisão 75/25 autorizada e executada.")
substituir(140,
    "Validação cruzada: StratifiedKFold com n_splits=5, shuffle=True e random_state=42, aplicado apenas aos 315 casos de treino. Em cada parte, 252 casos são usados no ajuste e 63 na validação; nenhum dos 105 casos de teste participa neste processo. Reportam-se média e desvio-padrão da exactidão entre as cinco partes.",
    "Corrigir a afirmação de validação sobre a totalidade dos dados.")
substituir(141,
    "Modelos treinados: Regressão Logística (max_iter=1000) e Árvore de Decisão (max_depth=5), ambos com random_state=42 e restantes parâmetros por omissão. Não foram usados pesos de classe, reamostragem, procura automática de hiperparâmetros ou ajuste do limiar com os dados de teste.",
    "Registar exactamente os dois modelos e o âmbito da experiência.")
figura(body[142], "03_protocolo_experimental",
       "Figura 3 — Protocolo experimental. A divisão externa usa semente 42 e estratificação; a validação cruzada ocorre dentro do treino. Fonte: dados.py e treino.py.", 142)
substituir(145,
    "A implementação foi realizada em Python 3.13, utilizando pandas e NumPy para os dados, scikit-learn para modelos e métricas, Matplotlib para gráficos exportados, Streamlit e Plotly para a interface, joblib para guardar os modelos e SQLite para o histórico. A lógica principal organiza-se nas sete etapas seguintes, distribuídas por módulos especializados:",
    "Actualizar a descrição para a aplicação modular com interface e persistência.")
substituir(146, "1. Leitura e validação de dados_referencia.csv em dados.py, verificando o esquema, os tipos, os valores permitidos e os identificadores; definição da semente 42.", "Actualizar a etapa de carregamento.")
substituir(147, "2. Definição, em modelos.py, dos dois algoritmos e dos respectivos pré-processadores. Definir um Pipeline não o ajusta aos dados: esse ajuste ocorre apenas durante fit.", "Distinguir definição e ajuste para evitar uma descrição ambígua de fuga de informação.")
substituir(148, "3. Divisão estratificada 75/25, sem sobreposição de identificadores, e gravação dos 315 casos de treino e 105 casos de teste nos ficheiros correspondentes.", "Actualizar a divisão usada.")
substituir(149, "4. Validação cruzada de 5 partes exclusivamente nos dados de treino, através de cross_val_score e StratifiedKFold. O scikit-learn ajusta uma cópia independente de todo o Pipeline em cada parte.", "Alinhar a sequência com treino.py.")
substituir(150, "5. Ajuste final de cada Pipeline aos 315 casos de treino e previsão sobre treino e teste, mantendo os 105 casos de teste fora do ajuste dos parâmetros.", "Explicitar o treino final e a avaliação externa.")
substituir(151, "6. Cálculo de exactidão, precisão, revocação, F1 e matrizes de confusão em avaliacao.py, e comparação da exactidão de treino com a de teste. A interface assinala uma diferença superior a 0,10 como indício a discutir, sem a tratar como prova estatística de sobreajuste.", "Actualizar a avaliação e qualificar a interpretação da diferença treino/teste.")
substituir(152, "7. Exportação dos resultados, gráficos, metadados e modelos. A interface app.py carrega os modelos ajustados para inferência em CSV ou formulário; os testes individuais são guardados por historico.py, sem voltar a treinar os classificadores.", "Descrever os artefactos e a interface actual.")
p = substituir(154,
    "from modelos import criar_modelos\nfrom dados import ENTRADAS, ALVO, SEMENTE\nfrom sklearn.model_selection import StratifiedKFold, cross_val_score\n\nmodelos = criar_modelos()\ncv = StratifiedKFold(n_splits=5, shuffle=True,\n                    random_state=SEMENTE)\nfor nome, modelo in modelos.items():\n    scores = cross_val_score(\n        modelo, treino[ENTRADAS], treino[ALVO],\n        cv=cv, scoring=\"accuracy\")\n    modelo.fit(treino[ENTRADAS], treino[ALVO])\n    previsoes = modelo.predict(teste[ENTRADAS])",
    "Substituir o excerto antigo de três modelos pelo fluxo actual; treino e teste são as partições já carregadas.")
p.paragraph_format.line_spacing = 1
p.paragraph_format.keep_together = True
for r in p.runs:
    r.font.name = "Consolas"
    r.font.size = Pt(9)
substituir(155,
    "O ficheiro classificador_apoio_academico.py é a entrada de linha de comandos. O código completo distribui-se por dados.py (esquema e divisão), modelos.py (algoritmos), treino.py (ajuste e exportação), avaliacao.py (inferência e métricas), historico.py (persistência) e app.py (interface). As versões das dependências constam de requirements.txt, e as instruções de execução constam do README.md.",
    "Corrigir a indicação de que todo o código permanece num único ficheiro.")
ancora = acrescentar(body[155],
    "Na área de testes em massa, o utilizador carrega um CSV e recebe, para cada pedido, as previsões dos dois algoritmos, a probabilidade da classe 1, o resultado real quando disponível e a indicação de acerto. A análise inclui divergências, distribuição das previsões, comparação das probabilidades, métricas, matrizes de confusão e exportação CSV. A área individual apresenta um formulário; cada submissão acrescenta os resultados ao histórico SQLite e actualiza a análise acumulada. O formulário envia os valores em conjunto após a submissão (Streamlit, 2026).", 155)
ancora = acrescentar(ancora,
    "As métricas do histórico utilizam apenas casos com resultado real conhecido e excluem entradas coincidentes com o treino. Os registos são separados por versão dos modelos, permanecem disponíveis após reiniciar a interface e não são duplicados por um simples recarregamento. Uma nova submissão, mesmo repetida, conta como um novo teste; a análise manual é exploratória e não substitui o teste reservado.", 155)
acrescentar(ancora,
    "A verificação automatizada executou 11 testes com sucesso, cobrindo a separação e reprodutibilidade dos dados, o isolamento do pré-processamento e da validação, a igualdade entre inferência individual e em massa, a validação de CSV, casos sem rótulo, métricas conhecidas, persistência e fluxos da interface. Os testes de interface usaram o AppTest do Streamlit e bases temporárias; não constituem uma avaliação de usabilidade com estudantes.", 155)
substituir(157,
    "Os resultados apresentados nesta secção foram recalculados a partir dos dados e modelos do projecto, verificando a concordância com resultados_grupo9.csv. A comparação utiliza exactamente os mesmos 105 pedidos reservados para teste, sem introduzir valores ilustrativos. Os dados de referência são fictícios; a classe 1 representa a decisão histórica de conceder apoio.",
    "Substituir o aviso de preenchimento por uma descrição verificável da experiência.")
substituir(159,
    "A tabela seguinte apresenta o desempenho no conjunto de teste (25% dos 420 pedidos), com semente 42. A terceira linha fornece uma referência simples: prever sempre a classe 0, maioritária no treino. Esta regra não é um terceiro modelo treinado; permite avaliar se os dois classificadores superam uma previsão constante. Precisão, revocação e F1 referem-se à classe positiva 1.",
    "Introduzir os resultados reais e preservar as dimensões da tabela, substituindo a linha obsoleta por uma referência constante explícita.")
tabela = Table(body[160], doc._body)
valores = [
    ["dados_referencia", "Regressão Logística", "73,33%", "72,97%", "60,00%", "0,659"],
    ["dados_referencia", "Árvore de Decisão\n(max_depth=5)", "64,76%", "62,50%", "44,44%", "0,519"],
    ["dados_referencia", "Referência: sempre 0\n(sem treino)", "57,14%", "0,00%", "0,00%", "0,000"],
]
for row, novos in zip(tabela.rows[1:], valores):
    for celula, novo in zip(row.cells, novos):
        antes = celula.text
        p = celula.paragraphs[0]
        p.clear()
        p.add_run(novo)
        p.paragraph_format.line_spacing = 1
        p.paragraph_format.space_after = Pt(3)
        for run in p.runs:
            run.font.size = Pt(10)
        alteracoes.append({"tipo": "célula da tabela de resultados", "bloco_original": 160, "antes": antes, "depois": novo})
ancora = acrescentar(body[160],
    "Fonte: dados_referencia.csv; conjunto: teste; divisão treino/teste: 75%/25%; n=105; semente: 42. Na referência constante, a precisão é definida como zero por não haver previsões positivas, seguindo zero_division=0.", 160, legenda=True)
ancora = figura(ancora, "04_metricas_teste", "Figura 4 — Métricas dos dois classificadores no teste reservado. Os valores do gráfico são percentagens; na tabela, F1 é apresentado na escala de 0 a 1. Fonte: métricas recalculadas do projecto.", 160)
ancora = acrescentar(ancora,
    "A Regressão Logística classificou correctamente 77 dos 105 pedidos, contra 68 da Árvore de Decisão. A diferença de exactidão foi de 8,57 pontos percentuais; as diferenças de precisão, revocação e F1 foram de 10,47, 15,56 e 13,91 pontos percentuais, respectivamente, em favor da Regressão Logística. A referência constante acertou 60 pedidos (57,14%), mas não identificou nenhum dos 45 apoios concedidos.", 160)
ancora = figura(ancora, "05_matrizes_confusao", "Figura 5 — Matrizes de confusão com contagens absolutas. Linhas: classe real; colunas: classe prevista; ordem [0, 1]. Fonte: inferência dos modelos nos 105 pedidos de teste.", 160)
acrescentar(ancora,
    "Na Regressão Logística, a matriz contém 50 verdadeiros negativos, 10 falsos positivos, 18 falsos negativos e 27 verdadeiros positivos. Na Árvore de Decisão, as contagens são 48, 12, 25 e 20, respectivamente. Assim, a árvore falhou 25 dos 45 casos historicamente concedidos (55,56%), enquanto a regressão falhou 18 (40,00%). Um falso negativo significa discordância com uma concessão histórica, não demonstra, isoladamente, uma decisão injusta. Por exemplo, na regressão: precisão=27/(27+10)=72,97%; revocação=27/(27+18)=60,00%; F1=54/(54+10+18)=0,659.", 160)
substituir(163,
    "A Regressão Logística apresentou exactidão de 77,78% no treino e 73,33% no teste, com uma diferença de 4,44 pontos percentuais. Na Árvore de Decisão, a exactidão passou de 82,54% para 64,76%, uma diferença de 17,78 pontos percentuais. A árvore ajustou melhor os casos de treino, mas apresentou pior desempenho em dados não usados no ajuste. O padrão sugere maior sobreajuste nesta configuração, mesmo com max_depth=5; uma divisão única não permite provar a sua causa. Como não foram comparadas outras profundidades, estes resultados não medem o efeito causal de alterar max_depth.",
    "Preencher a análise de sobreajuste com resultados reais dos dois modelos.")
figura(body[163], "06_treino_teste", "Figura 6 — Exactidão no treino e no teste. Diferenças: 4,44 pontos percentuais na Regressão Logística e 17,78 na Árvore de Decisão. Fonte: resultados_grupo9.csv, verificado por nova inferência.", 163)
substituir(165,
    "Na validação cruzada de 5 partes dentro do treino, a Regressão Logística atingiu exactidão média de 75,24%, com desvio-padrão de 2,15 pontos percentuais. A Árvore de Decisão obteve 67,62%, com desvio-padrão de 4,56 pontos percentuais. A Regressão Logística teve maior média e menor dispersão entre as partes, coerentemente com o teste reservado. Estes desvios-padrão descrevem a variação entre cinco partes com treinos sobrepostos; não são intervalos de confiança nem demonstram significância estatística da diferença (scikit-learn developers, 2026c).",
    "Preencher a média, dispersão e interpretação da validação cruzada.")
figura(body[165], "07_validacao_cruzada", "Figura 7 — Exactidão em cada parte da validação cruzada. As linhas tracejadas indicam a média de cada modelo. Cada parte valida 63 dos 315 casos de treino; os 105 casos de teste ficam excluídos. Fonte: validacao_cruzada_verificada.csv.", 165)
substituir(167,
    "Entre as duas configurações avaliadas, a Regressão Logística apresentou o melhor resultado nas quatro métricas de teste e na exactidão média da validação cruzada. A menor diferença treino/teste e a menor dispersão entre partes sugerem uma generalização mais estável neste conjunto. Esta evidência favorece a Regressão Logística como referência experimental do protótipo; não demonstra que ela seja superior em qualquer população ou que a relação verdadeira entre entradas e decisão seja necessariamente linear.",
    "Substituir instruções de redacção por uma discussão apoiada nos resultados.")
ancora = acrescentar(body[167],
    "A árvore permite representar interacções por regras sucessivas, mas a sua flexibilidade pode capturar particularidades dos dados. A regularização da Regressão Logística e a fronteira linear constituem hipóteses compatíveis com o resultado observado; não foi realizada uma experiência que isolasse essas causas. Tampouco se pode concluir que toda árvore de decisão tenha pior desempenho: profundidade, tamanho mínimo das folhas e poda não foram optimizados neste trabalho.", 167)
acrescentar(ancora,
    "Para o contexto de apoio académico, a revocação merece atenção: mesmo o melhor modelo omitiu 18 concessões históricas. A interpretação deve, por isso, considerar o custo de cada tipo de erro e o contexto de cada pedido, mantendo avaliação humana. A comparação com necessidade_avaliada continua a ser uma análise futura: a sua exclusão do treino não prova ausência de viés e as métricas globais apresentadas não constituem uma auditoria de equidade.", 167)
acrescentar(body[169],
    "Os benefícios descritos são potenciais. A experiência realizada não mediu tempos de atendimento, produtividade dos serviços, satisfação dos estudantes ou efeitos sobre a distribuição efectiva de apoios. O contributo demonstrado é um protótipo funcional que compara previsões e torna os erros observáveis, com registo cumulativo dos testes individuais.", 169)
ancora = acrescentar(body[174],
    "Âmbito da avaliação: a experiência utiliza apenas o conjunto de referência fictício. Não foi disponibilizado nem avaliado um conjunto próprio do problema do grupo; o programa exige essa componente adicional. Consequentemente, o artigo não apresenta resultados de aplicação em dados reais ou de uma avaliação externa independente (Rangel, 2026a; 2026b).", 174)
acrescentar(ancora,
    "Protocolo e histórico: os resultados dependem de uma divisão externa fixa, de dois conjuntos de hiperparâmetros e do rótulo histórico. Não foram realizados testes de significância, calibração das probabilidades ou auditoria por subgrupos. O histórico individual pode conter exemplos escolhidos manualmente e submissões repetidas; as suas métricas são exploratórias e só incluem casos rotulados que não coincidam com o treino.", 174)
acrescentar(body[179],
    "Completar a avaliação no problema próprio do grupo, documentando a origem e as condições de uso dos dados; experimentar profundidade, poda e tamanho mínimo das folhas por validação dentro do treino; e avaliar os erros por classe e a calibração das probabilidades num conjunto externo. Qualquer escolha posterior de parâmetros deve manter os novos dados de avaliação fora do ajuste.", 179)
substituir(183,
    "A componente prática comparou dois classificadores nos mesmos 105 pedidos de teste. A Regressão Logística obteve exactidão de 73,33% e F1 de 0,659, superando a Árvore de Decisão com profundidade 5, que atingiu 64,76% e 0,519. A árvore apresentou uma diferença treino/teste de 17,78 pontos percentuais, contra 4,44 na regressão, sugerindo maior sobreajuste nesta configuração. A interface permite testar lotes e casos individuais e acompanhar resultados acumulados. Estas conclusões limitam-se aos dados fictícios de referência e à reprodução de decisões históricas; permanecem por avaliar o problema próprio do grupo e os resultados por subgrupos de necessidade equivalente.",
    "Completar a conclusão quantitativa e retirar a alegação de ter medido o efeito de diferentes profundidades.")

# Mantém integralmente a capa e os nomes. O título divergente da folha de rosto é
# identificado no relatório para revisão dos autores, sem alterar os elementos pré-textuais.
biblio = body[187]
ancora = acrescentar(biblio,
    "Bigonha (2024): versão consultada disponível em https://homepages.dcc.ufmg.br/~bigonha/Livros/ia-aprendizado.pdf (consulta em 15 de Setembro de 2026).", 187)
referencias = [
    "Rangel, S. A. S. (2026a). Programa de Actividades – Inteligência Artificial. Universidade Pedagógica de Maputo. Material da disciplina: Programa_Actividades_IA_2026-Revisto.pdf.",
    "Rangel, S. A. S. (2026b). Guia de Ficheiros de Referência – Inteligência Artificial. Universidade Pedagógica de Maputo. Material da disciplina: Guia Ficheiros Referencia.pdf.",
    "scikit-learn developers. (2026a). LogisticRegression. Documentação scikit-learn, versão 1.9.1. https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html (consulta em 15 de Setembro de 2026).",
    "scikit-learn developers. (2026b). DecisionTreeClassifier. Documentação scikit-learn, versão 1.9.1. https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html (consulta em 15 de Setembro de 2026).",
    "scikit-learn developers. (2026c). StratifiedKFold. Documentação scikit-learn, versão 1.9.1. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html (consulta em 15 de Setembro de 2026).",
    "scikit-learn developers. (2026d). Common pitfalls and recommended practices. Documentação scikit-learn. https://scikit-learn.org/stable/common_pitfalls.html (consulta em 15 de Setembro de 2026).",
    "Streamlit. (2026). Using forms. Documentação Streamlit. https://docs.streamlit.io/develop/concepts/architecture/forms (consulta em 15 de Setembro de 2026).",
]
for ref in referencias:
    ancora = acrescentar(ancora, ref, 187)
    p = Paragraph(ancora, doc._body)
    p.paragraph_format.line_spacing = 1
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(9)

update = doc.settings.element.find(qn("w:updateFields"))
if update is None:
    update = OxmlElement("w:updateFields")
    doc.settings.element.append(update)
update.set(qn("w:val"), "true")
alteracoes.append({"tipo": "campo do documento", "descrição": "Activada a actualização dos campos ao abrir; o índice será actualizado no Word, preservando o campo e os títulos."})

assert titulos(doc) == titulos_originais, "Os títulos foram alterados."
assert [etree.tostring(e) for e in doc.element.body.iter(qn("w:sectPr"))] == seccoes_originais
assert [(len(t.rows), len(t.columns)) for t in doc.tables] == tabelas_originais
assert len(doc.inline_shapes) == 7
assert not any(marcador in texto(doc.element.body) for marcador in ["[Preencher", "[Discutir", "[ESTA SECÇÃO", "XX,X", "X,XX"])
temporario = PASTA / "IA trabalho 11 - em revisao.docx"
doc.save(temporario)
shutil.copy2(temporario, ORIGINAL)

for nome, hash_antes in hashes.items():
    assert sha256((BASE / nome).read_bytes()).hexdigest() == hash_antes, f"Ficheiro alterado: {nome}"

manifesto = {
    "data_utc": datetime.now(timezone.utc).isoformat(),
    "documento_original_sha256": sha256(BACKUP.read_bytes()).hexdigest(),
    "documento_completado_sha256_antes_de_paginar": sha256(ORIGINAL.read_bytes()).hexdigest(),
    "versao_modelos": pacote["versao"], "titulos_preservados": titulos_originais,
    "tabelas_preservadas": tabelas_originais, "seccoes_preservadas": len(seccoes_originais),
    "ficheiros_preservados_sha256": hashes, "numero_figuras": len(ficheiros_figuras),
    "alteracoes": alteracoes,
}
(PASTA / "alteracoes_detalhadas.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")

relatorio = [
    "# Relatório de alterações — IA trabalho 11.docx", "",
    "## Resultado", "",
    "O documento foi completado no ficheiro original. Uma cópia integral anterior à edição está guardada em `IA trabalho 11 - original.docx` nesta pasta.", "",
    "Foram preservados os títulos, a sua ordem e níveis, as duas secções de página, as margens, a capa, a folha de rosto e as cinco tabelas existentes, incluindo as suas quantidades de linhas e colunas. O conteúdo acrescentado altera naturalmente o número de páginas. Não foram criados capítulos novos.", "",
    "## Conteúdo completado e corrigido", "",
    "- Resultados reais, sobreajuste, validação cruzada, discussão, resumo e conclusão quantitativa.",
    "- Metodologia actualizada de 80/20 para 75/25; validação cruzada apenas no treino; remoção das descrições de uma experiência com árvore sem limite.",
    "- A terceira linha já existente na tabela de resultados foi reaproveitada para a referência constante 'sempre 0'. Não é um terceiro modelo: acerta 60/105 casos, sem reconhecer qualquer positivo. Isto preserva a estrutura da tabela e contextualiza a exactidão.",
    "- Implementação modular, interface, persistência, avaliação com rótulos opcionais e testes automatizados descritos segundo o código actual.",
    "- Frase interrompida em 'Com isto' completada; acrescentado o enquadramento PEAS na secção existente de formulação. Remissões antigas para números de capítulos foram substituídas pelos títulos correspondentes.",
    "- Limitações e benefícios potenciais distinguidos de resultados efectivamente medidos.",
    "- Bibliografia original mantida e complementada com documentação oficial e documentos da disciplina. A referência Bigonha (2024) foi confirmada no PDF do autor, incluindo o ano.", "",
    "## Figuras", "",
]
for i, nome in enumerate(ficheiros_figuras, 1):
    relatorio.append(f"{i}. `{nome}` — versões PNG de 300 dpi e PDF vectorial, na pasta `figuras/`; imagem incorporada no Word com legenda e fonte.")
relatorio += ["", "## Validação", "",
    "- 315 casos de treino e 105 de teste, sem identificadores partilhados; 179/136 e 60/45 casos das classes 0/1, respectivamente.",
    "- Nova inferência concorda com resultados_grupo9.csv; treino em memória dos dois modelos reproduz as previsões guardadas.",
    "- Validação cruzada recalculada com semente 42; médias e desvios-padrão conferidos. Os cinco valores por modelo constam de validacao_cruzada_verificada.csv.",
    "- 11 testes automatizados do projecto executados com sucesso nesta revisão. Foram usados bancos temporários, sem adicionar exemplos ao histórico de utilização.",
    "- Títulos, níveis, margens, secções, dimensões das tabelas e sete imagens conferidos por inspecção do documento. Ausência dos marcadores de preenchimento verificada.",
    "- Os CSV, código da aplicação, modelos guardados e resultados originais não foram alterados. Os hashes constam do JSON de auditoria.", "",
    "## Operações e ficheiros auxiliares", "",
    "Foram instalados python-docx 1.2.0, lxml 6.1.3 e PyMuPDF 1.28.2 no ambiente virtual existente, exclusivamente para editar e verificar o documento. requirements.txt da aplicação não foi alterado.",
    "A pasta contém o script de edição, os gráficos, os CSV verificados, a cópia original, uma cópia de trabalho e o registo detalhado de cada substituição e inserção. A edição não altera as bases de dados de testes individuais.", "",
    "Formatação do conteúdo novo: figuras em linha com largura de 14,7 cm e texto alternativo; legendas de 10 pontos com espaçamento simples; excerto de código em Consolas de 9 pontos; células preenchidas da tabela de resultados com texto de 10 pontos; referências acrescentadas com avanço pendente de 0,6 cm. Estas definições não alteram os estilos globais, os títulos ou as dimensões das tabelas.", "",
    "## Pontos que continuam a depender dos autores", "",
    "1. A folha de rosto ainda contém o título 'Processo e Metodologia de Processo', diferente do tema da capa. Foi preservada conforme o pedido; os autores devem confirmar o título correcto.",
    "2. Não há um conjunto próprio do problema do grupo disponível. A exigência dessa avaliação adicional está explicitada em Limitações; não foram inventados dados ou resultados.",
    "3. A declaração de uso de IA exigida pela disciplina está preparada em ficheiro separado, como minuta. Os autores devem indicar apenas as verificações que efectivamente fizeram e juntar a declaração à submissão segundo a orientação da docente.",
    "4. O texto teórico preexistente foi preservado, excepto na frase incompleta e nas passagens incompatíveis com o método executado. Recomenda-se rever com os autores a definição geral de inferência (que inicialmente descreve apenas a dedução) e as generalizações sobre a fiabilidade da indução.", "",
    "## Registo integral", "",
]
for numero, item in enumerate(alteracoes, 1):
    relatorio += [f"### Alteração {numero} — {item['tipo']}", ""]
    if "secção" in item:
        relatorio += [f"Secção: {item['secção']}.", ""]
    for chave in ["motivo", "antes", "depois", "texto", "ficheiro", "legenda", "descrição"]:
        if chave in item:
            relatorio += [f"**{chave.capitalize()}:** {item[chave]}", ""]
(PASTA / "Relatorio_de_alteracoes.md").write_text("\n".join(relatorio), encoding="utf-8")
(PASTA / "Declaracao_uso_IA_minuta.md").write_text(
    "# Minuta — declaração de uso de IA\n\n"
    "**Documento para revisão e confirmação pelos autores.**\n\n"
    "Foi utilizado o assistente Codex, da OpenAI, como apoio à refactorização do protótipo, construção da interface, "
    "organização da documentação, preenchimento das secções de resultados e discussão, e geração de gráficos a partir dos dados do projecto. "
    "Nesta revisão do artigo, o assistente executou verificações das métricas, da divisão treino/teste e dos testes automatizados. "
    "Estas verificações automáticas não substituem a conferência e compreensão pelos autores.\n\n"
    "Os autores devem completar, antes da submissão:\n\n"
    "- Ferramentas de IA efectivamente utilizadas e partes do trabalho em que foram usadas.\n"
    "- Código, cálculos, figuras, fontes e afirmações verificados pessoalmente.\n"
    "- Correcções introduzidas pelos autores após essa verificação.\n"
    "- Identificação e data da declaração.\n\n"
    "Não se presume que os autores já tenham realizado estas verificações. Esta minuta foi guardada separadamente para preservar a estrutura do artigo.\n",
    encoding="utf-8")
print(f"Documento completado: {ORIGINAL}")
print(f"{len(alteracoes)} alterações registadas; 7 figuras; títulos e tabelas preservados.")
