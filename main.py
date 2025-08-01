# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func
from sqlmodel import select, Session
from datetime import datetime

from database import create_db_and_tables, get_session
from models.transaction import Transaction, TransactionCreate, CategoriaTransacao, GroupedTransactions, TransactionResponse, TransactionUpdate

app = FastAPI(
    title="API de Finanças Pessoais com IA",
    description="Uma solução inteligente para gestão financeira pessoal com análises preditivas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Finanças Pessoais!"}

@app.post("/transactions/", response_model=Transaction)
def create_transaction(*, session: Session = Depends(get_session), transaction: TransactionCreate):
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def read_transaction(*, session: Session = Depends(get_session), transaction_id: int):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transaction

@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(*, session: Session = Depends(get_session), transaction_id: int, transaction: TransactionUpdate):
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    transaction_data = transaction.model_dump(exclude_unset=True)
    db_transaction.sqlmodel_update(transaction_data)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(*, session: Session = Depends(get_session), transaction_id: int):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    session.delete(transaction)
    session.commit()
    return {"message": "Transação deletada com sucesso"}

# Rota para agrupar as transações por categoria
@app.get("/transactions/grouped_by_category", response_model=List[GroupedTransactions])
def read_transactions_grouped_by_category(
    session: Session = Depends(get_session)
):
    # Usa a função `func.sum` da SQLAlchemy para somar os valores agrupados
    statement = (
        select(
            Transaction.category,
            func.sum(Transaction.amount).label("total_amount")
        )
        .group_by(Transaction.category)
    )
    results = session.exec(statement).all()
    
    # Mapeia os resultados para o modelo GroupedTransactions
    grouped_data = [GroupedTransactions(category=r.category, total_amount=r.total_amount) for r in results]

    return grouped_data
    
# Rota para filtrar as transações por tipo ou categoria
@app.get("/transactions/", response_model=List[TransactionResponse])
def read_transactions(
    *, 
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = Query(default=100, lte=100),
    transaction_type: Optional[str] = None, # Parâmetro opcional para filtrar por tipo
    category: Optional[str] = None # Parâmetro opcional para filtrar por categoria
):
    # Cria a query base
    statement = select(Transaction).offset(offset).limit(limit)

    # Adiciona as condições de filtragem se os parâmetros forem fornecidos
    if transaction_type:
        statement = statement.where(Transaction.type == transaction_type)
    
    if category:
        statement = statement.where(Transaction.category == category)
        
    transactions = session.exec(statement).all()
    return transactions
