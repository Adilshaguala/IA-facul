"""Testes de isolamento de dados, inferência, persistência e fluxos da interface."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from streamlit.testing.v1 import AppTest

from avaliacao import calcular_metricas, evolucao_acumulada, inferir, matrizes_confusao
from dados import ALVO, BASE, ENTRADAS, NUMERICAS, dividir_dados, ler_csv, validar_dados
from historico import guardar_teste, ler_historico
from treino import treinar_e_guardar


class ProjectoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporario = TemporaryDirectory()
        cls.destino = Path(cls.temporario.name)
        cls.original = (BASE / "dados_referencia.csv").read_bytes()
        cls.dados = ler_csv(BASE / "dados_referencia.csv", exigir_alvo=True)
        with patch("treino.cross_val_score", wraps=cross_val_score) as cv:
            cls.pacote = treinar_e_guardar(cls.destino)
            cls.chamadas_cv = cv.call_args_list
        cls.treino = ler_csv(cls.destino / "dados_treino.csv")
        cls.teste = ler_csv(cls.destino / "dados_teste.csv")

    @classmethod
    def tearDownClass(cls):
        cls.temporario.cleanup()

    def test_particoes_reproduziveis_sem_sobreposicao(self):
        self.assertEqual((len(self.treino), len(self.teste)), (315, 105))
        self.assertFalse(set(self.treino.id) & set(self.teste.id))
        self.assertEqual(set(self.treino.id) | set(self.teste.id), set(self.dados.id))
        self.assertEqual(self.original, (BASE / "dados_referencia.csv").read_bytes())
        self.assertEqual(sha256(self.original).hexdigest(), self.pacote["referencia_sha256"])
        treino, teste = dividir_dados(self.dados)
        pd.testing.assert_frame_equal(treino, self.treino)
        pd.testing.assert_frame_equal(teste, self.teste)
        combinado = pd.concat([self.treino, self.teste]).sort_values("id").reset_index(drop=True)
        pd.testing.assert_frame_equal(combinado, self.dados.sort_values("id").reset_index(drop=True))
        self.assertLess(abs(self.teste[ALVO].mean() - self.dados[ALVO].mean()), 0.01)

    def test_pre_processamento_e_validacao_apenas_no_treino(self):
        self.assertEqual(len(self.chamadas_cv), 2)
        for chamada in self.chamadas_cv:
            pd.testing.assert_frame_equal(chamada.args[1], self.treino[ENTRADAS])
            pd.testing.assert_series_equal(chamada.args[2], self.treino[ALVO])
        modelos = list(self.pacote["modelos"].values())
        self.assertEqual(len(modelos), 2)
        self.assertIsNot(modelos[0]["prep"], modelos[1]["prep"])
        for modelo in modelos:
            np.testing.assert_allclose(modelo["prep"].named_transformers_["num"].mean_, self.treino[NUMERICAS].mean())

    def test_inferencia_em_massa_igual_a_individual_e_modelo_guardado(self):
        pacote = joblib.load(self.destino / "artefactos" / "modelos.joblib")
        lote = inferir(pacote, self.teste)
        individual = inferir(pacote, self.teste.iloc[[0]])
        pd.testing.assert_frame_equal(lote[lote.Caso == 1].reset_index(drop=True), individual)
        self.assertEqual(len(lote), 210)
        self.assertTrue(lote["P(apoio=1)"].between(0, 1).all())
        self.assertEqual(calcular_metricas(lote)["Casos avaliados"].tolist(), [105, 105])

    def test_rotulos_ausentes_parciais_e_classe_unica(self):
        sem = inferir(self.pacote, self.teste.drop(columns=ALVO))
        self.assertTrue(calcular_metricas(sem).empty)
        self.assertTrue(sem.Real.isna().all())
        parcial = self.teste.head(4).copy()
        parcial[ALVO] = [1.0, np.nan, np.nan, np.nan]
        resultado = inferir(self.pacote, parcial)
        self.assertEqual(calcular_metricas(resultado)["Casos avaliados"].tolist(), [1, 1])
        for matriz in matrizes_confusao(resultado).values():
            self.assertEqual(matriz.shape, (2, 2))
            self.assertEqual(matriz.sum(), 1)

    def test_dados_de_treino_excluidos_das_metricas_mesmo_sem_id(self):
        resultado = inferir(self.pacote, self.treino.head(3).drop(columns="id"))
        self.assertTrue(resultado["Presente no treino"].all())
        self.assertTrue(calcular_metricas(resultado).empty)

    def test_validacao_csv_e_categorias_novas(self):
        for dados in [pd.DataFrame(), self.teste.drop(columns="curso")]:
            with self.assertRaises(ValueError):
                validar_dados(dados)
        for coluna, valor in [("ano", 5), ("ano", 1.5), ("tem_computador", 2),
                              ("media_anterior", np.inf), ("curso", ""),
                              ("regime", "outro"), (ALVO, "incorrecto")]:
            df = self.teste.head(1).copy().astype({coluna: object})
            df.loc[0, coluna] = valor
            with self.subTest(coluna=coluna, valor=valor), self.assertRaises(ValueError):
                validar_dados(df)
        with self.assertRaises(ValueError):
            ler_csv(BytesIO(b""))
        novo = self.teste.head(1).copy()
        novo["curso"] = "Curso novo"
        self.assertEqual(len(inferir(self.pacote, novo)), 2)

    def test_metricas_e_evolucao_com_resultados_conhecidos(self):
        resultado = pd.DataFrame({
            "Caso": [1, 2, 3, 4], "Modelo": ["Teste"] * 4,
            "Real": [0, 1, 1, np.nan], "Previsão": [0, 0, 1, 1],
            "Presente no treino": [False] * 4,
        })
        metricas = calcular_metricas(resultado).iloc[0]
        self.assertAlmostEqual(metricas["Exactidão"], 2 / 3)
        self.assertEqual(metricas["Precisão"], 1)
        self.assertEqual(metricas["Revocação"], 0.5)
        self.assertAlmostEqual(metricas["F1"], 2 / 3)
        np.testing.assert_allclose(evolucao_acumulada(resultado)["Exactidão"], [1, 0.5, 2 / 3])

    def test_historico_persistente_e_separado_por_versao(self):
        with TemporaryDirectory() as pasta:
            banco = Path(pasta) / "historico.sqlite3"
            primeiro = inferir(self.pacote, self.teste.head(1))
            segundo = inferir(self.pacote, self.teste.iloc[[1]].drop(columns=ALVO))
            guardar_teste(primeiro, "v1", banco, identificador="pedido1")
            guardar_teste(primeiro, "v1", banco, identificador="pedido1")
            guardar_teste(segundo, "v1", banco)
            guardar_teste(primeiro, "v2", banco)
            historico = ler_historico("v1", banco)
            self.assertEqual(len(historico), 4)
            self.assertEqual(historico.Caso.nunique(), 2)
            self.assertEqual(calcular_metricas(historico)["Casos avaliados"].tolist(), [1, 1])
            self.assertEqual(len(ler_historico("v2", banco)), 2)
            self.assertTrue(ler_historico("v3", banco).empty)

    def abrir_app(self):
        return AppTest.from_file(str(BASE / "app.py"), default_timeout=30).run()

    def sem_erros(self, app):
        self.assertFalse(app.exception, [erro.message for erro in app.exception])

    def test_interface_lote_reservado(self):
        with patch("treino.carregar_modelos", return_value=self.pacote), patch("treino.FICHEIRO_MODELOS", self.destino / "artefactos/modelos.joblib"):
            app = self.abrir_app()
            self.sem_erros(app)
            app.sidebar.radio[0].set_value("Testes em massa").run()
            app.button[0].click().run()
            self.sem_erros(app)
            self.assertEqual(app.metric[0].value, "105")
            self.assertEqual(len(app.session_state["massa"][1]), 210)
            self.assertGreaterEqual(len(app.get("plotly_chart")), 5)

    def test_interface_upload_e_troca_de_csv(self):
        with patch("treino.carregar_modelos", return_value=self.pacote), patch("treino.FICHEIRO_MODELOS", self.destino / "artefactos/modelos.joblib"):
            app = self.abrir_app()
            app.sidebar.radio[0].set_value("Testes em massa").run()
            next(r for r in app.radio if r.label == "Origem dos dados").set_value("Carregar CSV").run()
            csv = self.teste.head(2).drop(columns=ALVO).to_csv(index=False).encode()
            app.file_uploader[0].set_value(("sem_rotulos.csv", csv, "text/csv")).run()
            app.button[0].click().run()
            self.sem_erros(app)
            self.assertEqual(app.metric[0].value, "2")
            self.assertEqual(app.metric[1].value, "0")
            csv = self.teste.head(3).to_csv(index=False).encode()
            app.file_uploader[0].set_value(("novo.csv", csv, "text/csv")).run()
            self.assertEqual(len(app.metric), 0)
            app.button[0].click().run()
            self.sem_erros(app)
            self.assertEqual(app.metric[0].value, "3")
            app.file_uploader[0].set_value(("invalido.csv", b"curso\nTeste", "text/csv")).run()
            self.sem_erros(app)
            self.assertTrue(app.error)

    def test_interface_individual_acumula_sem_duplicar_em_recarregamento(self):
        with TemporaryDirectory() as pasta:
            banco = Path(pasta) / "historico.sqlite3"
            with patch("treino.carregar_modelos", return_value=self.pacote), \
                 patch("treino.FICHEIRO_MODELOS", self.destino / "artefactos/modelos.joblib"), \
                 patch("historico.guardar_teste", side_effect=lambda r, v: guardar_teste(r, v, banco)), \
                 patch("historico.ler_historico", side_effect=lambda v: ler_historico(v, banco)):
                app = self.abrir_app()
                app.sidebar.radio[0].set_value("Teste individual").run()
                app.button[0].click().run()
                self.sem_erros(app)
                self.assertEqual(len(ler_historico(self.pacote["versao"], banco)), 2)
                app.run()
                self.assertEqual(len(ler_historico(self.pacote["versao"], banco)), 2)
                next(s for s in app.selectbox if s.label.startswith("Decisão real")).set_value("1 — Concedido")
                app.button[0].click().run()
                self.sem_erros(app)
                historico = ler_historico(self.pacote["versao"], banco)
                self.assertEqual(len(historico), 4)
                self.assertEqual(calcular_metricas(historico)["Casos avaliados"].tolist(), [1, 1])
                reinicio = self.abrir_app()
                reinicio.sidebar.radio[0].set_value("Teste individual").run()
                self.sem_erros(reinicio)
                self.assertEqual(len(ler_historico(self.pacote["versao"], banco)), 4)


if __name__ == "__main__":
    unittest.main()
