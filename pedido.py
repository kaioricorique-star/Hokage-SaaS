from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Pedido(Base):
    __tablename__ = "Pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    valor = Column(Float)
    tenant_id = Column(Integer, index=True)
    status = Column(String, default="ATIVO") # Campo necessário para a lógica de cancelamento