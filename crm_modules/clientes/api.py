from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from crm_modules.clientes.schemas import ClienteCreate, ClienteUpdate, Cliente, ClienteArquivo
from crm_modules.clientes.service import ClienteService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session
import io

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"])


@router.post("/", response_model=Cliente)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    service = ClienteService(repository_session=db)
    try:
        return service.criar_cliente(cliente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search")
def buscar_clientes(q: str = "", db: Session = Depends(get_db)):
    service = ClienteService(repository_session=db)
    try:
        clientes = service.buscar_clientes_por_nome(q)
        return [
            {
                "id": c.id, 
                "nome": c.nome, 
                "valor_mensal": getattr(c, 'valor_mensal', 0),
                "dia_vencimento": getattr(c, 'dia_vencimento', None)
            } for c in clientes
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{cliente_id}", response_model=Cliente)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(repository_session=db)
    try:
        return service.obter_cliente(cliente_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    service = ClienteService(repository_session=db)
    try:
        return service.atualizar_cliente(cliente_id, cliente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{cliente_id}")
def desativar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(repository_session=db)
    try:
        service.desativar_cliente(cliente_id)
        return {"message": "Cliente desativado"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def listar_clientes_ativos(
    q: str = "",
    status: str = "",
    page: int = 1,
    per_page: int = 50,
    export: str = "",
    db: Session = Depends(get_db)
):
    service = ClienteService(repository_session=db)
    try:
        clientes, total = service.listar_clientes_filtrados(q, status, page, per_page)
        
        # Formata os clientes para incluir os campos necessários, garantindo que valor_mensal e dia_vencimento existam
        clientes_formatados = []
        for c in clientes:
            clientes_formatados.append({
                "id": c.id,
                "nome": c.nome,
                "email": c.email,
                "telefone": c.telefone,
                "cpf": c.cpf,
                "endereco": c.endereco,
                "valor_mensal": getattr(c, 'valor_mensal', 0) or 0,
                "dia_vencimento": getattr(c, 'dia_vencimento', None),
                "status_contrato": getattr(c, 'status_contrato', 'nenhum'),
                "data_cadastro": c.data_cadastro
            })

        if export == "csv":
            # Return CSV data for export
            import csv
            from fastapi.responses import Response

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['ID', 'Nome', 'Email', 'Telefone', 'CPF', 'Endereço', 'Status', 'Data Cadastro'])

            for cliente in clientes:
                writer.writerow([
                    cliente.id,
                    cliente.nome,
                    cliente.email,
                    cliente.telefone,
                    cliente.cpf,
                    cliente.endereco,
                    cliente.status_contrato or "nenhum",
                    cliente.data_cadastro.strftime("%d/%m/%Y") if cliente.data_cadastro else "N/A"
                ])

            return Response(
                content=output.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=clientes.csv"}
            )

        return {
            "clientes": clientes_formatados,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{cliente_id}/arquivos", response_model=ClienteArquivo)
async def upload_arquivo(
    cliente_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    service = ClienteService(repository_session=db)
    try:
        content = await file.read()
        return service.upload_arquivo_cliente(cliente_id, content, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{cliente_id}/arquivos", response_model=List[ClienteArquivo])
def listar_arquivos(cliente_id: int, db: Session = Depends(get_db)):
    service = ClienteService(repository_session=db)
    try:
        return service.listar_arquivos(cliente_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/arquivos/{arquivo_id}")
def excluir_arquivo(arquivo_id: int, db: Session = Depends(get_db)):
    service = ClienteService(repository_session=db)
    try:
        service.excluir_arquivo(arquivo_id)
        return {"message": "Arquivo excluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{cliente_id}/foto-casa")
async def upload_foto_casa(
    cliente_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    service = ClienteService(repository_session=db)
    try:
        content = await file.read()
        url = service.upload_foto_casa(cliente_id, content, file.filename)
        return {"foto_casa_url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


