# app/dependencies.py
from fastapi import Header, HTTPException

# Exemplo simples de como identificar a loja
def get_current_tenant(x_tenant_id: int = Header(...)):
    # Aqui você validaria se a loja existe no banco de dados
    if not x_tenant_id:
        raise HTTPException(status_code=403, detail="Loja não identificada")
    return x_tenant_id