# database.py
from sqlmodel import SQLModel, Session, create_engine

# Configuração do banco de dados SQLite
sqlite_file_name = "finances.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Cria o motor do banco de dados
engine = create_engine(sqlite_url, echo=True)

# Importa todos os modelos para garantir que sejam criados
from models.transaction import Transaction
from models.goal import Goal

def create_db_and_tables():
    """Cria as tabelas no banco de dados"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Função geradora para a dependência de sessão do FastAPI"""
    with Session(engine) as session:
        yield session
