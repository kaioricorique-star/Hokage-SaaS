from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
# Importe corretamente a função que valida o tenant
from app.auth import get_tenant_from_header

router = APIRouter(
    prefix="/api/clientes",
    tags=["Clientes"]
)

class Cliente(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    endereço: str

# Exemplo de banco de dados em memória
db_clientes = [
    Cliente(id=1, nome="João Silva", cpf="111.222.333-44", endereço="rua sidonio paes lote 15 qd 10"),
    Cliente(id=2, nome="Maria Souza", cpf="555.666.777-88",endereço="rua sidonio paes lote 15 qd 10")
]

# A dependência de autenticação deve ser colocada nas rotas, não no router
@router.get("/", response_model=List[Cliente], summary="Listar todos os clientes")
def listar_clientes(tenant_id: int = Depends(get_tenant_from_header)):
    return db_clientes

@router.post("/", response_model=Cliente, summary="Cadastrar um novo cliente")
def cadastrar_cliente(cliente: Cliente, tenant_id: int = Depends(get_tenant_from_header)):
    novo_id = len(db_clientes) + 1
    cliente.id = novo_id
    db_clientes.append(cliente)
    return cliente

@router.get("/{cliente_id}", response_model=Cliente, summary="Buscar cliente por ID")
def obter_cliente(cliente_id: int, tenant_id: int = Depends(get_tenant_from_header)):
    cliente = next((c for c in db_clientes if c.id == cliente_id), None)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente
    