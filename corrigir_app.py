#!/usr/bin/env python3
# -*- coding: utf-8 -*-

app_content = '''from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from crm_core.config.settings import settings

from crm_core.db.base import get_db
from sqlalchemy.orm import Session

app = FastAPI(title="CRM Provedor Web", version="1.0.0")

app.mount("/static", StaticFiles(directory="interfaces/web/static"), name="static")
templates = Jinja2Templates(directory="interfaces/web/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "CRM Provedor"})


@app.get("/test")
def test(request: Request):
    return {"message": "test"}


@app.get("/clientes/novo", response_class=HTMLResponse)
def novo_cliente_form(request: Request):
    return templates.TemplateResponse("novo_cliente.html", {"request": request})


@app.post("/clientes/novo")
async def criar_cliente(request: Request, db: Session = Depends(get_db)):
    from crm_modules.clientes.service import ClienteService
    from crm_modules.clientes.schemas import ClienteCreate
    try:
        form_data = await request.form()
        cliente_data = {
            "nome": form_data.get("nome"),
            "email": form_data.get("email"),
            "telefone": form_data.get("telefone"),
            "cpf": form_data.get("cpf"),
            "endereco": form_data.get("endereco")
        }
        service = ClienteService()
        cliente_create = ClienteCreate(**cliente_data)
        cliente = service.criar_cliente(cliente_create)
        return {"success": True, "message": "Cliente cadastrado com sucesso", "cliente_id": cliente.id}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.get("/clientes", response_class=HTMLResponse)
def listar_clientes(request: Request, db: Session = Depends(get_db)):
    from crm_modules.clientes.service import ClienteService
    service = ClienteService()
    clientes = service.listar_clientes_ativos()
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=settings.debug)
'''

with open('interfaces/web/app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("app.py corrigido - rotas reordenadas!")
print("   - /clientes/novo agora vem ANTES de /clientes")
print("   - Reinicie o servidor para aplicar as mudancas")
