# models/transaction.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    """Tipos de transação"""
    receita = "receita"
    despesa = "despesa"

class Category(str, Enum):
    """Categorias de transação"""
    alimentacao = "alimentacao"
    lazer = "lazer"
    saude = "saude"
    contas = "contas"
    outros = "outros"

class TransactionBase(SQLModel):
    """Modelo base para transações"""
    description: str = Field(..., description="Descrição da transação")
    amount: float = Field(..., description="Valor da transação")
    type: TransactionType = Field(..., description="Tipo: receita ou despesa")
    category: Category = Field(default=Category.outros, description="Categoria da transação")
    date: datetime = Field(default_factory=datetime.now, description="Data da transação")

class Transaction(TransactionBase, table=True):
    """Modelo da tabela de transações"""
    __tablename__ = "transactions"
    id: Optional[int] = Field(default=None, primary_key=True)

class TransactionCreate(TransactionBase):
    """Modelo para criação de transação"""
    pass

class TransactionUpdate(SQLModel):
    """Modelo para atualização de transação"""
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[Category] = None
    date: Optional[datetime] = None

class TransactionResponse(TransactionBase):
    """Modelo para resposta de transação"""
    id: int

class TransactionSummary(SQLModel):
    """Modelo para resumo de transações por categoria"""
    category: Category
    total_amount: float
    transaction_count: int
