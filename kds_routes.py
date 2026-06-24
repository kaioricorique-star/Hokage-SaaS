from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_tenant_from_header
from app.models.atendimento_kds import PedidoKDS, Mesas

router = APIRouter(
    prefix="/api/kds", 
    tags=["Cozinha (KDS)"], 
    dependencies=[Depends(get_tenant_from_header)]
)

class NovoPedidoKDS(BaseModel):
    mesa_id: Optional[int] = None
    balcao_nome: Optional[str] = None
    garcom_nome: Optional[str] = None
    itens: str

@router.post("/pedidos")
def criar_pedido_cozinha(dados: NovoPedidoKDS, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    novo_pedido = PedidoKDS(
        tenant_id=tenant_id,
        mesa_id=dados.mesa_id,
        balcao_nome=dados.balcao_nome,
        garcom_nome=dados.garcom_nome,
        itens=dados.itens
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return {"mensagem": "Pedido enviado para a cozinha", "pedido_id": novo_pedido.id}

@router.get("/pedidos-pendentes")
def listar_pedidos_cozinha(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(PedidoKDS).filter(
        PedidoKDS.tenant_id == tenant_id,
        PedidoKDS.status != "Entregue"
    ).order_by(PedidoKDS.data_criacao.asc()).all()

@router.patch("/pedidos/{pedido_id}/status")
def atualizar_status_kds(pedido_id: int, novo_status: str, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    pedido = db.query(PedidoKDS).filter(PedidoKDS.id == pedido_id, PedidoKDS.tenant_id == tenant_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    pedido.status = novo_status
    db.commit()
    return {"mensagem": "Status atualizado com sucesso"}