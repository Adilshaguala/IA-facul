"""Inferência e métricas partilhadas pela linha de comandos e interface."""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

from dados import ALVO, ENTRADAS, assinaturas, validar_dados

METRICAS = ["Exactidão", "Precisão", "Revocação", "F1"]


def inferir(pacote, dados):
    dados = validar_dados(dados)
    vistos = set(pacote["assinaturas_treino"])
    ids_treino = set(pacote["ids_treino"])
    pertence_treino = [
        assinatura in vistos or str(dados.iloc[i].get("id", "")) in ids_treino
        for i, assinatura in enumerate(assinaturas(dados))
    ]
    resultados = []
    for nome, modelo in pacote["modelos"].items():
        predicoes = modelo.predict(dados[ENTRADAS])
        indice_positivo = list(modelo.classes_).index(1)
        probabilidades = modelo.predict_proba(dados[ENTRADAS])[:, indice_positivo]
        tabela = dados.drop(columns=["Caso", "Modelo", "Previsão", "P(apoio=1)",
                                     "Presente no treino", "Real", "Acertou"], errors="ignore").copy()
        tabela.insert(0, "Caso", range(1, len(dados) + 1))
        tabela["Modelo"] = nome
        tabela["Previsão"] = predicoes
        tabela["P(apoio=1)"] = probabilidades
        tabela["Presente no treino"] = pertence_treino
        tabela["Real"] = dados[ALVO] if ALVO in dados else np.nan
        tabela["Acertou"] = [None if pd.isna(real) else bool(real == pred)
                              for real, pred in zip(tabela["Real"], predicoes)]
        resultados.append(tabela)
    return pd.concat(resultados, ignore_index=True).sort_values(["Caso", "Modelo"]).reset_index(drop=True)


def casos_avaliaveis(resultados):
    """Métricas só para casos rotulados que não foram usados no treino."""
    return resultados[resultados["Real"].notna() & ~resultados["Presente no treino"].astype(bool)]


def calcular_metricas(resultados):
    linhas = []
    for nome, grupo in casos_avaliaveis(resultados).groupby("Modelo", sort=False):
        real, pred = grupo["Real"].astype(int), grupo["Previsão"].astype(int)
        linhas.append({
            "Modelo": nome, "Casos avaliados": len(grupo),
            "Exactidão": accuracy_score(real, pred),
            "Precisão": precision_score(real, pred, zero_division=0),
            "Revocação": recall_score(real, pred, zero_division=0),
            "F1": f1_score(real, pred, zero_division=0),
        })
    return pd.DataFrame(linhas, columns=["Modelo", "Casos avaliados"] + METRICAS)


def matrizes_confusao(resultados):
    return {nome: confusion_matrix(grupo["Real"].astype(int), grupo["Previsão"], labels=[0, 1])
            for nome, grupo in casos_avaliaveis(resultados).groupby("Modelo", sort=False)}


def evolucao_acumulada(resultados):
    linhas = []
    for nome, grupo in casos_avaliaveis(resultados).groupby("Modelo", sort=False):
        grupo = grupo.sort_values("Caso")
        acertos = grupo["Real"].to_numpy() == grupo["Previsão"].to_numpy()
        for numero, valor in enumerate(np.cumsum(acertos) / np.arange(1, len(grupo) + 1), 1):
            linhas.append({"Modelo": nome, "Casos rotulados acumulados": numero, "Exactidão": valor})
    return pd.DataFrame(linhas)
