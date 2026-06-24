from fastapi import APIRouter, Depends
from app.auth import get_tenant_from_header

router = APIRouter(
    prefix="/api/fiscal",
    tags=["Fiscal"],
    dependencies=[Depends(get_tenant_from_header)]
)

@router.get("/imprimir/{pedido_id}")
async def imprimir_fiscal(pedido_id: int, tenant_id: int = Depends(get_tenant_from_header)):
    # Seu código protegido por tenant aqui
    return {"pedido_id": pedido_id, "extracted_tenant": tenant_id}