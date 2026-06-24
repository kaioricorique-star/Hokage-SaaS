from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from app.models.financeiro import Financeiro
from app.auth import get_tenant_from_header

router = APIRouter(
    prefix="/webwook", 
    tags=["Pagamentos"],
    dependencies=[Depends(get_tenant_from_header)]
)

@router.post("/mercado-pago/{tenant_id}")
async def webwook_mercado_pago(tenant_id: int, request: Request, db: Session = Depends(get_db), authenticated_tenant_id: int = Depends(get_tenant_from_header)):
    # Garante que o tenant logado é o mesmo que está efetuando a chamada no webhook
    if tenant_id != authenticated_tenant_id:
        raise HTTPException(status_code=403, detail="Acesso negado ao webhook")
        
    payload = await request.json()
    if payload.get("action") == "payment.updated":
        return {"status": "recebido"}
    
    return {"status": "ignorado"}