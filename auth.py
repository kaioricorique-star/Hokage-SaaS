from fastapi import Header, HTTPException

def get_tenant_from_header(x_tenant_id: int = Header(..., alias="X-Tenant-ID")):
    if not x_tenant_id:
        raise HTTPException(
            status_code=400, 
            detail="Header X-Tenant-ID é obrigatório para identificar a loja."
        )
    return x_tenant_id