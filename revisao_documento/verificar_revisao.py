"""Confere a revisão guardada pelo Word e fecha o relatório de alterações."""

from hashlib import sha256
from pathlib import Path
import json

from docx import Document
from docx.oxml.ns import qn

PASTA = Path(__file__).resolve().parent
BASE = PASTA.parent
manifesto = json.loads((PASTA / "alteracoes_detalhadas.json").read_text(encoding="utf-8"))
original = Document(PASTA / "IA trabalho 11 - original.docx")
novo = Document(BASE / "IA trabalho 11.docx")
rascunho = Document(PASTA / "IA trabalho 11 - em revisao.docx")


def texto(elemento):
    return "".join(t.text or "" for t in elemento.iter(qn("w:t")))


def titulos(documento):
    return [[n.get(qn("w:val")), texto(e)] for e in documento.element.body.iter(qn("w:p"))
            for n in e.findall("w:pPr/w:pStyle", e.nsmap)
            if n.get(qn("w:val")).startswith("Heading")]


assert titulos(novo) == manifesto["titulos_preservados"]
assert len(novo.inline_shapes) == 7
assert [(len(t.rows), len(t.columns)) for t in original.tables] == [(len(t.rows), len(t.columns)) for t in novo.tables]
for seccao_a, seccao_b in zip(original.sections, novo.sections):
    for nome in ["page_width", "page_height", "left_margin", "right_margin", "top_margin", "bottom_margin"]:
        assert abs(getattr(seccao_a, nome) - getattr(seccao_b, nome)) < 2000
for i in [0, 1]:
    assert original.tables[i].cell(0, 0).text == novo.tables[i].cell(0, 0).text
assert [texto(e) for e in rascunho.element.body if e.tag != qn("w:sdt")] == [
    texto(e) for e in novo.element.body if e.tag != qn("w:sdt")]
for nome, checksum in manifesto["ficheiros_preservados_sha256"].items():
    assert sha256((BASE / nome).read_bytes()).hexdigest() == checksum
assert sha256((PASTA / "IA trabalho 11 - original.docx").read_bytes()).hexdigest() == manifesto["documento_original_sha256"]
conteudo = texto(novo.element.body)
for marcador in ["[Preencher", "[Discutir", "[ESTA SECÇÃO", "XX,X", "X,XX"]:
    assert marcador not in conteudo
indice = texto(list(novo.element.body)[2])
assert "Metodologia de Construção do Artefacto" in indice
assert "Resultados no conjunto de dados de referência" in indice

validacao = {
    "titulos_preservados": len(titulos(novo)),
    "tabelas_preservadas": len(novo.tables),
    "figuras_incorporadas": len(novo.inline_shapes),
    "indice_actualizado_no_word": True,
    "capa_e_folha_de_rosto_preservadas": True,
    "ficheiros_protegidos_intactos": True,
    "documento_final_sha256": sha256((BASE / "IA trabalho 11.docx").read_bytes()).hexdigest(),
    "exportacao_pdf": "Não concluída: ExportAsFixedFormat e SaveAs2 bloquearam. As instâncias iniciadas para a revisão foram encerradas após guardar o DOCX.",
    "verificacao_visual": "Gráficos inspeccionados como imagens; paginação final não verificada visualmente em PDF.",
}
(PASTA / "verificacao_final.json").write_text(json.dumps(validacao, ensure_ascii=False, indent=2), encoding="utf-8")
manifesto["verificacao_final"] = validacao
(PASTA / "alteracoes_detalhadas.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")

relatorio = PASTA / "Relatorio_de_alteracoes.md"
nota = """

## Fecho da revisão e limite da verificação visual

O Word instalado abriu e guardou o DOCX e actualizou o índice, preservando os 39 títulos existentes. A verificação posterior confirmou as sete figuras incorporadas, as cinco tabelas com as dimensões originais, a capa, a folha de rosto e as margens. O texto fora dos campos de índice/bibliografia permaneceu idêntico ao da revisão preparada pelo script.

A tentativa adicional de exportar um PDF completo bloqueou com os métodos ExportAsFixedFormat e SaveAs2. Foram consultadas apenas as instâncias do Word iniciadas para esta tarefa e estas foram encerradas (processos 9472 e 12716); as outras instâncias não foram terminadas. Não foi produzido um PDF completo do artigo. Os PDF individuais dos gráficos estão disponíveis na pasta figuras.

Os gráficos foram inspeccionados directamente como imagens. A paginação final do Word não foi conferida visualmente em PDF; recomenda-se conferir a vista de impressão antes da entrega. Os hashes finais e o resultado dos controlos constam de verificacao_final.json. Nenhum capítulo novo foi acrescentado.

As fontes externas efectivamente consultadas são as entradas de documentação oficial e o PDF de Bigonha indicados na bibliografia. A minuta da declaração de uso de IA permanece separada e necessita de confirmação dos autores. O script de diagnóstico de janelas e o script de paginação foram conservados nesta pasta para documentar as operações realizadas.
"""
relatorio.write_text(relatorio.read_text(encoding="utf-8") + nota, encoding="utf-8")
print(json.dumps(validacao, ensure_ascii=False, indent=2))
