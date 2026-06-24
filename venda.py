from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Venda(Base):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    total = Column(Float, nullable=False)
    status = Column(String, default="pendente") # ex: pendente, concluida, cancelada
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com os itens da venda
    itens = relationship("ItemVenda", back_populates="venda")

class ItemVenda(Base):
    __tablename__ = "itens_venda"
    
    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    
    venda = relationship("Venda", back_populates="itens")