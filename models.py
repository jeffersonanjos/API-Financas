from pydantic import BaseModel
from uuid import UUID


class Transaction(BaseModel):
    id: UUID
    desc: str
    valor: float
    categoria: str

class Meta(BaseModel):
    id: UUID
    nome: str
    valor_alvo: float
