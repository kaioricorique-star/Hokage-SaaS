from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_tenant_from_header
from app.models.atendimento_kds import Mesas, Balcao, Garcom

router = APIRouter(prefix="/api/atendimento", tags=["Atendimento (Mesas, Balcão, Garçom)"])

# --- Schemas necessários ---
class MesaCreate(BaseModel):
    numero: str
    capacidade: int

class BalcaoCreate(BaseModel):
    nome: str

class GarcomCreate(BaseModel):
    nome: str

# --- Rotas ---

@router.post("/mesas")
def criar_mesa(dados: MesaCreate, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    nova_mesa = Mesas(tenant_id=tenant_id, numero=dados.numero, capacidade=dados.capacidade)
    db.add(nova_mesa)
    db.commit()
    db.refresh(nova_mesa)
    return nova_mesa

@router.get("/mesas")
def listar_mesas(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Mesas).filter(Mesas.tenant_id == tenant_id).all()

@router.post("/balcoes")
def criar_balcao(dados: BalcaoCreate, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    novo = Balcao(tenant_id=tenant_id, nome=dados.nome)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/balcoes")
def listar_balcoes(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Balcao).filter(Balcao.tenant_id == tenant_id).all()

@router.post("/garcons")
def criar_garcom(dados: GarcomCreate, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    novo = Garcom(tenant_id=tenant_id, nome=dados.nome)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/garcons")
def listar_garcons(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Garcom).filter(Garcom.tenant_id == tenant_id).all()