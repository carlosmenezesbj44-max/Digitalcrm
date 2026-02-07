from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from crm_core.config.settings import settings

from crm_core.db.base import get_db
from sqlalchemy.orm import Session
from crm_modules.usuarios.api import router as usuarios_router

app = FastAPI(title="CRM Provedor Web", version="1.0.0")
app.include_router(usuarios_router)

# Include servidores API routes
from crm_modules.servidores.api import router as servidores_router
app.include_router(servidores_router, prefix="/api/v1/servidores")

# Include clientes API routes
from crm_modules.clientes.api import router as clientes_router
app.include_router(clientes_router)

# Include planos API routes
from crm_modules.planos.api import router as planos_router
app.include_router(planos_router, prefix="/api/v1/planos")

# Include MikroTik API routes
from crm_modules.mikrotik.api import router as mikrotik_router
# Remove prefix duplicate since router already has /mikrotik prefix
app.include_router(mikrotik_router, prefix="/api/v1")

# Include Faturamento API routes
from crm_modules.faturamento.carne_api import router as faturamento_router
app.include_router(faturamento_router, prefix="/api/v1")

from crm_modules.faturamento.api import router as faturamento_main_router
app.include_router(faturamento_main_router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="interfaces/web/static"), name="static")
templates = Jinja2Templates(directory="interfaces/web/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "CRM Provedor"})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/registrar", response_class=HTMLResponse)
async def registrar_page(request: Request):
    return templates.TemplateResponse("registrar.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/servidores", response_class=HTMLResponse)
async def servidores(request: Request, db: Session = Depends(get_db)):
    from crm_modules.servidores.service import ServidorService
    service = ServidorService(repository_session=db)
    servidores = service.listar_servidores_ativos()
    return templates.TemplateResponse("servidores.html", {"request": request, "servidores": servidores})


@app.get("/servidores/novo", response_class=HTMLResponse)
async def novo_servidor_form(request: Request):
    return templates.TemplateResponse("novo_servidor.html", {"request": request})


@app.post("/servidores/novo")
async def criar_servidor(request: Request, db: Session = Depends(get_db)):
    from crm_modules.servidores.service import ServidorService
    from crm_modules.servidores.schemas import ServidorCreate
    
    try:
        form_data = await request.form()
        servidor_data = ServidorCreate(
            nome=form_data.get("nome"),
            ip=form_data.get("ip"),
            tipo_conexao=form_data.get("tipo_conexao"),
            tipo_acesso=form_data.get("tipo_acesso"),
            usuario=form_data.get("usuario"),
            senha=form_data.get("senha"),
            alterar_nome=form_data.get("alterar_nome") == "sim",
            ativo=True
        )
        
        service = ServidorService(repository_session=db)
        servidor = service.criar_servidor(servidor_data)
        
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/servidores", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("novo_servidor.html", {"request": request, "error": str(e)})


@app.get("/servidores/{servidor_id}/editar", response_class=HTMLResponse)
async def editar_servidor_form(servidor_id: int, request: Request, db: Session = Depends(get_db)):
    from crm_modules.servidores.service import ServidorService
    service = ServidorService(repository_session=db)
    servidor = service.obter_servidor(servidor_id)
    return templates.TemplateResponse("novo_servidor.html", {"request": request, "servidor": servidor})


@app.post("/servidores/{servidor_id}/editar")
async def atualizar_servidor(servidor_id: int, request: Request, db: Session = Depends(get_db)):
    from crm_modules.servidores.service import ServidorService
    from crm_modules.servidores.schemas import ServidorUpdate
    
    try:
        form_data = await request.form()
        servidor_data = ServidorUpdate(
            nome=form_data.get("nome"),
            ip=form_data.get("ip"),
            tipo_conexao=form_data.get("tipo_conexao"),
            tipo_acesso=form_data.get("tipo_acesso"),
            usuario=form_data.get("usuario"),
            senha=form_data.get("senha"),
            alterar_nome=form_data.get("alterar_nome") == "sim",
            ativo=form_data.get("ativo") == "sim"
        )
        
        service = ServidorService(repository_session=db)
        service.atualizar_servidor(servidor_id, servidor_data)
        
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/servidores", status_code=303)
    except Exception as e:
        from crm_modules.servidores.service import ServidorService
        service = ServidorService(repository_session=db)
        servidor = service.obter_servidor(servidor_id)
        return templates.TemplateResponse("novo_servidor.html", {"request": request, "servidor": servidor, "error": str(e)})


@app.post("/servidores/{servidor_id}/excluir")
async def excluir_servidor(servidor_id: int, db: Session = Depends(get_db)):
    from crm_modules.servidores.service import ServidorService
    try:
        service = ServidorService(repository_session=db)
        service.desativar_servidor(servidor_id)
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.post("/servidores/{servidor_id}/testar-conexao")
async def testar_conexao(servidor_id: int, db: Session = Depends(get_db)):
    from crm_modules.servidores.service import ServidorService
    try:
        service = ServidorService(repository_session=db)
        result = service.testar_conexao(servidor_id)
        return result
    except Exception as e:
        return {"success": False, "message": str(e)}


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


@app.get("/planos", response_class=HTMLResponse)
def listar_planos(request: Request, db: Session = Depends(get_db)):
    """Exibe página de listagem de planos"""
    from crm_modules.planos.service import PlanoService
    service = PlanoService(repository_session=db)
    planos = service.listar_planos_ativos()
    return templates.TemplateResponse("planos.html", {"request": request, "planos": planos})


@app.get("/planos/novo", response_class=HTMLResponse)
def novo_plano_form(request: Request):
    """Exibe formulário para criar novo plano"""
    return templates.TemplateResponse("novo_plano.html", {"request": request})


@app.post("/planos/novo")
async def criar_plano(request: Request, db: Session = Depends(get_db)):
    """Cria um novo plano"""
    from crm_modules.planos.service import PlanoService
    from crm_modules.planos.schemas import PlanoCreate
    
    try:
        form_data = await request.form()
        plano_data = PlanoCreate(
            nome=form_data.get("nome"),
            velocidade_download=int(form_data.get("velocidade_download")),
            velocidade_upload=int(form_data.get("velocidade_upload")),
            valor_mensal=float(form_data.get("valor_mensal")),
            descricao=form_data.get("descricao"),
            ativo=True
        )
        
        service = PlanoService(repository_session=db)
        service.criar_plano(plano_data)
        
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/planos", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("novo_plano.html", {"request": request, "error": str(e)})


@app.get("/planos/{plano_id}/editar", response_class=HTMLResponse)
def editar_plano_form(plano_id: int, request: Request, db: Session = Depends(get_db)):
    """Exibe formulário para editar plano"""
    from crm_modules.planos.service import PlanoService
    service = PlanoService(repository_session=db)
    plano = service.obter_plano(plano_id)
    return templates.TemplateResponse("novo_plano.html", {"request": request, "plano": plano})


@app.post("/planos/{plano_id}/editar")
async def atualizar_plano(plano_id: int, request: Request, db: Session = Depends(get_db)):
    """Atualiza um plano"""
    from crm_modules.planos.service import PlanoService
    from crm_modules.planos.schemas import PlanoUpdate
    
    try:
        form_data = await request.form()
        plano_data = PlanoUpdate(
            nome=form_data.get("nome"),
            velocidade_download=int(form_data.get("velocidade_download")),
            velocidade_upload=int(form_data.get("velocidade_upload")),
            valor_mensal=float(form_data.get("valor_mensal")),
            descricao=form_data.get("descricao"),
            ativo=form_data.get("ativo") == "sim"
        )
        
        service = PlanoService(repository_session=db)
        service.atualizar_plano(plano_id, plano_data)
        
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/planos", status_code=303)
    except Exception as e:
        from crm_modules.planos.service import PlanoService
        service = PlanoService(repository_session=db)
        plano = service.obter_plano(plano_id)
        return templates.TemplateResponse("novo_plano.html", {"request": request, "plano": plano, "error": str(e)})


@app.post("/planos/{plano_id}/deletar")
async def desativar_plano(plano_id: int, db: Session = Depends(get_db)):
    """Desativa um plano"""
    from crm_modules.planos.service import PlanoService
    try:
        service = PlanoService(repository_session=db)
        service.desativar_plano(plano_id)
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.get("/minha-conta", response_class=HTMLResponse)
def minha_conta(request: Request):
    """Exibe página de perfil do usuário"""
    return templates.TemplateResponse("minha_conta.html", {"request": request})


@app.get("/mikrotik/logs", response_class=HTMLResponse)
def mikrotik_logs(request: Request):
    """Exibe página de logs do MikroTik"""
    return templates.TemplateResponse("mikrotik_logs.html", {"request": request})


@app.get("/mikrotik/sessions", response_class=HTMLResponse)
def mikrotik_sessions(request: Request):
    """Exibe página de sessões do MikroTik"""
    return templates.TemplateResponse("mikrotik_sessions.html", {"request": request})


@app.get("/api/clientes/search")
async def buscar_clientes_api(q: str, db: Session = Depends(get_db)):
    """Busca clientes por nome, email ou telefone (API para autocomplete)"""
    from crm_modules.clientes.service import ClienteService
    service = ClienteService(repository_session=db)
    clientes = service.buscar_clientes(q)
    return [{"id": cliente.id, "nome": cliente.nome, "email": cliente.email} for cliente in clientes]


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
        return templates.TemplateResponse("carnes.html", {"request": request, "carnes": carnes})
    except Exception as e:
        return templates.TemplateResponse("carnes.html", {"request": request, "carnes": [], "error": str(e)})


@app.get("/carnes/{carne_id}/imprimir", response_class=HTMLResponse)
def imprimir_carne(carne_id: int, request: Request, db: Session = Depends(get_db)):
    """Imprime um carnê"""
    try:
        from crm_modules.faturamento.carne_models import CarneModel
        from sqlalchemy.orm import joinedload
        from datetime import datetime
        from crm_core.config.settings import settings

        # Busca o modelo diretamente para ter acesso aos relacionamentos no template
        carne = db.query(CarneModel).options(
            joinedload(CarneModel.cliente),
            joinedload(CarneModel.parcelas)
        ).filter(CarneModel.id == carne_id).first()

        if not carne:
            return HTMLResponse(content=f"Carnê não encontrado: ID {carne_id}", status_code=404)

        # Configuração para o template
        config = {
            "PIX_CHAVE": settings.pix_chave or "",
            "PIX_TIPO_CHAVE": settings.pix_tipo_chave or "cpf",
            "PIX_BENEFICIARIO": settings.pix_beneficiario or "CRM Provedor",
            "PIX_CIDADE": settings.pix_cidade or "São Paulo"
        }

        return templates.TemplateResponse("carne_impressao.html", {
            "request": request,
            "carne": carne,
            "now": datetime.now(),
            "config": config
        })
    except Exception as e:
        return HTMLResponse(content=f"Erro ao gerar impressão: {str(e)}", status_code=400)


@app.get("/faturas", response_class=HTMLResponse)
def listar_faturas(request: Request, db: Session = Depends(get_db)):
    """Lista todas as faturas"""
    try:
        from crm_modules.faturamento.service import FaturamentoService
        service = FaturamentoService(repository_session=db)
        faturas = service.listar_todas_faturas()
        return templates.TemplateResponse("faturas.html", {"request": request, "faturas": faturas})
    except Exception as e:
        return templates.TemplateResponse("faturas.html", {"request": request, "faturas": [], "error": str(e)})


@app.get("/faturas/{fatura_id}", response_class=HTMLResponse)
def detalhes_fatura(fatura_id: int, request: Request, db: Session = Depends(get_db)):
    """Exibe detalhes de uma fatura"""
    try:
        from crm_modules.faturamento.service import FaturamentoService
        service = FaturamentoService(repository_session=db)
        fatura = service.obter_fatura_detalhada(fatura_id)
        if not fatura:
            return templates.TemplateResponse("faturas.html", {"request": request, "error": "Fatura não encontrada"})
        return templates.TemplateResponse("fatura_detalhes.html", {"request": request, "fatura": fatura})
    except Exception as e:
        return templates.TemplateResponse("faturas.html", {"request": request, "error": str(e)})


@app.get("/boletos", response_class=HTMLResponse)
def listar_boletos(request: Request, db: Session = Depends(get_db)):
    """Lista todos os boletos"""
    try:
        from crm_modules.faturamento.boleto_service import BoletoService
        service = BoletoService(db)
        boletos = service.listar_todos_boletos()
        return templates.TemplateResponse("boletos.html", {"request": request, "boletos": boletos})
    except Exception as e:
        return templates.TemplateResponse("boletos.html", {"request": request, "boletos": [], "error": str(e)})


@app.get("/pagamentos", response_class=HTMLResponse)
def listar_pagamentos(request: Request, db: Session = Depends(get_db)):
    """Lista todos os pagamentos"""
    try:
        from crm_modules.faturamento.service import FaturamentoService
        service = FaturamentoService(repository_session=db)
        pagamentos = service.listar_todos_pagamentos()
        return templates.TemplateResponse("pagamentos.html", {"request": request, "pagamentos": pagamentos})
    except Exception as e:
        return templates.TemplateResponse("pagamentos.html", {"request": request, "pagamentos": [], "error": str(e)})


# ============================================
# CONTRATOS - Routes
# ============================================

@app.get("/contratos", response_class=HTMLResponse)
def listar_contratos(request: Request, db: Session = Depends(get_db)):
    """Lista todos os contratos (simplificado)"""
    from crm_modules.contratos.service import ContratoService
    try:
        service = ContratoService(repository_session=db)
        contratos = service.listar_todos_contratos()
        stats = service.obter_estatisticas_contratos()
        return templates.TemplateResponse("contratos.html", {"request": request, "contratos": contratos, "stats": stats})
    except Exception as e:
        return templates.TemplateResponse("contratos.html", {"request": request, "contratos": [], "error": str(e), "stats": {"total": 0, "aguardando": 0, "assinado": 0, "liberado": 0, "vencendo_30_dias": 0, "vencidos": 0}})


@app.get("/contratos/novo", response_class=HTMLResponse)
def novo_contrato_form(request: Request, db: Session = Depends(get_db)):
    """Exibe formulário para criar novo contrato"""
    from crm_modules.clientes.service import ClienteService
    cliente_service = ClienteService(repository_session=db)
    clientes = cliente_service.listar_clientes_ativos()
    return templates.TemplateResponse("novo_contrato.html", {"request": request, "clientes": clientes})


@app.post("/contratos/novo")
async def criar_contrato(request: Request, db: Session = Depends(get_db)):
    """Cria um novo contrato"""
    from crm_modules.contratos.service import ContratoService
    from crm_modules.contratos.schemas import ContratoCreate
    try:
        form_data = await request.form()
        contrato_data = ContratoCreate(
            titulo=form_data.get("titulo"),
            descricao=form_data.get("descricao"),
            cliente_id=int(form_data.get("cliente_id")),
            tipo_contrato=form_data.get("tipo_contrato"),
            data_vigencia_inicio=form_data.get("data_vigencia_inicio"),
            data_vigencia_fim=form_data.get("data_vigencia_fim"),
            valor_contrato=float(form_data.get("valor_contrato")) if form_data.get("valor_contrato") else None,
            moeda=form_data.get("moeda"),
            observacoes=form_data.get("observacoes"),
            incluir_pdf=form_data.get("incluir_pdf") == "true"
        )
        service = ContratoService(repository_session=db)
        service.criar_contrato(contrato_data)
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/contratos", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("novo_contrato.html", {"request": request, "error": str(e)})


@app.get("/contratos/{contrato_id}/imprimir", response_class=HTMLResponse)
def imprimir_contrato(contrato_id: int, request: Request, db: Session = Depends(get_db)):
    """Imprime um contrato"""
    from crm_modules.contratos.service import ContratoService
    from datetime import datetime
    try:
        service = ContratoService(repository_session=db)
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


@app.get("/contratos/{contrato_id}/editar", response_class=HTMLResponse)
def editar_contrato_form(contrato_id: int, request: Request, db: Session = Depends(get_db)):
    """Exibe formulário para editar contrato"""
    from crm_modules.contratos.service import ContratoService
    try:
        service = ContratoService(repository_session=db)
        contrato = service.obter_contrato(contrato_id)
        if not contrato:
            return templates.TemplateResponse("contratos.html", {"request": request, "error": "Contrato não encontrado"})
        return templates.TemplateResponse("novo_contrato.html", {"request": request, "contrato": contrato})
    except Exception as e:
        return templates.TemplateResponse("contratos.html", {"request": request, "error": str(e)})


@app.post("/contratos/{contrato_id}/editar")
async def atualizar_contrato(contrato_id: int, request: Request, db: Session = Depends(get_db)):
    """Atualiza um contrato"""
    from crm_modules.contratos.service import ContratoService
    from crm_modules.contratos.schemas import ContratoUpdate
    try:
        form_data = await request.form()
        contrato_data = ContratoUpdate(
            titulo=form_data.get("titulo"),
            descricao=form_data.get("descricao"),
            valor_contrato=float(form_data.get("valor_contrato")) if form_data.get("valor_contrato") else None,
            moeda=form_data.get("moeda"),
            data_vigencia_inicio=form_data.get("data_vigencia_inicio"),
            data_vigencia_fim=form_data.get("data_vigencia_fim"),
            observacoes=form_data.get("observacoes")
        )
        service = ContratoService(repository_session=db)
        service.atualizar_contrato(contrato_id, contrato_data)
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/contratos", status_code=303)
    except Exception as e:
        from crm_modules.contratos.service import ContratoService
        service = ContratoService(repository_session=db)
        contrato = service.obter_contrato(contrato_id)
        return templates.TemplateResponse("novo_contrato.html", {"request": request, "contrato": contrato, "error": str(e)})


@app.get("/contratos/{contrato_id}/pdf")
def gerar_pdf_contrato(contrato_id: int, db: Session = Depends(get_db)):
    """Gera PDF do contrato"""
    from crm_modules.contratos.service import ContratoService
    try:
        service = ContratoService(repository_session=db)
        pdf_bytes = service.gerar_pdf_contrato(contrato_id)
        from fastapi.responses import Response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=contrato_{contrato_id}.pdf"}
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/contratos/{contrato_id}/detalhes", response_class=JSONResponse)
def obter_detalhes_contrato_json(contrato_id: int, db: Session = Depends(get_db)):
    """Obtém detalhes de um contrato em formato JSON"""
    from crm_modules.contratos.service import ContratoService
    from crm_modules.contratos.service import ContratoService
    try:
        service = ContratoService(repository_session=db)
        contrato = service.obter_contrato(contrato_id)
        if not contrato:
            return JSONResponse({"error": "Contrato não encontrado"}, status_code=404)
        
        # Converter contrato para dicionário
        contrato_dict = {
            "id": contrato.id,
            "titulo": contrato.titulo,
            "cliente_id": contrato.cliente_id,
            "tipo_contrato": contrato.tipo_contrato.value if hasattr(contrato.tipo_contrato, "value") else contrato.tipo_contrato,
            "status_assinatura": contrato.status_assinatura.value if hasattr(contrato.status_assinatura, "value") else contrato.status_assinatura,
            "data_criacao": contrato.data_criacao.isoformat() if contrato.data_criacao else None,
            "data_assinatura": contrato.data_assinatura.isoformat() if contrato.data_assinatura else None,
            "data_vigencia_inicio": contrato.data_vigencia_inicio.isoformat() if contrato.data_vigencia_inicio else None,
            "data_vigencia_fim": contrato.data_vigencia_fim.isoformat() if contrato.data_vigencia_fim else None,
            "valor_contrato": contrato.valor_contrato,
            "moeda": contrato.moeda,
            "descricao": contrato.descricao,
            "observacoes": contrato.observacoes
        }
        
        return JSONResponse(contrato_dict)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/contratos/{contrato_id}", response_class=HTMLResponse)
def detalhes_contrato(contrato_id: int, request: Request, db: Session = Depends(get_db)):
    """Exibe detalhes de um contrato"""
    from crm_modules.contratos.service import ContratoService
    try:
        service = ContratoService(repository_session=db)
        contrato = service.obter_contrato(contrato_id)
        if not contrato:
            return templates.TemplateResponse("contratos.html", {"request": request, "error": "Contrato não encontrado"})
        return templates.TemplateResponse("contrato_detalhes.html", {"request": request, "contrato": contrato})
    except Exception as e:
        return templates.TemplateResponse("contratos.html", {"request": request, "error": str(e)})


# ============================================
# RELATORIOS - Routes
# ============================================

@app.get("/relatorios/contratos", response_class=HTMLResponse)
def relatorios_contratos(request: Request, db: Session = Depends(get_db)):
    """Página de relatórios de contratos"""
    try:
        from crm_modules.contratos.service import ContratoService
        service = ContratoService(repository_session=db)
        contratos = service.listar_todos_contratos()
        
        # Calcular estatísticas
        stats = {
            "total": len(contratos),
            "aguardando": len([c for c in contratos if c.status_assinatura == "pendente"]),
            "assinado": len([c for c in contratos if c.status_assinatura == "assinado"]),
            "liberado": len([c for c in contratos if c.status_assinatura == "liberado"]),
            "vencendo_30_dias": 0,
            "vencidos": 0
        }
        
        # Contratos recentes (últimos 30 dias)
        from datetime import datetime, timedelta
        hoje = datetime.now()
        data_limite = hoje - timedelta(days=30)
        contratos_recentes = [c for c in contratos if c.data_criacao and c.data_criacao > data_limite]
        
        return templates.TemplateResponse("relatorios_contratos.html", {
            "request": request,
            "stats": stats,
            "contratos_recentes": contratos_recentes
        })
    except Exception as e:
        print(f"Erro ao carregar relatório de contratos: {e}")
        return templates.TemplateResponse("relatorios_contratos.html", {
            "request": request,
            "stats": {"total": 0, "aguardando": 0, "assinado": 0, "liberado": 0, "vencendo_30_dias": 0, "vencidos": 0},
            "contratos_recentes": []
        })


@app.get("/relatorios/clientes", response_class=HTMLResponse)
def relatorios_clientes(request: Request, db: Session = Depends(get_db)):
    """Página de relatórios de clientes"""
    try:
        from crm_modules.clientes.service import ClienteService
        service = ClienteService(repository_session=db)
        clientes = service.listar_clientes()
        
        # Calcular estatísticas
        stats = {
            "total": len(clientes),
            "ativos": len([c for c in clientes if c.ativo]),
            "inativos": len([c for c in clientes if not c.ativo]),
            "novos_mes": 0,
            "cancelados_mes": 0,
            "receita_mensal": 0,
            "clientes_urbanos": 0,
            "clientes_rurais": 0
        }
        
        # Clientes recentes (últimos 30 dias)
        from datetime import datetime, timedelta
        hoje = datetime.now()
        data_limite = hoje - timedelta(days=30)
        clientes_recentes = [c for c in clientes if c.data_criacao and c.data_criacao > data_limite]
        
        return templates.TemplateResponse("relatorios_clientes.html", {
            "request": request,
            "stats": stats,
            "clientes_recentes": clientes_recentes
        })
    except Exception as e:
        print(f"Erro ao carregar relatório de clientes: {e}")
        return templates.TemplateResponse("relatorios_clientes.html", {
            "request": request,
            "stats": {"total": 0, "ativos": 0, "inativos": 0, "novos_mes": 0, "cancelados_mes": 0, "receita_mensal": 0, "clientes_urbanos": 0, "clientes_rurais": 0},
            "clientes_recentes": []
        })


# ============================================
# FIM DAS ROTAS PRINCIPAIS
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=settings.debug)