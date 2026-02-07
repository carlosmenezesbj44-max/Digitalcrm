from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any
import os
import shutil
from pathlib import Path
from crm_core.security.dependencies import obter_usuario_admin
from crm_core.db.base import get_db

router = APIRouter(prefix="/api/v1/configuracoes", tags=["configuracoes"])

@router.get("/")
async def get_configurations(current_user = Depends(obter_usuario_admin)) -> Dict[str, Any]:
    """
    Obter todas as configurações do sistema lendo diretamente do arquivo .env
    """
    try:
        # Caminho do arquivo .env
        env_path = Path(__file__).parent.parent.parent / '.env'
        
        # Carregar configurações do .env manualmente para evitar cache do os.getenv
        config = {}
        
        # Valores padrão
        defaults = {
            'GERENCIANET_SANDBOX': 'true',
            'PIX_TIPO_CHAVE': 'cpf'
        }
        
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        
        # Garantir que todas as chaves esperadas existam (mesmo que vazias)
        expected_keys = [
            'GERENCIANET_CLIENT_ID', 'GERENCIANET_CLIENT_SECRET', 'GERENCIANET_SANDBOX', 
            'APP_URL', 'GERENCIANET_WEBHOOK_SECRET',
            'SMTP_SERVER', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD', 'SMTP_FROM_EMAIL',
            'BOLETO_JUROS_PADRAO', 'BOLETO_MULTA_PADRAO', 'CARNE_PARCELAS_MAX',
            'BANCO_CODIGO', 'BANCO_AGENCIA', 'BANCO_CONTA', 'EMPRESA_CNPJ', 'EMPRESA_NOME',
            'COMPANY_NAME', 'COMPANY_RAZAO_SOCIAL', 'COMPANY_CNPJ', 'COMPANY_IE', 
            'COMPANY_TELEFONE', 'COMPANY_EMAIL', 'COMPANY_ENDERECO', 'COMPANY_LOGO',
            'PIX_CHAVE', 'PIX_TIPO_CHAVE', 'PIX_BENEFICIARIO', 'PIX_CIDADE'
        ]
        
        final_config = {}
        for key in expected_keys:
            final_config[key] = config.get(key, defaults.get(key, ''))
            
        return final_config

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar configurações: {str(e)}")

@router.get("/flat")
async def get_configurations_flat(current_user = Depends(obter_usuario_admin)) -> Dict[str, Any]:
    """
    Obter todas as configurações do sistema em formato flat (compatível com o frontend)
    """
    try:
        config = await get_configurations(current_user)
        return {
            "gerencianet": {
                "client_id": config.get('GERENCIANET_CLIENT_ID', ''),
                "client_secret": config.get('GERENCIANET_CLIENT_SECRET', ''),
                "sandbox": config.get('GERENCIANET_SANDBOX', 'true') == 'true',
                "app_url": config.get('APP_URL', ''),
                "webhook_secret": config.get('GERENCIANET_WEBHOOK_SECRET', '')
            },
            "email": {
                "smtp_server": config.get('SMTP_SERVER', ''),
                "smtp_port": config.get('SMTP_PORT', ''),
                "smtp_username": config.get('SMTP_USERNAME', ''),
                "smtp_password": config.get('SMTP_PASSWORD', ''),
                "smtp_from_email": config.get('SMTP_FROM_EMAIL', '')
            },
            "negocio": {
                "boleto_juros_padrao": config.get('BOLETO_JUROS_PADRAO', ''),
                "boleto_multa_padrao": config.get('BOLETO_MULTA_PADRAO', ''),
                "carne_parcelas_max": config.get('CARNE_PARCELAS_MAX', '')
            },
            "pix": {
                "pix_chave": config.get('PIX_CHAVE', ''),
                "pix_tipo_chave": config.get('PIX_TIPO_CHAVE', 'cpf'),
                "pix_beneficiario": config.get('PIX_BENEFICIARIO', ''),
                "pix_cidade": config.get('PIX_CIDADE', '')
            },
            "bancario": {
                "banco_codigo": config.get('BANCO_CODIGO', ''),
                "banco_agencia": config.get('BANCO_AGENCIA', ''),
                "banco_conta": config.get('BANCO_CONTA', ''),
                "empresa_cnpj": config.get('EMPRESA_CNPJ', ''),
                "empresa_nome": config.get('EMPRESA_NOME', '')
            },
            "empresa": {
                "company_name": config.get('COMPANY_NAME', ''),
                "company_razao_social": config.get('COMPANY_RAZAO_SOCIAL', ''),
                "company_cnpj": config.get('COMPANY_CNPJ', ''),
                "company_ie": config.get('COMPANY_IE', ''),
                "company_telefone": config.get('COMPANY_TELEFONE', ''),
                "company_email": config.get('COMPANY_EMAIL', ''),
                "company_endereco": config.get('COMPANY_ENDERECO', ''),
                "company_logo": config.get('COMPANY_LOGO', '')
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def save_configurations(
    config_data: Dict[str, Any],
    current_user = Depends(obter_usuario_admin)
):
    """
    Salvar configurações do sistema
    """
    try:
        # Achatar o dicionário para salvar no .env
        flat_config = {}
        
        if 'gerencianet' in config_data:
            g = config_data['gerencianet']
            flat_config['GERENCIANET_CLIENT_ID'] = g.get('client_id', '')
            flat_config['GERENCIANET_CLIENT_SECRET'] = g.get('client_secret', '')
            flat_config['GERENCIANET_SANDBOX'] = str(g.get('sandbox', 'true')).lower()
            flat_config['APP_URL'] = g.get('app_url', '')
            flat_config['GERENCIANET_WEBHOOK_SECRET'] = g.get('webhook_secret', '')

        if 'email' in config_data:
            e = config_data['email']
            flat_config['SMTP_SERVER'] = e.get('smtp_server', '')
            flat_config['SMTP_PORT'] = str(e.get('smtp_port', ''))
            flat_config['SMTP_USERNAME'] = e.get('smtp_username', '')
            flat_config['SMTP_PASSWORD'] = e.get('smtp_password', '')
            flat_config['SMTP_FROM_EMAIL'] = e.get('smtp_from_email', '')

        if 'negocio' in config_data:
            n = config_data['negocio']
            flat_config['BOLETO_JUROS_PADRAO'] = str(n.get('boleto_juros_padrao', ''))
            flat_config['BOLETO_MULTA_PADRAO'] = str(n.get('boleto_multa_padrao', ''))
            flat_config['CARNE_PARCELAS_MAX'] = str(n.get('carne_parcelas_max', ''))

        if 'pix' in config_data:
            p = config_data['pix']
            flat_config['PIX_CHAVE'] = p.get('pix_chave', '')
            flat_config['PIX_TIPO_CHAVE'] = p.get('pix_tipo_chave', 'cpf')
            flat_config['PIX_BENEFICIARIO'] = p.get('pix_beneficiario', '')
            flat_config['PIX_CIDADE'] = p.get('pix_cidade', '')

        if 'bancario' in config_data:
            b = config_data['bancario']
            flat_config['BANCO_CODIGO'] = b.get('banco_codigo', '')
            flat_config['BANCO_AGENCIA'] = b.get('banco_agencia', '')
            flat_config['BANCO_CONTA'] = b.get('banco_conta', '')
            flat_config['EMPRESA_CNPJ'] = b.get('empresa_cnpj', '')
            flat_config['EMPRESA_NOME'] = b.get('empresa_nome', '')

        if 'empresa' in config_data:
            emp = config_data['empresa']
            flat_config['COMPANY_NAME'] = emp.get('company_name', '')
            flat_config['COMPANY_RAZAO_SOCIAL'] = emp.get('company_razao_social', '')
            flat_config['COMPANY_CNPJ'] = emp.get('company_cnpj', '')
            flat_config['COMPANY_IE'] = emp.get('company_ie', '')
            flat_config['COMPANY_TELEFONE'] = emp.get('company_telefone', '')
            flat_config['COMPANY_EMAIL'] = emp.get('company_email', '')
            flat_config['COMPANY_ENDERECO'] = emp.get('company_endereco', '')
            flat_config['COMPANY_LOGO'] = emp.get('company_logo', '')

        # Chamar a função de atualização existente
        return await update_configurations(flat_config, current_user)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logo")
async def upload_logo(
    file: UploadFile = File(...),
    current_user = Depends(obter_usuario_admin)
):
    """
    Upload do logo da empresa
    """
    try:
        # Criar diretório static/uploads se não existir
        # api.py está em crm_modules/configuracoes/
        # static está em interfaces/web/static/
        base_dir = Path(__file__).parent.parent.parent
        upload_dir = base_dir / 'interfaces' / 'web' / 'static' / 'uploads'
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Nome do arquivo
        file_extension = file.filename.split('.')[-1]
        file_name = f"company_logo.{file_extension}"
        file_path = upload_dir / file_name

        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # URL do logo
        logo_url = f"/static/uploads/{file_name}"
        
        return {"logo_url": logo_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload do logo: {str(e)}")

@router.put("/")
async def update_configurations(
    configuracoes: Dict[str, Any],
    current_user = Depends(obter_usuario_admin)
):
    """
    Atualizar configurações do sistema
    """
    try:
        # Caminho do arquivo .env
        env_path = Path(__file__).parent.parent.parent / '.env'

        if not env_path.exists():
            raise HTTPException(status_code=404, detail="Arquivo .env não encontrado")

        # Ler conteúdo atual do .env
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Atualizar linhas específicas
        updated_lines = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                updated_lines.append(line)
                continue

            key = line.split('=')[0] if '=' in line else ''
            if key in configuracoes:
                value = configuracoes[key]
                if value is not None and value != '':
                    updated_lines.append(f"{key}={value}")
                # Se valor for vazio, não incluir a linha
            else:
                updated_lines.append(line)

        # Adicionar novas configurações que não existiam
        existing_keys = {line.split('=')[0] for line in lines if '=' in line and not line.startswith('#')}
        for key, value in configuracoes.items():
            if key not in existing_keys and value is not None and value != '':
                updated_lines.append(f"{key}={value}")

        # Escrever de volta no arquivo
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines) + '\n')

        return {"message": "Configurações atualizadas com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar configurações: {str(e)}")