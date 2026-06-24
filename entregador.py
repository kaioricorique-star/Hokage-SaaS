# app/routers/entregador.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.entregador import EntregadorCreate, EntregadorUpdate

router = APIRouter(
    prefix="/api/entregadores",
    tags=["Entregadores"]
)

# Simulação de base de dados em memória (substitua pelo seu banco SQLAlchemy)
fake_db_entregadores = []

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_entregador(entregador: EntregadorCreate):
    """
    Cria um novo entregador.
    """
    novo_id = len(fake_db_entregadores) + 1
    novo_entregador = {
        "id": novo_id,
        **entregador.dict(),
        "ativo": True
    }
    fake_db_entregadores.append(novo_entregador)
    return novo_entregador

@router.put("/{entregador_id}")
def editar_entregador(entregador_id: int, entregador_dados: EntregadorUpdate):
    """
    Edita os dados de um entregador existente pelo ID.
    """
    for item in fake_db_entregadores:
        if item["id"] == entregador_id:
            # Atualiza apenas os campos fornecidos
            update_data = entregador_dados.dict(exclude_unset=True)
            item.update(update_data)
            return {"message": "Entregador atualizado com sucesso.", "entregador": item}
    
    raise HTTPException(status_code=404, detail="Entregador não encontrado.")

@router.delete("/{entregador_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_entregador(entregador_id: int):
    """
    Remove um entregador pelo ID.
    """
    for index, item in enumerate(fake_db_entregadores):
        if item["id"] == entregador_id:
            fake_db_entregadores.pop(index)
            return None
            
    raise HTTPException(status_code=404, detail="Entregador não encontrado.")

# Rota extra para listar e poder testar os IDs
@router.get("/")
def listar_entregadores():
    return fake_db_entregadores