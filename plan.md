# Plano — Cargos sem CBO

## Objetivo

Criar um aplicativo Streamlit em português que receba uma planilha cadastral e liste registros cujo campo CBO/ocupação esteja vazio, preservando o fluxo de conferência e exportação do sistema anterior.

## Arquitetura e decisões

- **Aplicação:** Streamlit, executado como processo único; não há banco, login ou API porque a análise ocorre no arquivo enviado pelo usuário.
- **Entrada:** CSV, XLS, XLSX e XLSM, com detecção de codificação/delimitador e leitura de cabeçalho tolerante a acentos, caixa, espaços e aliases.
- **Núcleo de dados:** funções puras de parse, normalização, validação, detecção de CBO ausente e filtros; a interface apenas compõe essas funções.
- **Interface:** cabeçalho informativo, indicadores, filtros por setor e cargo, tabela de conferência e mensagens acionáveis.
- **Exportação:** Excel com somente os resultados após filtros; cada aba terá área de impressão, cabeçalho repetido, A4 paisagem e ajuste para uma página de largura.
- **Serviço/implantação:** o Preview Webdev usará o processo Streamlit; não serão declaradas rotas, cache ou recursos gerenciados adicionais. Para uso local, `streamlit run app.py` é o comando principal.
- **Qualidade:** pytest cobrindo aliases, validação, detecção de CBO ausente, filtragem e propriedades de impressão do Excel; `py_compile` e `git diff --check` como verificações auxiliares.

## Estrutura

- `app.py`: interface Streamlit, funções de leitura/normalização/análise e exportação.
- `test_app.py`: testes unitários e de exportação.
- `requirements.txt`: dependências Python.
- `README.md`: instalação, uso e testes.
- `ideas.md`: direção visual e identidade do projeto.
- `app.config.ts`: metadado da logo do projeto.

## Verificação

Executar `pytest -q`, `python3 -m py_compile app.py test_app.py`, `git diff --check` e iniciar o Streamlit em modo headless para confirmar que o aplicativo sobe sem erro.
