from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.usuario import Usuario
from app.auth import get_tenant_from_header
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse,PerfilUpdateSchema 
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter(dependencies=[Depends(get_tenant_from_header)])

@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    return db.query(Usuario).filter(Usuario.tenant_id == tenant_id).all()

@router.post("/api/usuarios")
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_tenant_from_header)):
    # Verifica se quem faz a requisição tem permissão
    if current_user.role not in ["Master", "Admin"]:
        raise HTTPException(status_code=403, detail="Você não tem permissão para criar usuários")
    
    # Lógica de criação...
    return {"message": "Usuário criado com sucesso"}
    
@router.put("/perfil/atualizar")
def atualizar_perfil(dados: PerfilUpdateSchema, 
    db: Session = Depends(get_db), 
    usuario_logado = Depends(get_tenant_from_header) # Sua dependência que valida o token
):
    # 1. Busca o usuário pelo ID que veio do token
    usuario = db.query(Usuario).filter(Usuario.id == usuario_logado.id).first()
    if dados.email:
        usuario.email = dados.email
    if dados.senha:
        usuario.senha_hash = pwd_context.hash(dados.senha)
    
    db.commit()
    return {"message": "Perfil atualizado com sucesso!"}
@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_from_header)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.tenant_id == tenant_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}