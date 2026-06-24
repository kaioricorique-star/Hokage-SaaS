from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel
from app.models.usuario import Usuario 

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

# Schemas atualizados para refletir o seu modelo
class LoginSchema(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str
    tenant_id: int

@router.post("/register")
def registrar_usuario(dados: UserCreate, db: Session = Depends(get_db)):
    # Buscando pelo campo correto: 'email'
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Criando com o campo correto: 'senha_hash'
    novo_usuario = Usuario(
        email=dados.email, 
        senha_hash=dados.password, # Lembre-se de futuramente usar hash aqui
        tenant_id=dados.tenant_id
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"message": "Usuário criado com sucesso!"}

@router.post("/login")
def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    # Buscando pelo campo correto: 'email'
    usuario = db.query(Usuario).filter(Usuario.email == login_data.email).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
    
    # Verificando contra o campo correto: 'senha_hash'
    if usuario.senha_hash != login_data.password:
        raise HTTPException(status_code=401, detail="Senha incorreta.")
    
    return {
        "message": "Login realizado",
        "tenant_id": usuario.tenant_id
    }