from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = False
    positionstack_api_key: str = ""
    mikrotik_host: str = ""
    mikrotik_user: str = ""
    mikrotik_password: str = ""
    huawei_host: str = ""
    huawei_user: str = ""
    huawei_password: str = ""
    company_name: str = "CRM Provedor"
    company_razao_social: str = ""
    company_logo: str = ""
    company_cnpj: str = ""
    company_ie: str = ""
    company_telefone: str = ""
    company_email: str = ""
    company_endereco: str = ""
    contract_template_html: str = ""

    # Configurações Gerencianet/Boleto
    gerencianet_sandbox: str = "true"
    boleto_juros_padrao: str = "0.1"
    boleto_multa_padrao: str = "2"
    carne_parcelas_max: str = "24"

    # Configurações PIX
    pix_chave: str = ""
    pix_tipo_chave: str = "cpf"
    pix_beneficiario: str = ""
    pix_cidade: str = ""

    # Configurações SMTP
    smtp_port: str = "587"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
