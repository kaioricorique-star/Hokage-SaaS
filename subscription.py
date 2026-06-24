from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from app.schemas import subscription
router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

# Rota 1: Definir ou alterar dias experimentais (Trial)
@router.post("/{tenant_id}/set-trial")
def configure_trial(tenant_id: int, days: int):
    # Lógica: define a data de término do trial (hoje + dias) e altera status para TRIAL
    trial_end = datetime.utcnow() + timedelta(days=days)
    # Salvar no banco: tenant.trial_ends_at = trial_end, tenant.status = "TRIAL"
    return {"message": f"Trial liberado para a loja {tenant_id} por {days} dias.", "ends_at": trial_end}

# Rota 2: Verificar status de acesso (Middleware / Rota chamada pelo Front ao carregar)
@router.get("/{tenant_id}/status")
def check_access_status(tenant_id: int):
    # Lógica: busca o tenant no banco e avalia se está bloqueado, inadimplente, etc.
    # Exemplo simplificado:
    # if tenant.status == "BLOCKED":
    #     raise HTTPException(status_code=403, detail="Acesso bloqueado. Débito pendente.")
    return {"status": "ACTIVE", "can_access": True, "days_left": 15}

# Rota 3: Liberar ou suspender acesso manualmente (Botão do Administrador do SaaS)
@router.post("/{tenant_id}/toggle-access")
def toggle_access(tenant_id: int, force_block: bool):
    # Lógica: se force_block=True, altera status para BLOCKED. Se False, reativa se pago.
    action = "Bloqueado" if force_block else "Liberado"
    return {"message": f"Acesso da loja {tenant_id} alterado para: {action}"}