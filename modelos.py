"""Definição dos dois algoritmos e dos respectivos pré-processadores."""

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from dados import CATEGORICAS, NUMERICAS, SEMENTE

NOMES_MODELOS = ("Regressão Logística", "Árvore de Decisão")


def criar_modelos():
    algoritmos = [
        LogisticRegression(max_iter=1000, random_state=SEMENTE),
        DecisionTreeClassifier(max_depth=5, random_state=SEMENTE),
    ]
    modelos = {}
    for nome, algoritmo in zip(NOMES_MODELOS, algoritmos):
        # Cada modelo recebe o seu próprio pré-processador, ajustado só no treino.
        preparacao = ColumnTransformer([
            ("num", StandardScaler(), NUMERICAS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
        ])
        modelos[nome] = Pipeline([("prep", preparacao), ("clf", algoritmo)])
    return modelos
