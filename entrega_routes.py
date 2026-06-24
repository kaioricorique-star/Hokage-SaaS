from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_tenant_from_header
from app.models.entrega import Entrega
from app.models.pedido import Pedido
from app.models.tenant import Tenant
from app.models.entregador import Entregador

router = APIRouter(prefix="/api/entregas", tags=["Entregas"])

@router.post("/entrega/estimativa")
def estimar_entrega(lat_cliente: float, lon_cliente: float, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)): 
    loja = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not loja or loja.latitude is None: raise HTTPException(status_code=404, detail="Configuração incompleta")
    dist = Entregador.calcular_distancia(loja.latitude, loja.longitude, lat_cliente, lon_cliente)
    return {"distancia_km": dist}

@router.post("/cancelar-reassinalar/{entrega_id}")
def cancelar_e_buscar_outro(entrega_id: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    entrega = db.query(Entrega).filter(Entrega.id == entrega_id, Entrega.tenant_id == tenant_id).first()
    if not entrega: raise HTTPException(status_code=404, detail="Não encontrado")
    entrega.status = "cancelado_imprevisto"
    pedido = db.query(Pedido).filter(Pedido.id == entrega.pedido_id, Pedido.tenant_id == tenant_id).first()
    entregador = db.query(Entregador).filter(Entregador.ativo == True, Entregador.tenant_id == tenant_id).first()
    if entregador and pedido:
        pedido.entregador_id = entregador.id
        db.add(Entrega(tenant_id=tenant_id, pedido_id=pedido.id, entregador_id=entregador.id, status="pendente"))
    db.commit()
    return {"status": "sucesso"}