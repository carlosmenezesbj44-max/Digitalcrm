#!/usr/bin/env python3

app_content = '''from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
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


@app.get("/clientes", response_class=HTMLResponse)
def listar_clientes(request: Request, db: Session = Depends(get_db)):
    from crm_modules.clientes.service import ClienteService
    service = ClienteService()
    clientes = service.listar_clientes_ativos()
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})


@app.get("/test")
def test(request: Request):
    return {"message": "test"}


@app.get("/clientes/novo")
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


# ============================================
# ORDENS DE SERVICO - Routes
# IMPORTANT: Action routes must come BEFORE generic {ordem_id} route
# ============================================

@app.get("/ordens-servico", response_class=HTMLResponse)
def listar_ordens_servico(request: Request, db: Session = Depends(get_db)):
    """Lista todas as ordens de serviço"""
    try:
        from crm_modules.ordens_servico.service import OrdemServicoService
        service = OrdemServicoService(repository_session=db)
        ordens = service.listar_ordens_servico()
        return templates.TemplateResponse("ordens_servico.html", {"request": request, "ordens": ordens})
    except Exception as e:
        return templates.TemplateResponse("ordens_servico.html", {"request": request, "ordens": [], "error": str(e)})


@app.get("/ordens-servico/nova", response_class=HTMLResponse)
def nova_ordem_form(request: Request, db: Session = Depends(get_db)):
    """Formulário para criar nova ordem de serviço"""
    try:
        from crm_modules.clientes.service import ClienteService
        cliente_service = ClienteService(repository_session=db)
        clientes = cliente_service.listar_clientes()[:10]  # Primeiros 10 clientes (mais recentes)
        return templates.TemplateResponse("nova_ordem_servico.html", {"request": request, "clientes": clientes})
    except Exception as e:
        return templates.TemplateResponse("nova_ordem_servico.html", {"request": request, "clientes": [], "error": str(e)})


# ACTION ROUTES - Must come BEFORE generic {ordem_id} route
@app.post("/ordens-servico/{ordem_id}/iniciar", include_in_schema=False)
async def iniciar_ordem_web(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Inicia uma ordem de serviço via web"""
    from crm_modules.ordens_servico.service import OrdemServicoService
    try:
        data = await request.json()
        tecnico = data.get('tecnico', '') or 'Técnico'
        
        service = OrdemServicoService(repository_session=db)
        service.iniciar_ordem_servico(ordem_id, tecnico)
        
        return JSONResponse({"success": True})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)


@app.post("/ordens-servico/{ordem_id}/aguardando-peca", include_in_schema=False)
async def aguardando_peca_web(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Marca OS como aguardando peça"""
    from crm_modules.ordens_servico.service import OrdemServicoService
    try:
        data = await request.json()
        observacoes = data.get('observacoes', None)
        
        service = OrdemServicoService(repository_session=db)
        service.aguardando_peca_ordem_servico(ordem_id, observacoes)
        
        return JSONResponse({"success": True})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)


@app.post("/ordens-servico/{ordem_id}/retomar", include_in_schema=False)
async def retomar_ordem_web(ordem_id: int, db: Session = Depends(get_db)):
    """Retoma uma ordem de serviço"""
    from crm_modules.ordens_servico.service import OrdemServicoService
    try:
        service = OrdemServicoService(repository_session=db)
        service.retomar_ordem_servico(ordem_id)
        
        return JSONResponse({"success": True})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)


@app.post("/ordens-servico/{ordem_id}/concluir", include_in_schema=False)
async def concluir_ordem_web(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Conclui uma ordem de serviço"""
    from crm_modules.ordens_servico.service import OrdemServicoService
    try:
        data = await request.json()
        observacoes = data.get('observacoes', None)
        
        service = OrdemServicoService(repository_session=db)
        service.concluir_ordem_servico(ordem_id, observacoes)
        
        return JSONResponse({"success": True})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)


@app.post("/ordens-servico/{ordem_id}/cancelar", include_in_schema=False)
async def cancelar_ordem_web(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Cancela uma ordem de serviço"""
    from crm_modules.ordens_servico.service import OrdemServicoService
    try:
        data = await request.json()
        motivo = data.get('motivo', '')
        
        if not motivo:
            return JSONResponse({"success": False, "message": "Motivo obrigatório"}, status_code=400)
        
        service = OrdemServicoService(repository_session=db)
        service.cancelar_ordem_servico(ordem_id, motivo)
        
        return JSONResponse({"success": True})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)


@app.get("/ordens-servico/{ordem_id}", response_class=HTMLResponse)
def detalhes_ordem_servico(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Exibe detalhes de uma ordem de serviço"""
    try:
        from crm_modules.ordens_servico.service import OrdemServicoService
        service = OrdemServicoService(repository_session=db)
        ordem = service.obter_ordem_servico(ordem_id)
        return templates.TemplateResponse("ordem_servico_detalhes.html", {"request": request, "ordem": ordem})
    except Exception as e:
        print(f"DEBUG: detalhes_ordem_servico error: {e}")
        return templates.TemplateResponse("ordens_servico.html", {"request": request, "error": str(e)})


@app.get("/ordens-servico/{ordem_id}/imprimir", response_class=HTMLResponse)
def imprimir_ordem_servico(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Imprime uma ordem de serviço"""
    try:
        from crm_modules.ordens_servico.service import OrdemServicoService
        from datetime import datetime
        service = OrdemServicoService(repository_session=db)
        ordem = service.obter_ordem_servico(ordem_id)
        return templates.TemplateResponse("ordem_servico_impressao.html", {
            "request": request, 
            "ordem": ordem,
            "now": datetime.now()
        })
    except Exception as e:
        return HTMLResponse(content=f"Erro ao gerar impressão: {str(e)}", status_code=400)


@app.get("/ordens-servico/{ordem_id}/editar", response_class=HTMLResponse)
def editar_ordem_form(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Formulário de edição de ordem de serviço"""
    try:
        from crm_modules.ordens_servico.service import OrdemServicoService
        from crm_modules.clientes.service import ClienteService
        service = OrdemServicoService(repository_session=db)
        ordem = service.obter_ordem_servico(ordem_id)
        
        # Buscar lista de clientes para o dropdown
        cliente_service = ClienteService(repository_session=db)
        clientes = cliente_service.listar_clientes()
        
        return templates.TemplateResponse("ordem_servico_editar.html", {
            "request": request,
            "ordem": ordem,
            "clientes": clientes
        })
    except Exception as e:
        print(f"DEBUG: editar_ordem error: {e}")
        return templates.TemplateResponse("ordens_servico.html", {"request": request, "error": str(e)})


@app.post("/ordens-servico", response_class=HTMLResponse)
async def criar_ordem_servico(request: Request, db: Session = Depends(get_db)):
    """Cria uma nova ordem de serviço"""
    from crm_modules.ordens_servico.service import OrdemServicoService
    from crm_modules.ordens_servico.schemas import OrdemServicoCreate
    try:
        form_data = await request.form()
        ordem_data = {
            "cliente_id": int(form_data.get("cliente_id")),
            "tipo_servico": form_data.get("tipo_servico"),
            "titulo": form_data.get("titulo"),
            "descricao": form_data.get("descricao"),
            "prioridade": form_data.get("prioridade"),
            "data_agendamento": form_data.get("data_agendamento") or None,
            "tecnico_responsavel": form_data.get("tecnico_responsavel") or None,
        }
        
        service = OrdemServicoService(repository_session=db)
        ordem_create = OrdemServicoCreate(**ordem_data)
        ordem = service.criar_ordem_servico(ordem_create)
        
        # Redirect to the new order details page
        from fastapi.responses import RedirectResponse
        return RedirectResponse(f"/ordens-servico/{ordem.id}", status_code=303)
    except Exception as e:
        print(f"DEBUG: criar_ordem_servico error: {e}")
        return templates.TemplateResponse("ordens_servico.html", {"request": request, "error": str(e)})


@app.post("/ordens-servico/{ordem_id}/editar")
async def atualizar_ordem_servico(ordem_id: int, request: Request, db: Session = Depends(get_db)):
    """Atualiza uma ordem de serviço"""
    from crm_modules.ordens_servico.service import OrdemServicoService
    from crm_modules.ordens_servico.schemas import OrdemServicoUpdate
    try:
        form_data = await request.form()
        update_data = OrdemServicoUpdate(
            tipo_servico=form_data.get("tipo_servico"),
            titulo=form_data.get("titulo"),
            descricao=form_data.get("descricao"),
            prioridade=form_data.get("prioridade"),
            data_agendamento=form_data.get("data_agendamento") or None,
            tecnico_responsavel=form_data.get("tecnico_responsavel") or None,
        )
        
        service = OrdemServicoService(repository_session=db)
        service.atualizar_ordem_servico(ordem_id, update_data)
        
        from fastapi.responses import RedirectResponse
        return RedirectResponse(f"/ordens-servico/{ordem_id}", status_code=303)
    except Exception as e:
        print(f"DEBUG: atualizar_ordem_servico error: {e}")
        return templates.TemplateResponse("ordem_servico_editar.html", {"request": request, "error": str(e)})


# ============================================
# CHECKLIST API ROUTES
# ============================================

@app.get("/api/v1/checklist/{ordem_servico_id}")
def get_checklist(ordem_servico_id: int, tipo_servico: str, db: Session = Depends(get_db)):
    """Busca o checklist completo de uma OS"""
    from crm_modules.ordens_servico.checklist_service import ChecklistService
    service = ChecklistService(session=db)
    
    # Buscar itens com progresso
    items = service.get_checklist_with_details(ordem_servico_id, tipo_servico)
    summary = service.get_progress_summary(ordem_servico_id)
    
    return {
        "ordem_servico_id": ordem_servico_id,
        "items": items,
        "summary": summary
    }


@app.post("/api/v1/checklist/{ordem_servico_id}/initialize")
def initialize_checklist(ordem_servico_id: int, tipo_servico: str, db: Session = Depends(get_db)):
    """Inicializa o checklist para uma OS"""
    from crm_modules.ordens_servico.checklist_service import ChecklistService
    service = ChecklistService(session=db)
    
    items = service.initialize_checklist(ordem_servico_id, tipo_servico)
    summary = service.get_progress_summary(ordem_servico_id)
    
    return {
        "success": True,
        "message": "Checklist inicializado",
        "summary": summary
    }


@app.post("/api/v1/checklist/{ordem_servico_id}/items/{item_id}/toggle")
def toggle_checklist_item(
    ordem_servico_id: int,
    item_id: int,
    completado_por: str = None,
    observacoes: str = None,
    db: Session = Depends(get_db)
):
    """Marca ou desmarca um item do checklist"""
    from crm_modules.ordens_servico.checklist_service import ChecklistService
    service = ChecklistService(session=db)
    
    try:
        item = service.toggle_item(ordem_servico_id, item_id, completado_por, observacoes)
        if item:
            summary = service.get_progress_summary(ordem_servico_id)
            return {"success": True, "summary": summary}
        return {"success": False, "message": "Item não encontrado"}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.get("/api/v1/checklist/{ordem_servico_id}/summary")
def get_checklist_summary(ordem_servico_id: int, db: Session = Depends(get_db)):
    """Busca apenas o resumo do progresso do checklist"""
    from crm_modules.ordens_servico.checklist_service import ChecklistService
    service = ChecklistService(session=db)
    summary = service.get_progress_summary(ordem_servico_id)
    return summary


@app.post("/api/v1/checklist/{ordem_servico_id}/items/{item_id}/check")
def check_checklist_item(
    ordem_servico_id: int,
    item_id: int,
    completado_por: str = None,
    observacoes: str = None,
    db: Session = Depends(get_db)
):
    """Marca um item do checklist como concluído"""
    from crm_modules.ordens_servico.checklist_service import ChecklistService
    service = ChecklistService(session=db)
    
    item = service.check_item(ordem_servico_id, item_id, completado_por, observacoes)
    if item:
        summary = service.get_progress_summary(ordem_servico_id)
        return {"success": True, "summary": summary}
    return {"success": False, "message": "Item não encontrado"}


@app.post("/api/v1/checklist/{ordem_servico_id}/items/{item_id}/uncheck")
def uncheck_checklist_item(ordem_servico_id: int, item_id: int, db: Session = Depends(get_db)):
    """Desmarca um item do checklist"""
    from crm_modules.ordens_servico.checklist_service import ChecklistService
    service = ChecklistService(session=db)
    
    item = service.uncheck_item(ordem_servico_id, item_id)
    if item:
        summary = service.get_progress_summary(ordem_servico_id)
        return {"success": True, "summary": summary}
    return {"success": False, "message": "Item não encontrado"}


@app.get("/api/v1/checklist/{ordem_servico_id}/is-complete")
def is_checklist_complete(ordem_servico_id: int, db: Session = Depends(get_db)):
    """Verifica se o checklist está completo"""
    from crm_modules.ordens_servico.checklist_service import ChecklistService
    service = ChecklistService(session=db)
    is_complete = service.is_checklist_completed(ordem_servico_id)
    return {"is_complete": is_complete}


# ============================================
# CARNES E BOLETOS - Routes
# ============================================

@app.get("/carnes", response_class=HTMLResponse)
def listar_carnes(request: Request, db: Session = Depends(get_db)):
    """Lista todos os carnês"""
    try:
        from crm_modules.faturamento.carne_service import CarneService
        service = CarneService(db)
        carnes = service.listar_carnes()
        return templates.TemplateResponse("carnes_boletos.html", {"request": request, "carnes": carnes})
    except Exception as e:
        return templates.TemplateResponse("carnes_boletos.html", {"request": request, "carnes": [], "error": str(e)})


@app.get("/carnes/{carne_id}/imprimir", response_class=HTMLResponse)
def imprimir_carne(carne_id: int, request: Request, db: Session = Depends(get_db)):
    """Imprime um carnê"""
    try:
        from crm_modules.faturamento.carne_models import CarneModel
        from sqlalchemy.orm import joinedload
        from datetime import datetime
        
        # Busca o modelo diretamente para ter acesso aos relacionamentos no template
        carne = db.query(CarneModel).options(
            joinedload(CarneModel.cliente),
            joinedload(CarneModel.parcelas)
        ).filter(CarneModel.id == carne_id).first()
        
        if not carne:
            return HTMLResponse(content=f"Carnê não encontrado: ID {carne_id}", status_code=404)
        
        return templates.TemplateResponse("carne_impressao.html", {
            "request": request,
            "carne": carne,
            "now": datetime.now()
        })
    except Exception as e:
        return HTMLResponse(content=f"Erro ao gerar impressão: {str(e)}", status_code=400)


# ============================================
# CONTRATOS - Routes
# ============================================

@app.get("/contratos", response_class=HTMLResponse)
def listar_contratos(request: Request):
    """Lista todos os contratos (simplificado)"""
    from crm_modules.contratos.service import ContratoService
    from crm_core.db.session import SessionLocal
    db = SessionLocal()
    try:
        service = ContratoService(db)
        contratos = service.listar_contratos()
        return templates.TemplateResponse("contratos.html", {"request": request, "contratos": contratos})
    except Exception as e:
        return templates.TemplateResponse("contratos.html", {"request": request, "contratos": [], "error": str(e)})
    finally:
        db.close()


@app.get("/contratos/{contrato_id}", response_class=HTMLResponse)
def detalhes_contrato(contrato_id: int, request: Request):
    """Exibe detalhes de um contrato"""
    from crm_modules.contratos.service import ContratoService
    from crm_core.db.session import SessionLocal
    db = SessionLocal()
    try:
        service = ContratoService(db)
        contrato = service.obter_contrato(contrato_id)
        if not contrato:
            return templates.TemplateResponse("contratos.html", {"request": request, "error": "Contrato não encontrado"})
        return templates.TemplateResponse("contrato_detalhes.html", {"request": request, "contrato": contrato})
    except Exception as e:
        return templates.TemplateResponse("contratos.html", {"request": request, "error": str(e)})
    finally:
        db.close()


@app.get("/contratos/{contrato_id}/imprimir", response_class=HTMLResponse)
def imprimir_contrato(contrato_id: int, request: Request):
    """Imprime um contrato"""
    from crm_modules.contratos.service import ContratoService
    from crm_core.db.session import SessionLocal
    from datetime import datetime
    db = SessionLocal()
    try:
        service = ContratoService(db)
        contrato = service.obter_contrato(contrato_id)
        if not contrato:
            return HTMLResponse(content="Contrato não encontrado", status_code=404)
        
        return templates.TemplateResponse("contrato_impressao.html", {
            "request": request,
            "contrato": contrato,
            "now": datetime.now()
        })
    except Exception as e:
        return HTMLResponse(content=f"Erro ao gerar impressão: {str(e)}", status_code=400)
    finally:
        db.close()


# ============================================
# RELATORIOS - Routes
# ============================================

@app.get("/relatorios/contratos", response_class=HTMLResponse)
def relatorios_contratos(request: Request):
    """Página de relatórios de contratos"""
    return templates.TemplateResponse("relatorios_contratos.html", {"request": request})


# ============================================
# FIM DAS ROTAS PRINCIPAIS
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=settings.debug)
'''

with open('interfaces/web/app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Arquivo app.py atualizado com sucesso!")
