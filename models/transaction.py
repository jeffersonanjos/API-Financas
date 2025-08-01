# models/transaction.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Enum para o tipo de transação ('receita' ou 'despesa')
class TransactionType(str, Enum):
    despesa = "despesa"
    receita = "receita"
    
# Enum para as categorias permitidas
class CategoriaTransacao(str, Enum):
    alimentacao = "alimentacao"
    lazer = "lazer"
    saude = "saude"
    contas = "contas"
    outros = "outros"

# Modelo de base que será usado para a criação e atualização
class TransactionBase(SQLModel):
    description: str
    amount: float
    type: TransactionType
    category: CategoriaTransacao = Field(default=CategoriaTransacao.outros)
    date: datetime = Field(default_factory=datetime.now)

# Modelo da tabela que herda do TransactionBase e adiciona o ID
class Transaction(TransactionBase, table=True):
    __tablename__ = "transactions"
    id: Optional[int] = Field(default=None, primary_key=True)

# Modelo para a criação de uma transação
class TransactionCreate(TransactionBase):
    pass

# Modelo para atualização, onde todos os campos são opcionais
class TransactionUpdate(SQLModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[CategoriaTransacao] = Field(default=None)
    date: Optional[datetime] = None

# Modelo para resposta de transação individual
class TransactionResponse(SQLModel):
    id: int
    description: str
    amount: float
    type: str
    date: datetime

# Modelo para agrupar transações por categoria
class GroupedTransactions(SQLModel):
    category: CategoriaTransacao
    total_amount: float
