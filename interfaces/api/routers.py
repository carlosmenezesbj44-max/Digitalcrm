from fastapi import APIRouter
from crm_modules.clientes.api import router as clientes_router
from crm_modules.ordens_servico.api import router as ordens_servico_router
from crm_modules.configuracoes.api import router as configuracoes_router
from crm_modules.planos.api import router as planos_router
from crm_modules.produtos.api import router as produtos_router
from crm_modules.faturamento.api import router as faturamento_router

api_router = APIRouter()
api_router.include_router(clientes_router, prefix="/clientes", tags=["clientes"])
api_router.include_router(ordens_servico_router, prefix="/ordens-servico", tags=["ordens-servico"])
api_router.include_router(configuracoes_router, prefix="/configuracoes", tags=["configuracoes"])
api_router.include_router(planos_router, prefix="/planos", tags=["planos"])
api_router.include_router(produtos_router, prefix="/produtos", tags=["produtos"])
api_router.include_router(faturamento_router, prefix="/faturamento", tags=["faturamento"])
