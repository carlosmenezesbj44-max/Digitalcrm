from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from crm_core.security.auth_utils import decodificar_token
from crm_core.db.base import get_db_session
from crm_modules.usuarios.models import Usuario
from typing import List

# Rotas que não precisam de autenticação
ROTAS_PUBLICAS = [
    # Páginas HTML (GET requests) - deixar públicas, validação feita no client
    "/",
    "/login",
    "/registrar",
    "/clientes",
    "/clientes/novo",
    "/cliente/contratos",
    "/tecnicos",
    "/tecnicos/novo",
    "/produtos",
    "/produtos/novo",
    "/planos",
    "/planos/novo",
    "/ordens-servico",
    "/ordens-servico/nova",
    "/servidores",
    "/servidores/novo",
    "/usuarios",
    "/faturas",
    "/pagamentos",
    "/dashboard",
    "/contratos",
    "/contratos/novo",
    "/novo_cliente",
    "/novo_tecnico",
    "/novo_produto",
    "/novo_plano",
    "/novo_servidor",
    "/novo_contrato",
    "/configuracoes",
    "/boletos",
    "/carnes",
    # APIs de autenticação
    "/api/usuarios/registrar",
    "/api/usuarios/login",
    # Documentação e estáticos
    "/docs",
    "/openapi.json",
    "/redoc",
    "/static",
]

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware que valida token JWT em todas as requisições"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            # Verificar se a rota é pública
            is_public = self._eh_rota_publica(request.url.path)
            print(f"[AUTH] Path: {request.url.path}, Public: {is_public}, Method: {request.method}")
            if is_public:
                response = await call_next(request)
                print(f"[AUTH] Static response status: {response.status_code}")
                return response
            
            # Extrair token do header
            auth_header = request.headers.get("authorization")
            
            if not auth_header:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Credenciais nao fornecidas"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            try:
                scheme, token = auth_header.split()
                if scheme.lower() != "bearer":
                    raise ValueError()
            except ValueError:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Formato de token invalido"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Validar token
            payload = decodificar_token(token)
            if payload is None:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Token invalido ou expirado"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Verificar se usuário existe e está ativo
            db = get_db_session()
            try:
                usuario_id = payload.get("usuario_id")
                if not usuario_id:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Token invalido"},
                    )
                usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
                
                if not usuario or not usuario.ativo:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Usuario invalido ou inativo"},
                    )
                
                # Adicionar usuário ao request para uso nas rotas
                request.state.usuario = usuario
                
            finally:
                db.close()
            
            response = await call_next(request)
            return response
        except Exception as e:
            print(f"[AUTH ERROR] {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Erro interno: {str(e)}"},
            )
    
    @staticmethod
    def _eh_rota_publica(path: str) -> bool:
        """Verifica se a rota é pública"""
        return any(path.startswith(rota) for rota in ROTAS_PUBLICAS)
