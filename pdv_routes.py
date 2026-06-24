from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.auth import get_tenant_from_header

router = APIRouter(
    prefix="/api/pdv", 
    tags=["PDV"],
    dependencies=[Depends(get_tenant_from_header)]
)

class PagamentoItem(BaseModel):
    metodo: str
    valor: float

class VendaRequest(BaseModel):
    itens: list
    desconto: float = 0.0
    pagamentos: List[PagamentoItem]


@router.post("/registrar-venda")
def registrar_venda(tenant_id: int = Depends(get_tenant_from_header)):
    return {
        "status": "teste", 
        "tenant_id": tenant_id
    }

@router.post("/venda")
async def processar_venda(pedido: VendaRequest, db = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return {
        "status": "sucesso",
        "tenant_id": tenant_id,
        "desconto_aplicado": pedido.desconto,
        "quantidade_pagamentos": len(pedido.pagamentos)
    }