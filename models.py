from sqlalchemy import Column, Integer, String, Float
from database import Base

class Transaction(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    valor = Column(Float)
    categoria = Column(String)

    def save(self):
        session = Session()
        session.add(self)
        session.commit()

    @staticmethod
    def get_all():
        session = Session()
        return session.query(Transaction).all()

class Goal(Base):
    __tablename__ = "metas"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    valor_alvo = Column(Float)