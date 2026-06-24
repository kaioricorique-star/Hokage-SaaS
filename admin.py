# app/routers/admin.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/admin",
    tags=["Painel de Controle - Administrador"]
)

# --- Schemas para o Admin ---
class TenantStatusUpdate(BaseModel):
    is_blocked: bool
    motivo: Optional[str] = "Manutenção ou Inadimplência"

# Simulação de banco de dados (Substitua pelo seu SQLAlchemy/PostgreSQL)
fake_db_tenants = [
    {"tenant_id": 1, "nome_loja": "Loja adm 1", "status": "ACTIVE", "plan": "Premium"},
    {"tenant_id": 2, "nome_loja": "Mercadinho Central", "status": "ACTIVE", "plan": "Basic"},
    {"tenant_id": 3, "nome_loja": "Padaria Pão Quente", "status": "BLOCKED", "plan": "Premium"}
]

@router.get("/tenants")
def listar_todas_as_lojas():
    """
    Lista todas as lojas/tenants cadastradas na plataforma SaaS.
    """
    return {
        "total_lojas": len(fake_db_tenants),
        "lojas": fake_db_tenants
    }

@router.patch("/tenants/{tenant_id}/status")
def alterar_status_loja(tenant_id: int, status_data: TenantStatusUpdate):
    """
    Função de administrador: Bloqueia ou desbloqueia o acesso de uma loja globalmente.
    """
    for loja in fake_db_tenants:
        if loja["tenant_id"] == tenant_id:
            loja["status"] = "BLOCKED" if status_data.is_blocked else "ACTIVE"
            acao = "bloqueada" if status_data.is_blocked else "desbloqueada/ativa"
            return {
                "message": f"Acesso da loja #{tenant_id} alterado para {acao}.",
                "detalhes": loja
            }
            
    raise HTTPException(status_code=404, detail="Loja/Tenant não encontrada.")

@router.get("/sistema/metricas")
def obter_metricas_globais():
    """
    Obtém estatísticas gerais do servidor (NOC) para o painel do superadministrador.
    """
    return {
        "servidor_ativo": True,
        "uso_memoria_mb": 450,
        "lojas_ativas": len([l for l in fake_db_tenants if l["status"] == "ACTIVE"]),
        "lojas_bloqueadas": len([l for l in fake_db_tenants if l["status"] == "BLOCKED"]),
        "tempo_atividade_horas": 724
    }