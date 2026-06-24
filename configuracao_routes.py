from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.auth import get_tenant_from_header

router = APIRouter(
    prefix="/api/configuracoes",
    tags=["Configurações"],
    dependencies=[Depends(get_tenant_from_header)]
)

class ConfiguracaoEmpresa(BaseModel):
    id: Optional[int] = None
    nome_empresa: str
    cnpj: str
    endereco: str
    usa_impressao_remota: bool
    limite_estoque_alerta: int

db_config = ConfiguracaoEmpresa(
    id=1, 
    nome_empresa="Hokage Lanches LTDA", 
    cnpj="00.000.000/0001-00", 
    endereco="Rua Ninja, 100", 
    usa_impressao_remota=True, 
    limite_estoque_alerta=5
)

@router.get("/", response_model=ConfiguracaoEmpresa, summary="Obter configurações da empresa")
def obter_configuracoes(tenant_id: int = Depends(get_tenant_from_header)):
    return db_config

@router.put("/", response_model=ConfiguracaoEmpresa, summary="Atualizar configurações da empresa")
def atualizar_configuracoes(nova_config: ConfiguracaoEmpresa, tenant_id: int = Depends(get_tenant_from_header)):
    global db_config
    nova_config.id = 1
    db_config = nova_config
    return db_config