# pip install fastapi uvicorn pydantic
# pip freeze > requirements.txt
# uvicorn main:app

from typing import List
from uuid import UUID
from fastapi import FastAPI
from models import Transaction, Meta

app = FastAPI()

transacoes:List[Transaction]=[]
metas:List[Meta]=[]

# Rotas de Transações
@app.post("/transacoes/")
def add_transacao(desc: str, valor: float, categoria: str):
    transacao = {
        "id": UUID.uuid4(),
        "desc": desc,
        "valor": valor,
        "categoria": categoria
    }

    trans = Transaction(**transacao)
    transacoes.append(trans)
    
    

@app.get("/transacoes/")
def listar_transacoes():
    return transacoes

# Rotas de Metas (simplificado)
@app.post("/metas/")
def add_meta(nome: str, valor_alvo: float):
    meta = {
        "id": UUID.uuid3(),
        "nome": nome,
        "valor_alvo": valor_alvo
    }

    goal = Meta(**meta)
    metas.append(goal)

@app.get("/metas/")
def listar_metas():
    return metas

