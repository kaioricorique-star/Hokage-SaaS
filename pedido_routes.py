from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_tenant_from_header
from ..pedido import Pedido
from app.models.financeiro import Financeiro
from ..services.payment_service import processar_pagamento_pedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"], dependencies=[Depends(get_tenant_from_header)])

@router.get("/")
def listar_pedidos(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Pedido).filter(Pedido.tenant_id == tenant_id).all()

@router.post("/")
def criar_pedido(descricao: str, valor: float, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    novo_pedido = Pedido(descricao=descricao, valor=valor, tenant_id=tenant_id)
    db.add(novo_pedido)
    
    nova_entrada = Financeiro(
        descricao=f"Venda: {descricao}", 
        valor=valor, 
        tipo="ENTRADA", 
        tenant_id=tenant_id
    )
    db.add(nova_entrada)
    
    db.commit()
    db.refresh(novo_pedido)
    return {"message": "Pedido e registro financeiro criados com sucesso"}

@router.post("/pagar/{pedido_id}")
def endpoint_pagar(pedido_id: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id, Pedido.tenant_id == tenant_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    
    return processar_pagamento_pedido(pedido_id, db=db, tenant_id=tenant_id)