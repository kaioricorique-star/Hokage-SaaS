from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.produto import Produto
from app.auth import get_tenant_from_header
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse

router = APIRouter(dependencies=[Depends(get_tenant_from_header)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/produtos", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    novo_produto = Produto(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto
# A "Válvula de Escape": Se for Master, ignora o filtro. Se for comum, filtra pelo tenant.
    if auth_data["role"] != "Master":
        query = query.filter(Produto.tenant_id == auth_data["tenant_id"])
        
    return query.all()
    
@router.get("/produtos", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Produto).filter(Produto.tenant_id == tenant_id).all()
    # A "Válvula de Escape": Se for Master, ignora o filtro. Se for comum, filtra pelo tenant.
    if auth_data["role"] != "Master":
        query = query.filter(Produto.tenant_id == auth_data["tenant_id"])
        
    return query.all()

@router.delete("/produtos/{produto_id}")
def deletar_produto(
    produto_id: int, 
    db: Session = Depends(get_db), 
    tenant_id: int = Depends(get_tenant_from_header)
):
    produto = db.query(Produto).filter(Produto.id == produto_id, Produto.tenant_id == tenant_id).first()
    # A "Válvula de Escape": Se for Master, ignora o filtro. Se for comum, filtra pelo tenant.
    if auth_data["role"] != "Master":
        query = query.filter(Produto.tenant_id == auth_data["tenant_id"])
        
    return query.all()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    db.delete(produto)
    db.commit()
    return {"message": "Produto deletado com sucesso"}