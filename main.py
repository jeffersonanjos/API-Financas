# pip install fastapi uvicorn pydantic
# pip freeze > requirements.txt
# uvicorn main:app

from fastapi import FastAPI
from models import Transaction, Goal

app = FastAPI()



# Rotas de Transações
@app.post("/transacoes/")
def add_transacao(descricao: str, valor: float):
    categoria = categorize_transaction(descricao)  # IA simplificada
    transacao = Transaction(descricao=descricao, valor=valor, categoria=categoria)
    transacao.save()
    return {"message": "Transação salva!"}

@app.get("/transacoes/")
def listar_transacoes():
    return Transaction.get_all()

# Rotas de Metas (simplificado)
@app.post("/metas/")
def add_meta(nome: str, valor_alvo: float):
    meta = Goal(nome=nome, valor_alvo=valor_alvo)
    meta.save()
    return {"message": "Meta criada!"}

# Rota do Assistente de NLP
@app.post("/assistente/")
def perguntar(pergunta: str):
    resposta = nlp_query(pergunta)  # Ex: "Quanto gastei com comida?"
    return {"resposta": resposta}