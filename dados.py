"""Esquema, validação e divisão reproduzível dos dados de referência."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
SEMENTE = 42
FRACCAO_TESTE = 0.25
ALVO = "apoio_concedido"
CATEGORICAS = ["curso", "ano", "regime"]
NUMERICAS = [
    "media_anterior", "disciplinas_em_atraso", "horas_trabalho_semanal",
    "distancia_campus_km", "tem_computador", "acesso_internet_casa",
    "pedidos_anteriores",
]
ENTRADAS = CATEGORICAS + NUMERICAS


def validar_dados(df, exigir_alvo=False):
    """Rejeita entradas inválidas; o alvo pode estar ausente ou parcialmente vazio."""
    if df.empty:
        raise ValueError("O CSV não contém casos.")
    if df.columns.duplicated().any():
        raise ValueError("O CSV tem nomes de colunas repetidos.")
    faltam = set(ENTRADAS) - set(df.columns)
    if faltam:
        raise ValueError("Faltam colunas: " + ", ".join(sorted(faltam)))
    df = df.copy().reset_index(drop=True)
    if df[ENTRADAS].isna().any().any():
        raise ValueError("As colunas de entrada não podem conter valores vazios.")
    for coluna in NUMERICAS + ["ano"]:
        try:
            df[coluna] = pd.to_numeric(df[coluna], errors="raise")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"A coluna {coluna} deve conter números.") from exc
        if not np.isfinite(df[coluna]).all():
            raise ValueError(f"A coluna {coluna} contém números não finitos.")
        if (df[coluna] < 0).any():
            raise ValueError(f"A coluna {coluna} não pode ter valores negativos.")
    inteiras = ["ano", "disciplinas_em_atraso", "horas_trabalho_semanal",
                "tem_computador", "acesso_internet_casa", "pedidos_anteriores"]
    for coluna in inteiras:
        if (df[coluna] % 1 != 0).any():
            raise ValueError(f"A coluna {coluna} deve conter números inteiros.")
        df[coluna] = df[coluna].astype(int)
    for coluna in ["tem_computador", "acesso_internet_casa"]:
        if not df[coluna].isin([0, 1]).all():
            raise ValueError(f"A coluna {coluna} só aceita 0 ou 1.")
    if not df.ano.between(1, 4).all():
        raise ValueError("O ano curricular deve estar entre 1 e 4.")
    if not df.media_anterior.between(0, 20).all():
        raise ValueError("A média anterior deve estar entre 0 e 20.")
    if not df.horas_trabalho_semanal.le(168).all():
        raise ValueError("As horas de trabalho semanal não podem exceder 168.")
    if not df.regime.isin(["laboral", "pos_laboral"]).all():
        raise ValueError("O regime deve ser laboral ou pos_laboral.")
    if not df.curso.map(lambda valor: isinstance(valor, str) and bool(valor.strip())).all():
        raise ValueError("O curso deve ser um texto não vazio.")
    if exigir_alvo and (ALVO not in df or df[ALVO].isna().any()):
        raise ValueError(f"O treino exige {ALVO} preenchido em todas as linhas.")
    if ALVO in df:
        try:
            df[ALVO] = pd.to_numeric(df[ALVO], errors="raise")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{ALVO} só aceita 0, 1 ou vazio.") from exc
        if not df[ALVO].dropna().isin([0, 1]).all():
            raise ValueError(f"{ALVO} só aceita 0, 1 ou vazio.")
    return df


def ler_csv(origem, exigir_alvo=False):
    try:
        df = pd.read_csv(origem)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeError) as exc:
        raise ValueError("Não foi possível ler o CSV. Use UTF-8 e separador vírgula.") from exc
    return validar_dados(df, exigir_alvo)


def dividir_dados(df):
    """Selecciona 25% aleatoriamente, preservando a proporção de classes."""
    df = validar_dados(df, exigir_alvo=True)
    if "id" not in df or df.id.isna().any() or df.id.duplicated().any():
        raise ValueError("Os dados de referência devem ter identificadores únicos.")
    treino, teste = train_test_split(
        df, test_size=FRACCAO_TESTE, random_state=SEMENTE, stratify=df[ALVO],
    )
    return treino.reset_index(drop=True), teste.reset_index(drop=True)


def assinaturas(df):
    """Identifica entradas iguais às de treino, mesmo que o CSV omita o id."""
    return [tuple(str(row[c]) if c in ["curso", "regime"] else float(row[c])
                  for c in ENTRADAS) for _, row in df.iterrows()]
