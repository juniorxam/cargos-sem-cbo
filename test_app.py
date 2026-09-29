import io

import pandas as pd
from openpyxl import load_workbook

import app


def make_source(rows):
    return pd.DataFrame(
        [["Cargo", "Setor", "Código da CBO", "Servidor", "NUMFUNC"]] + rows
    )


def test_parse_raw_recognizes_cbo_alias_and_cargo():
    parsed = app.parse_raw(make_source([["Enfermeiro", "A", "", "Ana", "1"]]))

    assert list(parsed.columns[:3]) == ["CARGO", "SETOR", "CBO"]


def test_schema_requires_cargo_and_cbo_columns():
    assert app.validate_source_schema(pd.DataFrame(columns=["CARGO"])) is not None
    assert app.validate_source_schema(pd.DataFrame(columns=["CARGO", "CBO"])) is None


def test_alert_cbo_vazio_lists_only_cargos_without_cbo():
    parsed = app.parse_raw(make_source([
        ["Enfermeiro", "A", "", "Ana", "1"],
        ["Técnico", "A", "3222-05", "Bia", "2"],
        ["Médico", "B", "   ", "Caio", "3"],
    ]))
    cleaned = app.clean(parsed)

    result = app.alert_cbo_vazio(cleaned)

    assert result["CARGO"].tolist() == ["Enfermeiro", "Médico"]
    assert result["PROBLEMA"].eq("Cargo cadastrado sem CBO preenchido").all()


def test_filter_pendencias_filters_by_sector_and_cargo():
    parsed = app.parse_raw(make_source([
        ["Enfermeiro", "A", "", "Ana", "1"],
        ["Enfermeiro", "B", "", "Bia", "2"],
        ["Técnico", "A", "", "Caio", "3"],
    ]))
    pendencias = app.alert_cbo_vazio(app.clean(parsed))

    result = app.filter_pendencias(pendencias, setor="A", cargo="Enfermeiro")

    assert len(result) == 1
    assert result.iloc[0]["SERVIDOR"] == "Ana"


def test_excel_export_is_a4_landscape_one_page_wide():
    content = app.df_to_excel_bytes({"Dados": pd.DataFrame({"CARGO": ["Enfermeiro"]})})
    workbook = load_workbook(io.BytesIO(content))
    sheet = workbook["Dados"]

    assert sheet.page_setup.orientation == "landscape"
    assert str(sheet.page_setup.paperSize) == str(sheet.PAPERSIZE_A4)
    assert sheet.page_setup.fitToWidth == 1
    assert sheet.page_setup.fitToHeight == 0
    assert sheet.print_area == "'Dados'!$A$1:$A$2"
