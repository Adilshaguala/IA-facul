"""Histórico local persistente: uma transacção por teste individual."""

from datetime import datetime, timezone
import json
import sqlite3
from uuid import uuid4

import pandas as pd

from dados import BASE

BANCO = BASE / "artefactos" / "historico.sqlite3"


def conectar(caminho):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(caminho)
    con.execute("""CREATE TABLE IF NOT EXISTS testes (
        numero INTEGER PRIMARY KEY AUTOINCREMENT,
        identificador TEXT NOT NULL UNIQUE,
        data_utc TEXT NOT NULL,
        versao TEXT NOT NULL,
        resultados TEXT NOT NULL
    )""")
    return con


def guardar_teste(resultados, versao, caminho=BANCO, identificador=None):
    identificador = identificador or str(uuid4())
    con = conectar(caminho)
    try:
        with con:
            con.execute("INSERT OR IGNORE INTO testes (identificador, data_utc, versao, resultados) VALUES (?, ?, ?, ?)",
                        (identificador, datetime.now(timezone.utc).isoformat(), versao,
                         resultados.to_json(orient="records", force_ascii=False)))
    finally:
        con.close()
    return identificador


def ler_historico(versao, caminho=BANCO):
    con = conectar(caminho)
    try:
        registos = con.execute("SELECT numero, data_utc, resultados FROM testes WHERE versao = ? ORDER BY numero",
                               (versao,)).fetchall()
    finally:
        con.close()
    linhas = []
    for numero, data, payload in registos:
        for row in json.loads(payload):
            row["Caso"] = numero
            row["Data (UTC)"] = data
            linhas.append(row)
    return pd.DataFrame(linhas)
