from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from sqlalchemy import create_engine 
from app.models.atendimento_kds import Mesas, Balcao, Garcom, PedidoKDS#
from app.middlewares.audit_middleware import audit_dispatch
from app.database.connection import Base, engine
from app.routes import subscription
from app.routes import entregador
from app.routes import ticket_routes
from app.routes import admin
from app.routes import clientes_routes,cardapio_routes
from app.routes.caixa_routes import router as caixa_router
from app.routes import cardapio_routes
from app.routes import (
    auth_routes, tenant_routes, produto_routes, 
    entrega_routes, usuario_routes, pedido_routes,financeiro_routes, fiscal_routes, 
    pdv_routes, dashboard_routes, ia_routes, atendimento_routes, 
    kds_routes,webwook_routes
)

app = FastAPI(title="Hokage SaaS API 2026")

origins = [
    "http://localhost:8000/",                     # React/Vite local
    "https://seu-pdv-frontend.vercel.app",     # Front-end em produção
    "https://app.hokagepdv.com.br"             # Domínio oficial
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 3. Inicializa o banco (Garante que os models importados acima sejam criados)
Base.metadata.create_all(bind=engine)

# 4. Inclusão de rotas
app.include_router(auth_routes.router, prefix="/api", tags=["Autenticação"])
app.include_router(subscription.router)
app.include_router(atendimento_routes.router)
app.include_router(caixa_router)
app.include_router(cardapio_routes.router)
app.include_router(clientes_routes.router) 
app.include_router(dashboard_routes.router) 
app.include_router(entregador.router) 
app.include_router(entrega_routes.router, prefix="/api", tags=["Entregas"])
app.include_router(financeiro_routes.router, prefix="/api", tags=["Financeiro"])
app.include_router(fiscal_routes.router, prefix="/fiscal", tags=["Fiscal"])
app.include_router(ia_routes.router)
app.include_router(kds_routes.router)
app.include_router(admin.router)
app.include_router(pedido_routes.router, prefix="/api", tags=["Pedidos"])
app.include_router(produto_routes.router, prefix="/api", tags=["Produtos"])
app.include_router(tenant_routes.router, prefix="/api", tags=["Tenants"])
app.include_router(usuario_routes.router, prefix="/api", tags=["Usuários"])
app.include_router(pdv_routes.router, prefix="/pdv", tags=["PDV"])
app.include_router(ticket_routes.router, prefix="/api", tags=["Chamados de Suporte"])
# 5. Configuração de Segurança (Custom OpenAPI)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Hokage Enterprise SaaS",
        version="1.0.0",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
            
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
