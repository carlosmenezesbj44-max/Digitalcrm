# CRM Provedor

Sistema de CRM para provedores de serviços.

## Instalação

1. Instale o Poetry: `pip install poetry`
2. Instale as dependências: `poetry install`
3. Configure o ambiente: copie `.env.example` para `.env` e ajuste as variáveis.

## Executar

- API: `poetry run uvicorn interfaces.api.main:app --reload`
- CLI: `poetry run python interfaces/cli/cli.py`

## Estrutura do Projeto

- `crm_core/`: Núcleo compartilhado (config, DB, segurança, etc.)
- `crm_modules/`: Módulos de negócio (clientes, contratos, etc.)
- `interfaces/`: Interfaces (API FastAPI, web opcional, CLI)
- `tasks/`: Tarefas assíncronas
- `tests/`: Testes

## Desenvolvimento

Use `black` e `isort` para formatação.
