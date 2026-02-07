#!/usr/bin/env python3
from crm_core.db.base import get_db
from crm_modules.contratos.service import ContratoService

db = next(get_db())
try:
    service = ContratoService(repository_session=db)
    contratos_service = service.listar_todos_contratos()
    print(f'Contratos no service: {len(contratos_service)}')
    for contrato in contratos_service:
        print(f'ID: {contrato.get("id")}, Titulo: {contrato.get("titulo")}, Cliente: {contrato.get("cliente_nome")}')
finally:
    db.close()