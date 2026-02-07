from fastapi import APIRouter, Depends, HTTPException, Request
from crm_modules.faturamento.schemas import FaturaCreate, FaturaUpdate, PagamentoCreate, FaturaResponse, PagamentoResponse
from crm_modules.faturamento.service import FaturamentoService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

def _load_env_pix_config() -> dict:
    """Lê configurações PIX diretamente do .env para refletir mudanças sem restart."""
    try:
        env_path = Path(__file__).parent.parent.parent / '.env'
        data = {}
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        data[key.strip()] = value.strip()
        return {
            "PIX_CHAVE": data.get("PIX_CHAVE", os.getenv("PIX_CHAVE", "")),
            "PIX_TIPO_CHAVE": data.get("PIX_TIPO_CHAVE", os.getenv("PIX_TIPO_CHAVE", "cpf")),
            "PIX_BENEFICIARIO": data.get("PIX_BENEFICIARIO", os.getenv("PIX_BENEFICIARIO", "CRM PROVEDOR")),
            "PIX_CIDADE": data.get("PIX_CIDADE", os.getenv("PIX_CIDADE", "SAO PAULO")),
        }
    except Exception:
        return {
            "PIX_CHAVE": os.getenv("PIX_CHAVE", ""),
            "PIX_TIPO_CHAVE": os.getenv("PIX_TIPO_CHAVE", "cpf"),
            "PIX_BENEFICIARIO": os.getenv("PIX_BENEFICIARIO", "CRM PROVEDOR"),
            "PIX_CIDADE": os.getenv("PIX_CIDADE", "SAO PAULO"),
        }


@router.post("/faturas/", response_model=FaturaResponse)
def criar_fatura(fatura: FaturaCreate, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    try:
        return service.criar_fatura(fatura)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/faturas/", response_model=List[FaturaResponse])
def listar_faturas(db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    return service.listar_todas_faturas()


@router.get("/faturas/{fatura_id}", response_model=FaturaResponse)
def obter_fatura(fatura_id: int, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    try:
        return service.obter_fatura(fatura_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/faturas/{fatura_id}", response_model=FaturaResponse)
def atualizar_fatura(fatura_id: int, fatura: FaturaUpdate, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    try:
        return service.atualizar_fatura(fatura_id, fatura)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/faturas/cliente/{cliente_id}", response_model=List[FaturaResponse])
def listar_faturas_cliente(cliente_id: int, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    return service.listar_faturas_cliente(cliente_id)


@router.get("/pagamentos/", response_model=List[PagamentoResponse])
def listar_pagamentos(db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    return service.listar_todos_pagamentos()


@router.post("/pagamentos/", response_model=PagamentoResponse)
def registrar_pagamento(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    try:
        return service.registrar_pagamento(pagamento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/faturas/gerar-mensal/{mes}/{ano}")
def gerar_faturas_mensais(mes: int, ano: int, cliente_id: int = None, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    try:
        if cliente_id:
            # Gerar fatura para cliente específico
            fatura = service.gerar_fatura_cliente(cliente_id, mes, ano)
            return {"message": f"Fatura gerada para cliente {cliente_id}", "faturas": [fatura.id] if fatura else []}
        else:
            # Gerar faturas para todos os clientes
            faturas = service.gerar_faturas_mensais(mes, ano)
            return {"message": f"{len(faturas)} faturas geradas", "faturas": [f.id for f in faturas]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/relatorios/faturas-pendentes")
def relatorio_faturas_pendentes(db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    # Simple report: count pending invoices
    pendentes = len(service.repository.get_faturas_pendentes())
    return {"faturas_pendentes": pendentes}


@router.get("/faturas/{fatura_id}/imprimir")
def imprimir_fatura(fatura_id: int, request: Request, db: Session = Depends(get_db)):
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    import os
    from datetime import datetime

    service = FaturamentoService(repository_session=db)
    try:
        fatura = service.obter_fatura_detalhada(fatura_id)
        
        # Carregar configurações da empresa para o template
        pix_config = _load_env_pix_config()
        config = {
            "COMPANY_NAME": os.getenv("COMPANY_NAME", "CRM PROVEDOR"),
            "COMPANY_CNPJ": os.getenv("COMPANY_CNPJ", ""),
            "COMPANY_LOGO": os.getenv("COMPANY_LOGO", ""),
            "COMPANY_TELEFONE": os.getenv("COMPANY_TELEFONE", ""),
            "COMPANY_EMAIL": os.getenv("COMPANY_EMAIL", ""),
            "COMPANY_ENDERECO": os.getenv("COMPANY_ENDERECO", ""),
            "BOLETO_JUROS_PADRAO": os.getenv("BOLETO_JUROS_PADRAO", "2,00"),
            "BOLETO_MULTA_PADRAO": os.getenv("BOLETO_MULTA_PADRAO", "1,00"),
            **pix_config,
        }
        
        templates = Jinja2Templates(directory="interfaces/web/templates")
        return templates.TemplateResponse(
            "fatura_impressao.html", 
            {
                "request": request, 
                "fatura": fatura,
                "config": config,
                "now": datetime.now
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/faturas/{fatura_id}/enviar-email")
def enviar_fatura_email(fatura_id: int, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    try:
        # For now, just a mock success
        return {"message": "Fatura enviada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/faturas/{fatura_id}/marcar-paga")
def marcar_fatura_paga(fatura_id: int, db: Session = Depends(get_db)):
    service = FaturamentoService(repository_session=db)
    try:
        fatura = service.marcar_fatura_paga(fatura_id)
        return fatura
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
