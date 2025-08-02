from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class GoalStatus(str, Enum):
    """Status das metas"""
    ativa = "ativa"
    concluida = "concluida"
    cancelada = "cancelada"

class GoalBase(SQLModel):
    """Modelo base para metas financeiras"""
    title: str = Field(..., description="Título da meta")
    description: Optional[str] = Field(default=None, description="Descrição da meta")
    target_amount: float = Field(..., description="Valor alvo da meta")
    current_amount: float = Field(default=0.0, description="Valor atual acumulado")
    deadline: Optional[datetime] = Field(default=None, description="Data limite para atingir a meta")
    status: GoalStatus = Field(default=GoalStatus.ativa, description="Status da meta")

class Goal(GoalBase, table=True):
    """Modelo da tabela de metas"""
    __tablename__ = "goals"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação")

class GoalCreate(GoalBase):
    """Modelo para criação de meta"""
    pass

class GoalUpdate(SQLModel):
    """Modelo para atualização de meta"""
    title: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[datetime] = None
    status: Optional[GoalStatus] = None

class GoalResponse(GoalBase):
    """Modelo para resposta de meta"""
    id: int
    created_at: datetime 