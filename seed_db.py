from app.database.connection import SessionLocal, engine, Base
from app.models.usuario import Usuario
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    db = SessionLocal()
    # Verifica se já existe um admin para não duplicar
    if not db.query(Usuario).filter(Usuario.email == "admin@hokage.com").first():
        admin = Usuario(
            email="admin@hokage.com",
            senha_hash=pwd_context.hash("123456"), # Senha: 123456
            tenant_id=1 # Primeiro tenant
        )
        db.add(admin)
        db.commit()
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe.")
    db.close()

if __name__ == "__main__":
    init_db()