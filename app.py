"""Interface Streamlit para análise comparativa dos pedidos de apoio académico."""

from hashlib import sha256
from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

from avaliacao import (
    METRICAS, calcular_metricas, casos_avaliaveis, evolucao_acumulada,
    inferir, matrizes_confusao,
)
from dados import ALVO, BASE, ler_csv
from historico import guardar_teste, ler_historico
from modelos import NOMES_MODELOS
from treino import FICHEIRO_MODELOS, carregar_modelos

CORES = dict(zip(NOMES_MODELOS, ["#137C8B", "#E58A35"]))


def csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def grafico(figura, chave):
    figura.update_layout(margin=dict(l=10, r=10, t=45, b=10), legend_title_text="")
    st.plotly_chart(figura, width="stretch", key=chave,
                    config={"displaylogo": False, "toImageButtonOptions": {"format": "png", "scale": 2}})


def mostrar_analise(resultados, chave, acumulada=False):
    if resultados.empty:
        st.info("Ainda não há testes individuais guardados. Preencha o formulário para começar.")
        return
    por_caso = resultados.pivot(index="Caso", columns="Modelo", values="Previsão")
    divergencias = por_caso.nunique(axis=1).gt(1)
    avaliaveis = casos_avaliaveis(resultados)
    a, b, c = st.columns(3)
    a.metric("Casos analisados", len(por_caso))
    b.metric("Casos com resultado real avaliável", avaliaveis.Caso.nunique())
    c.metric("Divergências entre modelos", int(divergencias.sum()))
    vistos = resultados.loc[resultados["Presente no treino"], "Caso"].nunique()
    if vistos:
        st.warning(f"{vistos} caso(s) coincide(m) com dados de treino. As previsões são mostradas, "
                   "mas esses casos são excluídos das métricas de teste.")
    st.caption("0 = apoio não concedido · 1 = apoio concedido · P(apoio=1) = probabilidade estimada pelo modelo.")

    st.subheader("Resultados por caso")
    apenas_divergentes = st.checkbox("Mostrar apenas divergências", key=f"{chave}_filtro")
    tabela = resultados[resultados.Caso.isin(divergencias[divergencias].index)] if apenas_divergentes else resultados
    principais = ["Caso", "id", "Data (UTC)", "Modelo", "Previsão", "P(apoio=1)", "Real", "Acertou", "Presente no treino"]
    colunas = [c for c in principais if c in tabela]
    with st.expander("Incluir os dados de entrada na tabela"):
        incluir = st.checkbox("Mostrar todas as colunas", key=f"{chave}_entradas")
    st.dataframe(tabela if incluir else tabela[colunas], hide_index=True, width="stretch",
                 column_config={"P(apoio=1)": st.column_config.NumberColumn(format="%.3f")})
    st.download_button("Descarregar todas as previsões (CSV)", csv_bytes(resultados),
                       file_name=f"{chave}_previsoes.csv", mime="text/csv", key=f"{chave}_download")

    st.subheader("Comparação das previsões")
    esquerda, direita = st.columns(2)
    with esquerda:
        contagem = resultados.groupby(["Modelo", "Previsão"]).size().reset_index(name="Casos")
        contagem["Decisão prevista"] = contagem["Previsão"].map({0: "Não concedido", 1: "Concedido"})
        grafico(px.bar(contagem, x="Decisão prevista", y="Casos", color="Modelo", barmode="group",
                       color_discrete_map=CORES, title="Decisões previstas"), f"{chave}_distribuicao")
    with direita:
        probabilidades = resultados.pivot(index="Caso", columns="Modelo", values="P(apoio=1)").reset_index()
        grafico(px.scatter(probabilidades, x=NOMES_MODELOS[0], y=NOMES_MODELOS[1], hover_data=["Caso"],
                           range_x=[0, 1], range_y=[0, 1], title="Probabilidade de apoio por caso"), f"{chave}_probabilidades")

    metricas = calcular_metricas(resultados)
    if metricas.empty:
        st.info("Para calcular exactidão, precisão, revocação, F1 e matriz de confusão, "
                "é necessário indicar a decisão real em casos que não pertencem ao treino.")
        return
    st.subheader("Desempenho nos casos com decisão real")
    st.caption("Classe positiva: apoio concedido (1). Métricas sem denominador são apresentadas como 0. "
               "Casos sem decisão real são excluídos. Repetições submetidas contam como novos testes.")
    st.dataframe(metricas, hide_index=True, width="stretch")
    st.download_button("Descarregar métricas (CSV)", csv_bytes(metricas), file_name=f"{chave}_metricas.csv",
                       mime="text/csv", key=f"{chave}_metricas_download")
    longo = metricas.melt(id_vars="Modelo", value_vars=METRICAS, var_name="Métrica", value_name="Valor")
    grafico(px.bar(longo, x="Métrica", y="Valor", color="Modelo", barmode="group", range_y=[0, 1],
                   color_discrete_map=CORES, title="Exactidão, precisão, revocação e F1"), f"{chave}_metricas")
    for coluna, (nome, matriz) in zip(st.columns(2), matrizes_confusao(resultados).items()):
        with coluna:
            figura = px.imshow(matriz, text_auto=True, x=["0 — Não concedido", "1 — Concedido"],
                               y=["0 — Não concedido", "1 — Concedido"], color_continuous_scale="Teal",
                               labels={"x": "Previsão", "y": "Decisão real", "color": "Casos"}, title=nome)
            grafico(figura, f"{chave}_matriz_{nome}")
    if acumulada:
        grafico(px.line(evolucao_acumulada(resultados), x="Casos rotulados acumulados", y="Exactidão",
                        color="Modelo", markers=True, range_y=[0, 1], color_discrete_map=CORES,
                        title="Evolução da exactidão acumulada"), f"{chave}_evolucao")


def pagina_treino(pacote):
    st.header("Treino e avaliação de referência")
    a, b, c = st.columns(3)
    a.metric("Casos de treino · 75%", pacote["n_treino"])
    b.metric("Casos de teste · 25%", pacote["n_teste"])
    c.metric("Semente aleatória", pacote["semente"])
    st.write("A Regressão Logística e a Árvore de Decisão foram treinadas nos mesmos 315 casos. "
             "A validação cruzada de 5 partes usa apenas o treino. Os 105 casos reservados são usados para a avaliação final.")
    resultados = pacote["resultados"]
    st.dataframe(resultados, hide_index=True, width="stretch")
    comparacao = resultados.rename(columns={"Exactidão": "Teste", "Exactidão (treino)": "Treino",
                                            "CV exactidão (média)": "Validação cruzada"})
    longo = comparacao.melt(id_vars="Modelo", value_vars=["Treino", "Validação cruzada", "Teste"],
                            var_name="Conjunto", value_name="Exactidão")
    grafico(px.bar(longo, x="Conjunto", y="Exactidão", color="Modelo", barmode="group",
                   range_y=[0, 1], color_discrete_map=CORES, title="Generalização: treino, validação e teste"), "treino_comparacao")
    for _, row in resultados.iterrows():
        if row["Diferença treino-teste"] > 0.1:
            st.info(f"{row['Modelo']}: a exactidão desce {row['Diferença treino-teste']:.1%} "
                    "entre treino e teste. Esta diferença sugere sobreajuste; deve ser discutida com os resultados da validação cruzada.")
    st.download_button("Descarregar tabela de referência", csv_bytes(resultados),
                       file_name="resultados_grupo9.csv", mime="text/csv")
    st.subheader("Método usado")
    st.markdown("""
    - **Repartição:** aleatória e estratificada pela decisão histórica, com semente 42.
    - **Entradas:** curso, ano, regime e características académicas e materiais.
    - **Preparação:** normalização das variáveis numéricas e codificação das categorias, ajustadas dentro de cada treino.
    - **Regressão Logística:** até 1 000 iterações. **Árvore de Decisão:** profundidade máxima de 5.
    - **Colunas excluídas:** `id` é um identificador; `necessidade_avaliada` fica disponível como medida independente.
    - **Decisão:** classe seleccionada pelo método `predict` de cada modelo; a probabilidade apresentada refere-se à classe 1.
    """)
    st.caption(f"Versão dos modelos: {pacote['versao']} · Treinados em {pacote['criado_em']}")


def pagina_massa(pacote):
    st.header("Testes em massa")
    st.write("Carregue um CSV para comparar os dois modelos em todos os casos.")
    origem = st.radio("Origem dos dados", ["Teste reservado (dados_teste.csv)", "Carregar CSV"], horizontal=True)
    conteudo = None
    if origem == "Carregar CSV":
        ficheiro = st.file_uploader("CSV de teste", type=["csv"])
        if ficheiro is not None:
            conteudo = ficheiro.getvalue()
        st.caption("Use as colunas de entrada de dados_teste.csv. A coluna apoio_concedido é opcional; "
                   "pode estar vazia nos casos sem decisão real conhecida.")
    else:
        caminho = BASE / "dados_teste.csv"
        if caminho.exists():
            conteudo = caminho.read_bytes()
            st.download_button("Descarregar os 105 casos de teste", conteudo, file_name="dados_teste.csv", mime="text/csv")
        else:
            st.error("O ficheiro de teste está em falta. Execute novamente o treino.")
    if conteudo is None:
        return
    chave_dados = sha256(conteudo + pacote["versao"].encode()).hexdigest()
    try:
        dados = ler_csv(BytesIO(conteudo))
    except ValueError as exc:
        st.error(str(exc))
        return
    st.caption(f"{len(dados)} casos carregados.")
    novos = sorted(set(dados.curso) - set(pacote["cursos"]))
    if novos:
        st.info("Cursos não observados no treino: " + ", ".join(novos) + ". A codificação ignora essas categorias desconhecidas.")
    if st.button("Analisar CSV", type="primary"):
        with st.spinner("A calcular as previsões…"):
            st.session_state["massa"] = (chave_dados, inferir(pacote, dados))
    salvo = st.session_state.get("massa")
    if salvo is not None and salvo[0] == chave_dados:
        mostrar_analise(salvo[1], "massa")


def pagina_individual(pacote):
    st.header("Teste individual")
    st.write("Introduza um pedido. Cada submissão guarda as previsões dos dois modelos e actualiza a análise acumulada.")
    with st.form("pedido"):
        esquerda, direita = st.columns(2)
        with esquerda:
            curso = st.selectbox("Curso", pacote["cursos"])
            ano = st.selectbox("Ano curricular", [1, 2, 3, 4])
            regime = st.selectbox("Regime", ["laboral", "pos_laboral"])
            media = st.number_input("Média anterior", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
            atraso = st.number_input("Disciplinas em atraso", min_value=0, value=0, step=1)
        with direita:
            horas = st.number_input("Horas de trabalho semanal", min_value=0, max_value=168, value=0, step=1)
            distancia = st.number_input("Distância ao campus (km)", min_value=0.0, value=5.0, step=0.1)
            computador = st.checkbox("Tem computador próprio", value=True)
            internet = st.checkbox("Tem Internet em casa", value=True)
            anteriores = st.number_input("Pedidos anteriores", min_value=0, value=0, step=1)
        real = st.selectbox("Decisão real conhecida (opcional)", ["Desconhecida", "0 — Não concedido", "1 — Concedido"])
        enviado = st.form_submit_button("Inferir e guardar", type="primary")
    if enviado:
        entrada = {
            "curso": curso, "ano": ano, "regime": regime, "media_anterior": media,
            "disciplinas_em_atraso": atraso, "horas_trabalho_semanal": horas,
            "distancia_campus_km": distancia, "tem_computador": int(computador),
            "acesso_internet_casa": int(internet), "pedidos_anteriores": anteriores,
        }
        if real != "Desconhecida":
            entrada[ALVO] = int(real[0])
        previsoes = inferir(pacote, pd.DataFrame([entrada]))
        guardar_teste(previsoes, pacote["versao"])
        st.success("Teste guardado no histórico.")
    historico = ler_historico(pacote["versao"])
    if not historico.empty:
        st.subheader("Último teste guardado")
        ultimo = historico[historico.Caso == historico.Caso.max()]
        for coluna, (_, row) in zip(st.columns(2), ultimo.iterrows()):
            coluna.metric(row["Modelo"], "Concedido" if row["Previsão"] else "Não concedido")
            coluna.caption(f"Probabilidade estimada de apoio: {row['P(apoio=1)']:.1%}")
    st.divider()
    st.subheader("Análise acumulada")
    st.caption("O histórico permanece guardado ao fechar a aplicação. Esta análise reúne os testes "
               "individuais da versão actual dos modelos; cada nova submissão conta como um teste.")
    mostrar_analise(historico, "individual", acumulada=True)


def main():
    st.set_page_config(page_title="Apoio académico · Análise de modelos", page_icon="📊", layout="wide")
    st.title("Apoio académico")
    st.caption("APRENDIZAGEM SUPERVISIONADA · REGRESSÃO LOGÍSTICA E ÁRVORE DE DECISÃO")
    if not FICHEIRO_MODELOS.exists():
        st.info("Prepare os dados e treine os modelos uma vez antes de começar.")
        st.code("python classificador_apoio_academico.py", language="bash")
        return
    pacote = carregar_modelos()
    with st.sidebar:
        st.header("Laboratório de modelos")
        pagina = st.radio("Navegação", ["Treino e resultados", "Testes em massa", "Teste individual"])
        st.divider()
        st.write("**75% treino / 25% teste**")
        st.caption("315 casos para aprender · 105 para avaliar")
        st.caption("Os modelos reproduzem decisões históricas. A previsão não é uma avaliação independente da necessidade de apoio.")
    if pagina == "Treino e resultados":
        pagina_treino(pacote)
    elif pagina == "Testes em massa":
        pagina_massa(pacote)
    else:
        pagina_individual(pacote)


if __name__ == "__main__":
    main()
