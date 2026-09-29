# Cargos sem CBO

Aplicativo Streamlit para auditar cadastros funcionais e localizar todos os registros em que o cargo está preenchido, mas o campo **CBO/OCUPAÇÃO** está vazio, nulo ou contém apenas espaços.

## Funcionalidades

O sistema aceita arquivos CSV, XLS, XLSX e XLSM. Ele reconhece variações comuns dos cabeçalhos, valida a presença de `CARGO` e `CBO/OCUPAÇÃO`, mostra indicadores da base e permite filtrar os resultados por setor e cargo. A tela apresenta tanto a lista detalhada para correção quanto um resumo agrupado por cargo.

A exportação gera um Excel com os resultados atuais após os filtros. As abas são configuradas para impressão em **A4 paisagem**, com ajuste para **uma página de largura**, área de impressão, cabeçalho repetido e congelamento do cabeçalho.

## Como executar

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

Depois, envie a planilha pela barra lateral. Se os nomes das colunas forem diferentes, use cabeçalhos equivalentes a `CARGO`, `SETOR` e `CBO` ou `OCUPAÇÃO`.

## Testes

```bash
pytest -q
python3 -m py_compile app.py test_app.py
```
