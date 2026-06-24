from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_tenant_from_header
from app.models.caixa import Caixa
from app.models import financeiro # Importação necessária

router = APIRouter(
    prefix="/api/caixa", 
    tags=["Caixa"]
) # <--- Parêntese fechado corretamente aqui

@router.get("/resumo-diario", summary="Obter resumo do caixa aberto")
def resumo_diario(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    caixa_aberto = db.query(Caixa).filter(
        Caixa.tenant_id == tenant_id, 
        Caixa.status == "aberto"
    ).first()
    
    if not caixa_aberto:
        return {"status": "Caixa Fechado"}
        
    return {
        "status": "Caixa Aberto",
        "abertura": caixa_aberto.data_abertura,
        "mensagem": "Integre com a soma de pagamentos aqui"
    }

@router.get("/")
def listar_movimentacoes(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    # Agora com o modelo Financeiro importado, isto funcionará
    movimentacoes = db.query(Financeiro).filter(Financeiro.tenant_id == tenant_id).all()
    
    return movimentacoes