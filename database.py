# database.py
from sqlmodel import SQLModel, Session, create_engine

# URL do banco de dados SQLite
sqlite_file_name = "finances.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Cria o motor do banco de dados com a configuração necessária para FastAPI
engine = create_engine(sqlite_url, echo=True)

# Função para criar as tabelas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Função geradora para a dependência de sessão do FastAPI
def get_session():
    with Session(engine) as session:
        yield session
