from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from app.auth import get_tenant_from_header
from fastapi import status
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.produto import Produto

router = APIRouter(
    prefix="/api/cardapio",
    tags=["Cardápio"]
)

class CrossSellItem(BaseModel):
    item_id: int
    nome: str
    preco_adicional: float

class ItemCardapio(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    preco: float
    preco_promocional: Optional[float] = None  # Para descontos
    categoria: str
    estoque_atual: int = 0
    ativo: bool = True
    # Cross-selling: IDs de itens que sugerimos junto com este
    itens_sugeridos: List[CrossSellItem] = []
    
class ItemCardapioUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    preco_promocional: Optional[float] = None
    categoria: Optional[str] = None
    estoque_atual: Optional[int] = None
    ativo: Optional[bool] = None
    
@router.get("/", response_model=List[ItemCardapio], summary="Listar itens com filtros")
def listar_cardapio(
    categoria: Optional[str] = None,
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_from_header)
):
    query = db.query(Produto).filter(Produto.tenant_id == tenant_id)
    
    if categoria:
        query = query.filter(Produto.categoria == categoria)
    
    if ativo is not None:
        query = query.filter(Produto.ativo == ativo)
        
    return query.all()

@router.post("/", response_model=ItemCardapio, summary="Adicionar item completo")
def adicionar_item(
    item: ItemCardapio, 
    db: Session = Depends(get_db), 
    tenant_id: int = Depends(get_tenant_from_header)
):
    # 1. Cria a entidade do modelo (assumindo que você criou o modelo Produto no SQLAlchemy)
    novo_produto = Produto(
        nome=item.nome,
        preco=item.preco,
        preco_promocional=item.preco_promocional,
        estoque=item.estoque_atual,
        categoria=item.categoria,
        tenant_id=tenant_id
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto
    
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover item do cardápio")
def remover_item(
    item_id: int, 
    db: Session = Depends(get_db), 
    tenant_id: int = Depends(get_tenant_from_header)
):
    # 1. Busca o produto no banco garantindo que pertença ao tenant
    item = db.query(Produto).filter(
        Produto.id == item_id, 
        Produto.tenant_id == tenant_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item não encontrado ou acesso negado."
        )
    
    # 2. Remove o item
    db.delete(item)
    db.commit()
    
    return None