"""Treino offline, validação cruzada apenas no treino e exportação dos artefactos."""

from datetime import datetime, timezone
from hashlib import sha256
import json

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
import sklearn

from avaliacao import METRICAS, calcular_metricas, inferir, matrizes_confusao
from dados import ALVO, BASE, ENTRADAS, FRACCAO_TESTE, SEMENTE, assinaturas, dividir_dados, ler_csv
from modelos import criar_modelos

ARTEFACTOS = BASE / "artefactos"
FICHEIRO_MODELOS = ARTEFACTOS / "modelos.joblib"


def treinar_e_guardar(destino=BASE):
    origem = BASE / "dados_referencia.csv"
    df = ler_csv(origem, exigir_alvo=True)
    treino, teste = dividir_dados(df)
    modelos = criar_modelos()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    resumo_cv = {}
    for nome, modelo in modelos.items():
        scores = cross_val_score(modelo, treino[ENTRADAS], treino[ALVO], cv=cv, scoring="accuracy")
        modelo.fit(treino[ENTRADAS], treino[ALVO])
        resumo_cv[nome] = {
            "Exactidão (treino)": accuracy_score(treino[ALVO], modelo.predict(treino[ENTRADAS])),
            "CV exactidão (média)": float(scores.mean()),
            "CV exactidão (desvio padrão)": float(scores.std()),
        }

    referencia_hash = sha256(origem.read_bytes()).hexdigest()
    codigo = b"".join((BASE / nome).read_bytes() for nome in ["dados.py", "modelos.py", "treino.py", "avaliacao.py"])
    versao = sha256(codigo + referencia_hash.encode() + sklearn.__version__.encode()).hexdigest()[:16]
    pacote = {
        "modelos": modelos, "versao": versao,
        "criado_em": datetime.now(timezone.utc).isoformat(),
        "referencia_sha256": referencia_hash,
        "ids_treino": treino.id.astype(str).tolist(), "ids_teste": teste.id.astype(str).tolist(),
        "assinaturas_treino": assinaturas(treino),
        "cursos": sorted(treino.curso.unique().tolist()),
        "semente": SEMENTE, "fraccao_teste": FRACCAO_TESTE,
        "n_treino": len(treino), "n_teste": len(teste),
    }
    previsoes = inferir(pacote, teste)
    resultados = calcular_metricas(previsoes)
    for coluna in next(iter(resumo_cv.values())):
        resultados[coluna] = resultados.Modelo.map(lambda nome: resumo_cv[nome][coluna])
    resultados["Diferença treino-teste"] = resultados["Exactidão (treino)"] - resultados["Exactidão"]
    resultados["Ficheiro de referência"] = "dados_referencia.csv"
    resultados["Conjunto"] = "teste"
    resultados["Divisão treino/teste"] = "75% / 25%"
    resultados["Semente"] = SEMENTE
    pacote["resultados"] = resultados

    destino.mkdir(parents=True, exist_ok=True)
    pasta = destino / "artefactos"
    pasta.mkdir(exist_ok=True)
    # O ficheiro de referência é apenas lido; as duas partições são ficheiros novos.
    treino.to_csv(destino / "dados_treino.csv", index=False)
    teste.to_csv(destino / "dados_teste.csv", index=False)
    resultados.to_csv(destino / "resultados_grupo9.csv", index=False)
    previsoes.to_csv(pasta / "previsoes_teste.csv", index=False)
    matrizes = {nome: matriz.tolist() for nome, matriz in matrizes_confusao(previsoes).items()}
    (pasta / "matrizes_confusao.json").write_text(json.dumps(matrizes, ensure_ascii=False, indent=2), encoding="utf-8")
    metadados = {chave: valor for chave, valor in pacote.items()
                 if chave not in ["modelos", "resultados", "assinaturas_treino"]}
    (pasta / "treino.json").write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")
    temporario = pasta / "modelos.joblib.tmp"
    joblib.dump(pacote, temporario)
    temporario.replace(pasta / "modelos.joblib")
    ax = resultados.set_index("Modelo")[METRICAS].T.plot.bar(figsize=(9, 5), ylim=(0, 1))
    ax.set_ylabel("Valor")
    ax.set_title("Comparação no teste reservado (25%)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(destino / "comparacao_modelos.png", dpi=150)
    plt.close()
    return pacote


def carregar_modelos():
    if not FICHEIRO_MODELOS.exists():
        raise FileNotFoundError("Execute primeiro: python classificador_apoio_academico.py")
    return joblib.load(FICHEIRO_MODELOS)
