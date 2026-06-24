from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.auth import get_tenant_from_header
from datetime import date
from app.models.financeiro import Financeiro
from app.routes import pdv_routes
router = APIRouter(
    prefix="/api/dashboard", 
    tags=["Dashboard"], 
    dependencies=[Depends(get_tenant_from_header)]
)

@router.get("/resumo-diario")
def obter_resumo_diario(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    hoje = date.today()
    
    # 1. Performance: Agregação direta no banco (SQLAlchemy)
    resumo_vendas = db.query(
        func.sum(Venda.total).label("faturamento_bruto"),
        func.count(Venda.id).label("total_pedidos")
    ).filter(
        Venda.tenant_id == tenant_id,
        func.date(Venda.data_criacao) == hoje
    ).first()

    faturamento = resumo_vendas.faturamento_bruto or 0.0
    total_pedidos = resumo_vendas.total_pedidos or 0

    # 2. Lucro Líquido: Buscando despesas do Financeiro
    despesas_hoje = db.query(func.sum(Financeiro.valor)).filter(
        Financeiro.tenant_id == tenant_id,
        Financeiro.tipo == 'SAIDA',
        func.date(Financeiro.data_criacao) == hoje
    ).scalar() or 0.0

    lucro_liquido = faturamento - despesas_hoje
    
    return {
        "vendas_hoje": total_pedidos,
        "faturamento": faturamento,
        "despesas": despesas_hoje,
        "lucro_liquido": lucro_liquido,
        "ticket_medio": (faturamento / total_pedidos) if total_pedidos > 0 else 0.0
    }