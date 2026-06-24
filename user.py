from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    nome_empresa = Column(String, index=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    is_admin = Column(Boolean, default=False)