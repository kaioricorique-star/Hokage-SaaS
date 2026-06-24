from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.tenant import Tenant
from app.models.usuario import Usuario
from app.schemas.tenant_schema import TenantCreate, TenantResponse
from app.auth import get_tenant_from_header
from passlib.context import CryptContext
from ..services.tenant_service import salvar_configuracao_tenant

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/tenants", response_model=TenantResponse)
def criar_loja(tenant: TenantCreate, db: Session = Depends(get_db)):
    nova_loja = Tenant(
        nome_fantasia=tenant.nome_fantasia,
        cnpj=tenant.cnpj,
        slug=tenant.slug,
        endereco=tenant.endereco, # Adicionado
        telefone=tenant.telefone   # Adicionado
    )
    db.add(nova_loja)
    db.commit()
    db.refresh(nova_loja)
    
@router.get("/tenants", response_model=List[TenantResponse], dependencies=[Depends(get_tenant_from_header)])
def listar_lojas(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Tenant).filter(Tenant.id == tenant_id).all()

@router.delete("/tenants", dependencies=[Depends(get_tenant_from_header)])
def deletar_loja(del_tenant_id: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    if del_tenant_id != tenant_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar esta loja.")
    
    loja = db.query(Tenant).filter(Tenant.id == del_tenant_id).first()
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada.")
        
    db.delete(loja)
    db.commit()
    return {"message": "Loja deletada com sucesso"}