# pip install fastapi uvicorn pydantic
# pip freeze > requirements.txt
# uvicorn main:app

from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import Transaction, Meta
import uuid

app = FastAPI()

transacoes: List[Transaction] = []
metas: List[Meta] = []

# Rotas de Transações
@app.post("/transacoes/", response_model=Transaction)
def add_transacao(desc: str, valor: float, categoria: str):
    transacao = {
        "id": uuid.uuid4(),
        "desc": desc,
        "valor": valor,
        "categoria": categoria
    }
    trans = Transaction(**transacao)
    transacoes.append(trans)
    return trans

@app.get("/transacoes/", response_model=List[Transaction])
def listar_transacoes():
    return transacoes

@app.get("/transacoes/{id}", response_model=Transaction)
def get_transacao(id: UUID):
    for t in transacoes:
        if t.id == id:
            return t
    raise HTTPException(status_code=404, detail="Transação não encontrada")

@app.delete("/transacoes/{id}")
def delete_transacao(id: UUID):
    for i, t in enumerate(transacoes):
        if t.id == id:
            del transacoes[i]
            return {"mensagem": "Transação deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Transação não encontrada")

@app.put("/transacoes/{id}", response_model=Transaction)
def atualizar_transacao(id: UUID, desc: str, valor: float, categoria: str):
    for i, t in enumerate(transacoes):
        if t.id == id:
            atualizada = Transaction(id=id, desc=desc, valor=valor, categoria=categoria)
            transacoes[i] = atualizada
            return atualizada
    raise HTTPException(status_code=404, detail="Transação não encontrada")

# Rotas de Metas
@app.post("/metas/", response_model=Meta)
def add_meta(nome: str, valor_alvo: float):
    meta = {
        "id": uuid.uuid4(),
        "nome": nome,
        "valor_alvo": valor_alvo
    }
    goal = Meta(**meta)
    metas.append(goal)
    return goal

@app.get("/metas/", response_model=List[Meta])
def listar_metas():
    return metas

@app.get("/metas/{id}", response_model=Meta)
def get_meta(id: UUID):
    for m in metas:
        if m.id == id:
            return m
    raise HTTPException(status_code=404, detail="Meta não encontrada")

@app.delete("/metas/{id}")
def delete_meta(id: UUID):
    for i, m in enumerate(metas):
        if m.id == id:
            del metas[i]
            return {"mensagem": "Meta deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Meta não encontrada")

@app.put("/metas/{id}", response_model=Meta)
def atualizar_meta(id: UUID, nome: str, valor_alvo: float):
    for i, m in enumerate(metas):
        if m.id == id:
            atualizada = Meta(id=id, nome=nome, valor_alvo=valor_alvo)
            metas[i] = atualizada
            return atualizada
    raise HTTPException(status_code=404, detail="Meta não encontrada")


